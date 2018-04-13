import matplotlib.pyplot as plt
import numpy as np


worker1 = [121.812595844, 137.795418024, 123.066055059]
worker2 = [133.266366005, 115.550198078, 119.492813826]
worker3 = [125.482635021, 124.849133015, 121.949814081]
worker4 = [141.718168974, 126.107424021, 124.244347811]
worker5 = [128.563075066, 134.929493904, 133.166479826]
worker6 = [135.515371799, 141.633826971, 133.037237883]
worker7 = [145.099139929, 137.332015038, 138.624593019]
worker8 = [153.783060074, 162.558688164, 145.318677902]


y_data = [worker1, worker2, worker3, worker4, worker5, worker6, worker7, worker8]
y = []
e = []
for worker_data in y_data:
    y.append(np.mean(worker_data))
    e.append(np.std(worker_data))

x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
e = np.array(e)
y = np.array(y)

plt.errorbar(x, y, e, marker='x', ecolor='r')
plt.ylabel('Time (s)')
plt.xlabel('Number of VMs and workers')
plt.title('Weak-scaling of Airfoil')
print("Means: " + str(y))
print("Std: " + str(e))
plt.savefig('weak-scaling.png')
plt.show()
