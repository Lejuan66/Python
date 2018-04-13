"""Basically an abstraction of the OpenStack Python API. Spawns and terminates VMs + creates snapshots."""
# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
# https://docs.openstack.org/python-novaclient/pike/reference/api/v2/servers.html
import time
import os
import sys
import inspect
import subprocess
import pipes
from os import environ as env

import novaclient
from novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


class WorkerSpawner():
    def __init__(self,
                 flavor_name='ssc.small',
                 nics=[{'net-id': 'c35590c9-0ed0-4a95-8f32-affb94864108'}],
                 image_name='Ubuntu 16.04 LTS (Xenial Xerus) - latest',
                 secgroups=['wendelin'],
                 max_workers=8,
                 name_prefix='acc11-worker-',
                 cloud_cfg='/cloud-cfg-worker.txt',
                 snapshot_name='acc11-worker-snapshot'):
        self.nics = nics
        self.secgroups = secgroups
        self.max_workers = max_workers
        self.snapshot_name = snapshot_name
        # for IPv6 {'net-id': '522637dc-c186-4fcc-910a-09ef139d56ee'}
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                        username=env['OS_USERNAME'],
                                        password=env['OS_PASSWORD'],
                                        project_name=env['OS_PROJECT_NAME'],
                                        project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                        project_id=env['OS_PROJECT_ID'],
                                        user_domain_name=env['OS_USER_DOMAIN_NAME'])

        sess = session.Session(auth=auth)
        self.nova = client.Client('2.1', session=sess)
        self.image = self.nova.glance.find_image(image_name)
        self.flavor = self.nova.flavors.find(name=flavor_name)
        self.cfg_file_path = os.getcwd() + cloud_cfg
        # make sure cloud-cfg is there
        if not os.path.isfile(self.cfg_file_path):
            raise OSError(self.cfg_file_path + ' not found in path')

        self.instances = []
        self.names = []
        for i in range(self.max_workers):
            self.names.append(name_prefix+str(i))
        # makes us start with worker-0 atleast.
        self.names.reverse()

    def spawn(self, n=1):
        print("Spawning " + str(n) + " number of workers")

        userdatas = []
        for _ in range(n):
            userdatas.append(open(self.cfg_file_path))

        spawned = []
        for i in range(n):
            try:
                name = self.names.pop()
            except IndexError:
                print('Max worker capacity met')
                return spawned
            try:
                instance = self.nova.servers.create(
                    name=name,
                    image=self.image,
                    flavor=self.flavor,
                    userdata=userdatas[i],
                    nics=self.nics,
                    security_groups=self.secgroups,
                    key_name="wendelin_pubkey")
            except novaclient.exceptions.Forbidden:
                # out of resources
                print('SNIC out of resources')

            print("Spawned " + name)
            spawned.append(name)
            self.instances.append(instance)
        return spawned

    def terminate(self, hostname):
        """Terminate VM called hostname"""
        # unique names
        matches = list(filter(lambda x: x.name == hostname, self.instances))

        if len(matches) == 0:
            # already terminated
            return
        elif len(matches) == 1:
            instance = matches[0]
            # terminate it
            self.names.append(instance.name)
            self.instances.remove(instance)
            # actual deletion from openstack
            status = self.nova.servers.get(instance.id).status

            while status == 'BUILD':
                time.sleep(5)
                status = self.nova.servers.get(instance.id).status
                print("Waiting for VM to finish BUILD before terminating.")
            instance.delete()
            print("Worker VM " + hostname + " deleted.")
        else:
            # inconsistency in the system
            raise ValueError('More than one of same name in self.instances')

    def terminate_all(self):
        for instance in self.instances:
            self.terminate(instance.name)

    def image_available(self, image_name):
        try:
            self.nova.glance.find_image(image_name)
            return True
        except novaclient.exceptions.NotFound:
            return False

    def create_snapshot(self):
        """Auxilliary function that is used to create images.
           Not to be used in the monitor, but rather beforehand.
        """
        # Don't create if it already exists
        if self.image_available(self.snapshot_name):
            print('Snapshot already exists')
            return

        self.spawn()

        sleep_len = 10
        # Make sure the network is up
        t = 0
        networks = None
        while not networks:
            try:
                networks = self.instances[0].networks
            except:
                # not ready yet
                pass
            print('Waited {0}s for network to be up'.format(t))
            if not networks:
                time.sleep(sleep_len)
                t += sleep_len
                self.instances[0] = self.nova.servers.get(self.instances[0].id)

        # make sure an ip is received that we can ssh to
        # self.instances[0].add_floating_ip('129.16.125.236')
        t = 0
        ip = None
        while not ip:
            networks = self.instances[0].networks
            for key in networks:
                if 'IPv4' in key:
                    ips = networks[key]
                    for i in ips:
                        # change to not if we want a floating ip
                        if i.startswith('192'):
                            ip = i
                            break
                    break
            if not ip:
                time.sleep(sleep_len)
                print('Waited {0}s for ip'.format(t))
                t += sleep_len
                self.instances[0] = self.nova.servers.get(self.instances[0].id)

        # make sure cloud init finishes
        t = 0
        while not self._exists_remote(ip):
            print('Waited {0}s for cloud-init to finish'.format(t))
            time.sleep(sleep_len*3)
            t += sleep_len*3
        # create snapshot and make sure it gets active
        self.nova.servers.create_image(self.instances[0].id, self.snapshot_name, None)
        snapshot = self.nova.glance.find_image(self.snapshot_name)

        # Wait until snap
        t = 0
        status = snapshot.status
        while status != 'active':
            print('Waited {0}s for snapshot. Status is {1}'.format(t, status))
            snapshot = self.nova.glance.find_image(self.snapshot_name)
            status = snapshot.status
            time.sleep(sleep_len*3)
            t += sleep_len*3
        print('Snapshot successfully uploaded. Now terminating worker.')
        # kill created worker
        self.terminate_all()

    # https://stackoverflow.com/questions/14392432/checking-a-file-existence-on-a-remote-ssh-server-using-python
    def _exists_remote(self, host):
        """Test if a file exists at path on a host accessible with SSH."""
        # This file gets written after cloudinit is done
        # path = '/var/lib/cloud/instance/boot-finished'
        path = '/home/ubuntu/SETUP_COMPLETE'
        t = 0
        sleep_len = 10
        while True:
            status = subprocess.call(
                ['ssh', '-oStrictHostKeyChecking=no', '-i', '/home/ubuntu/.ssh/id_rsa', 'ubuntu@'+host, 'test -f {}'.format(pipes.quote(path))])
            if status == 0:
                return True
            else:
                return False
