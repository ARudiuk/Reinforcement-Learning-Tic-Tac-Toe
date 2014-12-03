import numpy as np
import pylab as pl
name = "9hidden-td0"
results = np.loadtxt(name+'results.gz')
indices = np.where(results==-1)
results[indices]=1
length = np.shape(results)[0]
temp =  results[length-10000:length]
print np.shape(np.where(temp==0))
print np.shape(np.where(temp==1))
print np.shape(np.where(temp==2))
print np.average(temp,axis=0)
print length
bin_size = 1000
ticks = length/bin_size
results = np.reshape(results,(ticks,bin_size))
print np.shape(results)
results = np.average(results,axis=1)
pl.plot(results)
pl.show()