import pylab as pl
import numpy as np
import time


class ANN:

    #Initlialize
    def __init__(self,feature_size,output_size, nhidden1, momentum = 0, beta = 1,learning_rate=0.4):
        #use positive ones for bias node as opposed to book and position on the left of input
        #only works for input that is two dimensional because of shape(x)[1] looking for size of second dimension\
        #all variables are initialized, even ones that might not be used like the number of hidded nodes in a 
        #hidden layer         
        #number of features plus bias
        self.feature_size = feature_size
        #number of ouputs
        self.output_size = output_size
        #hidden layer 1 size
        self.hidden_layer1_size = nhidden1     
        #set momentum
        self.momentum = momentum
        #set beta term for logistic function
        self.beta = beta
        #set learning rate
        self.learning_rate = learning_rate        

        #initialize weight matrices    
        self.weights1 = (np.random.rand(self.feature_size+1,self.hidden_layer1_size)-0.5)*2/np.sqrt(self.feature_size+1)
        self.weights2 = (np.random.rand(self.hidden_layer1_size+1, self.output_size) - 0.5)* 2/np.sqrt(self.hidden_layer1_size+1)
        self.updatew1 = np.zeros((np.shape(self.weights1)))
        self.updatew2 = np.zeros((np.shape(self.weights2)))    

    #do a forward pass using the current weights using the provided data
    #if no data is provided then use the entire input data set
    #in the future it'd be nice to have more activation functions than logistic
    def forward_pass(self, input_data, action):
        temp = np.zeros((self.feature_size/4,))
        temp[action]=1
        action=temp
        input_data = np.append(input_data,action) 
        input_data = np.concatenate((np.array([1]),input_data))
        self.input_data = np.reshape(input_data,(1,self.feature_size+1))
        self.hidden1 = np.dot(self.input_data, self.weights1)
        self.hidden1 = 1.0/(1.0+np.exp(-self.beta*self.hidden1))
        self.hidden1 = np.concatenate((np.ones((1,1)),self.hidden1),axis=1) 
        self.outputs = np.dot(self.hidden1, self.weights2)       
        return 1.0/(1.0+np.exp(-self.beta*self.outputs))    
    def update_weights(self,state,action,target):
        self.output = self.forward_pass(state,action)         
        #calculate error based on logistic
        # print "start"
        # print self.output
        # print target
        # print self.output-target
        # print (self.output-target)**2
        # time.sleep(2)
        deltao = self.beta*(self.output-target)*self.output*(1.0-self.output)
        #calculate errors depending on amount of hidden layers
        deltah1 = self.hidden1*self.beta*(1.0-self.hidden1)*(np.dot(deltao,np.transpose(self.weights2)))
        self.updatew1 = self.learning_rate*(np.dot(np.transpose(self.input_data),deltah1[:,1:])) + self.momentum*self.updatew1
        self.updatew2 = self.learning_rate*(np.dot(np.transpose(self.hidden1),deltao)) + self.momentum*self.updatew2
        self.weights1 -= self.updatew1
        self.weights2 -= self.updatew2