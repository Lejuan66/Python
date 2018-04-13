import matplotlib.pyplot as plt

Spawned =[1, 2, 3, 4, 5, 6, 7, 8]
Online = [152,152,160,161,162,170,181,182]
Deleted = [364,394,424,454,484,514,544,574]
m_colors = ["red","green","blue","yellow","orange","purple","pink","black"]
fig, ax = plt.subplots()
worker_names = []
worker_names_pos =[]
x_ticks = []
x_max = max(Deleted)
x_tick =0 
x_ticks.append(x_tick)
while(x_tick <= x_max):
	x_tick += 60
	x_ticks.append(x_tick)

for i in Spawned:
	
	index = i -1
	worker_names.append("Worker " + str(i))
	worker_names_pos.append(15 + index*10)
	ax.broken_barh([(Online[index], Deleted[index] - Online[index])], (10* i, 5), facecolors=m_colors[index])
ax.set_ylim(5, worker_names_pos[-1] +5)
ax.set_xlim(0, x_tick)
ax.set_xlabel('seconds since start')
ax.set_yticks(worker_names_pos)
ax.set_yticklabels(worker_names)
ax.grid(True)
plt.xticks(x_ticks)

plt.show()