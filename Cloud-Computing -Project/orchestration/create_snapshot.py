from worker_spawner import WorkerSpawner

# Tries to create snapshot 'acc11-worker-snapshot'. Won't if it already exists.
ws = WorkerSpawner()

ws.create_snapshot()
