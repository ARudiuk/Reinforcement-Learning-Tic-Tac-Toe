import matplotlib.pyplot as plt
import numpy as np
data = np.load('testfile.npy')
data = np.reshape(data, (3**9*9, 1))
size = np.shape(data)
print size
plt.plot(data[1:1000])
plt.show()