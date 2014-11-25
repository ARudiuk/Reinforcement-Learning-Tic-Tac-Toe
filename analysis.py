import numpy as np
import pylab as pl
name = "test"
results = np.load(name+'results'+'.npy')
length = np.shape(results)[0]
ticks = length/100
results = np.reshape(results,(ticks,100))
results = np.average(results,axis=1)
pl.plot(results)
pl.show()