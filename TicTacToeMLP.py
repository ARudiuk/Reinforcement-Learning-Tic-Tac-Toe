import numpy as np
import kmeans
import pylab as pl
import game

class mlp:
    def __init__(self,nhidden,beta=1,momentum=0.9,outtype='logistic'):
        """ Constructor """
        # Set up network size
        self.nin = 9
        self.nout = 1
        self.ndata = 1
        self.nhidden = nhidden
        self.outputs = np.zeros((9,))
        self.beta = beta
        self.momentum = momentum
        self.outtype = outtype

        # Initialise network
        self.weights1 = (np.random.rand(self.nin+1,self.nhidden)-0.5)*2/np.sqrt(self.nin)
        self.weights2 = (np.random.rand(self.nhidden+1,self.nout)-0.5)*2/np.sqrt(self.nhidden)

    def mlptrain(self,inputs,selected_outputs,rewards,eta,lambd):
        move_count = np.shape(inputs)[1]
        """ Train the thing """
        # Add the inputs that match the bias node
        inputs = np.concatenate((inputs,-np.ones((self.ndata,1))),axis=1)
        change = range(self.ndata)

        updatew1 = np.zeros((np.shape(self.weights1)))
        updatew2 = np.zeros((np.shape(self.weights2)))
        deltao = np.zeros((np.shape(selected_outputs)[0],move_count))
        deltah = np.zeros((np.shape(selected_outputs)[0],move_count))
        for n in range(move_count):

#            if (np.mod(n,100)==0):
#                print "Iteration: ",n, " Error: ",error

            # Different types of output neurons
            if self.outtype == 'linear':
                deltao[n] = (selected_outputs[n]-rewards[n])/self.ndata
            elif self.outtype == 'logistic':
                deltao[n] = self.beta*(selected_outputs[n]-rewards[n])*selected_outputs[n]*(1.0-selected_outputs[n])
            elif self.outtype == 'softmax':
                deltao[n] = (selected_outputs[n]-rewards[n])*(selected_outputs[n]*(-selected_outputs[n])+selected_outputs[n])/self.ndata
            else:
                print "error"

            deltah[n] = self.hidden*self.beta*(1.0-self.hidden)*(np.dot(deltao[n],np.transpose(self.weights2)))
        for n in range(move_count, 0, -1):
            sum1 = 0
            sum2 = 0
            for i in range(n):
                sum1 = (lambd**(n-i))*deltah[i] + sum1
                sum2 = (lambd**(n-i))*deltao[i] + sum2
            if n==move_count:
                updatew1 = eta*(rewards[n]-selected_outputs[n])*sum1
                updatew2 = eta*(rewards[n]-selected_outputs[n])*sum2
            else:
                updatew1 = eta*(selected_outputs[n+1]-selected_outputs[n])*sum1
                updatew2 = eta*(selected_outputs[n+1]-selected_outputs[n])*sum2
            self.weights1 += updatew1
            self.weights2 += updatew2

            # Randomise order of inputs (not necessary for matrix-based calculation)
            #np.random.shuffle(change)
            #inputs = inputs[change,:]
            #targets = targets[change,:]

    def mlpfwd(self,inputs):
        """ Run the network forward """

        self.hidden = np.dot(inputs,self.weights1);
        self.hidden = 1.0/(1.0+np.exp(-self.beta*self.hidden))
        self.hidden = np.concatenate((self.hidden,-np.ones((np.shape(inputs)[0],1))),axis=1)

        outputs = np.dot(self.hidden,self.weights2);

        # Different types of output neurons
        if self.outtype == 'linear':
            return outputs
        elif self.outtype == 'logistic':
            return 1.0/(1.0+np.exp(-self.beta*outputs))
        elif self.outtype == 'softmax':
            normalisers = np.sum(np.exp(outputs),axis=1)*np.ones((1,np.shape(outputs)[0]))
            return np.transpose(np.transpose(np.exp(outputs))/normalisers)
        else:
            print "error"

    def confmat(self,inputs,targets):
        """Confusion matrix"""

        # Add the inputs that match the bias node
        inputs = np.concatenate((inputs,-np.ones((np.shape(inputs)[0],1))),axis=1)
        outputs = self.mlpfwd(inputs)

        nclasses = np.shape(targets)[1]

        if nclasses==1:
            nclasses = 2
            outputs = np.where(outputs>0.5,1,0)
        else:
            # 1-of-N encoding
            outputs = np.argmax(outputs,1)
            targets = np.argmax(targets,1)

        cm = np.zeros((nclasses,nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                cm[i,j] = np.sum(np.where(outputs==i,1,0)*np.where(targets==j,1,0))

#        print "Confusion matrix is:"
#        print cm
#        print "Percentage Correct: ",np.trace(cm)/np.sum(cm)*100
        return np.trace(cm)/np.sum(cm)*100

    def tictactoe(self,inputs):
        inputs = np.reshape(inputs,(np.shape(inputs)[0],1))
        inputs = np.transpose(inputs)
        inputs = np.concatenate((inputs,-np.ones((np.shape(inputs)[0],1))),axis=1)
        outputs = self.mlpfwd(inputs)
        return outputs