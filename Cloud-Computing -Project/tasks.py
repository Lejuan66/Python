import time
from celery import Celery
from docker_container.py_airfoil import do_single_mesh_result

# localhost gets replaced by script in cloudinit.
app = Celery('tasks',
             broker ='pyamqp://rabbit:wabbit@localhost/vrabbit',
             backend = 'redis://localhost:6379/0',
)

app.conf.update(
    worker_send_task_events = True,
    task_send_sent_event = True,
    worker_prefetch_multiplier = 1,
    task_acks_late = True,
    task_reject_on_worker_lost = True,
)

@app.task
def airfoil(angle=0, points=200, refinements=0, NACA='0012', samples=10,
            viscosity=0.0001, velocity=10, sim_time=1,
            result_filename='results'):
    # Call airfoil function in worker
    result_filepath = do_single_mesh_result(angle, points, refinements, NACA, samples, viscosity, velocity, sim_time, result_filename)

    return result_filepath
