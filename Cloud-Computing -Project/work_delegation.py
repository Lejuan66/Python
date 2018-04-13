"Entry point of function. Takes user parameters and divides it up into angles, which are distributed to workers."
import subprocess
from celery.result import ResultSet
from tasks import airfoil
from timeit import default_timer as timer


def _key_string(angle, num_nodes, levels, NACA, num_samples, viscosity, speed, sim_time):
    """Returns database key for the parameters."""
    return str(angle) + '_' + str(num_nodes) + '_' + str(levels) + '_' + NACA + '_' + str(num_samples) + '_' + str(viscosity) + '_' + str(speed) + '_' + str(sim_time)


def _result_string(start_angle, stop_angle, num_angles, num_nodes, levels, NACA, num_samples, viscosity, speed, sim_time):
    """Returns the file path of the result for the given parameters."""
    return str(start_angle) + '_' + str(stop_angle) + '_' + str(num_angles) + '_' + str(num_nodes) + '_' + str(levels) + '_' + NACA + '_' + str(num_samples) + '_' + str(viscosity) + '_' + str(speed) + '_' + str(sim_time) + '.tar.gz'


# called by flask
def divide_work(start_angle, stop_angle, num_angles, num_nodes, levels, NACA, num_samples, viscosity, speed, sim_time):
    anglediff = (stop_angle - start_angle) // num_angles

    # http://docs.celeryproject.org/en/latest/reference/celery.result.html#celery.result.ResultSet
    in_progress = ResultSet([])
    results = []
    # +1 to match runme.sh
    for i in range(0, num_angles+1):
        angle = start_angle + anglediff*i
        key = _key_string(angle, num_nodes, levels, NACA, num_samples, viscosity, speed, sim_time)

        # query database
        # possibly add something more to check if the result is queued and pending. Simultaneous queries will cause double tasks to be added to the queue, since the tasks are pending. Possibly add a global queue that we append in progress results to, which we check if status is pending.
        result = airfoil.AsyncResult(key)
        if result.status == 'SUCCESS':
            alrdy_queued = True
            results.append(result.get())

        elif result.status in ['STARTED', 'RETRY']:
            alrdy_queued = True
            in_progress.add(result)

        elif result.status == 'PENDING':
            alrdy_queued = False

        else:
            print('Task status FAILURE.')
            alrdy_queued = False

        if not alrdy_queued:
            result = airfoil.apply_async((angle, num_nodes, levels, NACA, num_samples, viscosity, speed, sim_time, key), task_id=key)
            in_progress.add(result)

    # waiting for all results
    # in_progress.join_native() is supposed to be more efficient, but it seems to hang
    results.extend(in_progress.join()) # list of all results
    result_file = _result_string(start_angle, stop_angle, num_angles, num_nodes, levels, NACA, num_samples, viscosity, speed, sim_time)
    results_archive = '/home/ubuntu/results/' + result_file
    tar_cmd = ['tar', '-zcvf', results_archive, '-C', '/home/ubuntu/sync_results']
    tar_cmd.extend(results)

    subprocess.call(tar_cmd)
    return result_file

# for doing a test run.
if __name__ == '__main__':
    start = timer()
    result_archive = divide_work(0, 30, 10, 200, 1, '0012', 10, 0.1, 10.0, 1)

    end = timer()
    print(str(end-start))
    print(result_archive)
