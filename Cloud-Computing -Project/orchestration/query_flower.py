"""Used for testing the flower api"""
api_root = 'http://localhost:5555/api'


url = '{}/queues/length'.format(api_root)
print(url)
resp = requests.get(url)
print(resp.json())


url = '{}/workers?refresh=1'.format(api_root)
print(url)
resp = requests.get(url)
workers = resp.json()
print(workers.keys())


url = '{}/tasks'.format(api_root)
print(url)
resp = requests.get(url)
tasks = resp.json()
print(tasks)

# var ws = new WebSocket('ws://localhost:5555/api/task/events/task-succeeded/');
# ws.onmessage = function (event) {
#     console.log(event.data);
# }
