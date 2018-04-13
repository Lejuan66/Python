"""Worker management the stupid way without Flower.
DEPRECATED. flower_manager.py is used instead.
"""
from celery import Celery
from worker_spawner import WorkerSpawner


class WorkerManager():

    def __init__(self):
        """Init worker manager"""
        self.task_count = 0
        self.worker_spawning = 0
        self.worker_despawning = []
        self.workers = []
        # Assumes a snapshot has already been created and is available.
        # self.ws = WorkerSpawner(image_name='acc11-worker-snapshot')
        self.ws = WorkerSpawner(
            cloud_cfg='/cloud-cfg-light-worker.txt',
            image_name='acc11-worker-snapshot',
            max_workers=2)

    def get_worker_count(self):
        return len(self.workers) + self.worker_spawning - len(self.worker_despawning)

    def should_spawn_worker(self):
        worker_count = self.get_worker_count()
        if self.task_count > worker_count:
            return True
        else:
            return False

    def should_terminate_worker(self):
        if self.task_count < self.get_worker_count():
            return True
        else:
            return False

    def spawn_worker(self):
        # add number of spawned workers
        self.worker_spawning += self.ws.spawn()

    def terminate_worker(self, idle_host):
        self.worker_despawning.append(idle_host)
        self.workers.remove(idle_host)
        self.ws.terminate(idle_host.split('@')[1])

    def monitor(self, app):
        state = app.events.State()

        def handle_succeeded_tasks(event):
            self.task_count -= 1
            print("task finished, tasks active: " + str(self.task_count))
            if self.should_terminate_worker():
                # TODO: replace with a real idle host
                idle_host = self.workers[0]
                self.terminate_worker(idle_host)

        def handle_sent_tasks(event):
            self.task_count += 1
            print("task started, tasks active: " + str(self.task_count))
            if self.should_spawn_worker():
                self.spawn_worker()

        def handle_worker_online(event):
            state.event(event)
            self.workers.append(event['hostname'])
            if self.worker_spawning > 0:
                self.worker_spawning -= 1
            print("worker online: " + event['hostname'] + " count: " + str(len(self.workers)))

        def handle_worker_offline(event):
            state.event(event)
            self.workers.remove(event['hostname'])
            try:
                self.worker_despawning.remove(event['hostname'])
            except ValueError:
                pass
            print("worker offline: " + event['hostname'] + " count: " + str(len(self.workers)))
            # direct terminate to make sure it's removed. In case of celery crash
            self.ws.terminate(event['hostname'])

        with app.connection() as connection:
            recv = app.events.Receiver(connection, handlers={
                'task-succeeded': handle_succeeded_tasks,
                'task-sent': handle_sent_tasks,
                'worker-online': handle_worker_online,
                'worker-offline': handle_worker_offline,
            })
            recv.capture(limit=None, timeout=None, wakeup=True)


app = Celery(broker='pyamqp://rabbit:wabbit@localhost/vrabbit')
wm = WorkerManager()
wm.monitor(app)
