"""Worker management the smart way with Flower."""
import requests, json
import time
from worker_spawner import WorkerSpawner


class WorkerManager():
    """Starts and stops workers depending on the task queue and active workers"""

    def __init__(self, freq_hz=1, terminate_time_s=30):
        """Init worker manager"""
        self.workers_spawning = []
        self.sleep_time = 1/freq_hz

        api_root = 'http://localhost:5555/api'
        self.queue_url = '{}/queues/length'.format(api_root)
        self.workers_url = '{}/workers?refresh=1'.format(api_root)
        self.workers_status_url = '{}/workers?refresh=1&status=1'.format(api_root)
        self.tasks_url = '{}/tasks'.format(api_root)
        self.terminate_timer = None
        self.terminate_time_s = terminate_time_s
        self.min_workers = 0
        # Assumes a snapshot has already been created and is available.
        self.ws = WorkerSpawner(
            cloud_cfg='/cloud-cfg-light-worker.txt',
            image_name='acc11-worker-snapshot',
            max_workers=8)

    def _get_worker_count(self, workers):
        return len(workers.keys()) + len(self.workers_spawning)

    def _get_queue_len(self, queues):
        # assume only one queue
        # messages and unacknowledged messages seems to be the same
        if queues['active_queues']:
            if 'messages' in queues['active_queues'][0]:
                return queues['active_queues'][0]['messages']
        else:
            return 0

    def _get_json(self, url):
        resp = requests.get(url)
        return resp.json()

    def _spawn_worker(self):
        # add number of spawned workers
        self.workers_spawning.extend(self.ws.spawn())

    def _terminate_worker(self, idle_host):
        # idle_host ~ celery@worker1
        self.ws.terminate(idle_host.split('@')[1])

    def _find_idle_worker(self, workers):
        """Find worker without assigned tasks."""
        for key, value in workers.iteritems():
            tasks = len(value['active']) + len(value['scheduled']) + len(value['reserved'])
            if tasks == 0:
                return key
        return None

    def _terminate_timer_ringing(self):
        elapsed_time_s = time.time() - self.terminate_timer
        if elapsed_time_s > self.terminate_time_s:
            return True
        else:
            return False

    def _make_workers_spawning_consistent(self, workers):
        """Removes running workers from workers_spawning list."""
        worker_names = workers.keys()
        self.workers_spawning = [name for name in self.workers_spawning if 'celery@' + name not in worker_names]

    def _filter_offline_workers(self, workers, workers_status):
        """Filter offline workers from workers list."""
        for key, value in workers_status.iteritems():
            if not value:
                try:
                    workers.pop(key)
                except KeyError:
                    print('worker status and workers inconsistency. Blame flower.')

    def run(self):
        """Continuously compares the amount of tasks in queue with the amount of workers to decide if it should spawn or terminate VMs. Strives towards a 1 to 1 relationship."""

        for _ in range(self.min_workers):
            self._spawn_worker()

        while True:
            tasks = self._get_json(self.tasks_url)
            workers = self._get_json(self.workers_url)
            workers_status = self._get_json(self.workers_status_url)
            self._filter_offline_workers(workers, workers_status)
            queues = self._get_json(self.queue_url)
            queue_len = self._get_queue_len(queues)

            self._make_workers_spawning_consistent(workers)

            print('queue_length: ' + str(queue_len))
            if queue_len > self._get_worker_count(workers):
                self._spawn_worker()
                self.terminate_timer = None

            elif self._get_worker_count(workers) == self.min_workers:
                # To maintain a minimum amount of workers.
                self.terminate_timer = None
            else:
                if self.terminate_timer:
                    if self._terminate_timer_ringing():
                        self.terminate_timer = None
                        print('Terminate timer ringing, finding idle host...')
                        idle_worker = self._find_idle_worker(workers)
                        if idle_worker:
                            self._terminate_worker(idle_worker)
                    else:
                        print('Waiting for terminate timer')

                else:
                    self.terminate_timer = time.time()

            time.sleep(self.sleep_time)


if __name__ == "__main__":
    wm = WorkerManager()
    wm.run()
