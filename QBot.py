from os import path
import numpy as np
import itertools as iterT

class QBot:
    def __init__(self,name,mu = 0.7, gamma = 0.4, epsilon = 0.1):
        self.name = name        
        does_file_exist = path.isfile(name+'.npy')
        self.states = iterT.product("012",repeat = 9)
        #try other structures like sets, or dictionaries for speed
        #timeit for timing
        #make it a list first so you can do more than just iterator operators on it
        self.states = list(self.states)
        #change from char to int
        self.states = [map(int,x) for x in self.states]
        #change to numpy array so that stuff doesn't get buggy
        self.states = np.reshape(self.states,(3**9,9))
        if does_file_exist:
            print "Bot info exists"
            self.load_info()
        else:
            print "Bot info does not exist, new file will be made."
            #Tied to Tic-Tac-Toe currently
            self.Q = np.random.rand(3**9,9)*0.1-0.05
            for i in range(np.shape(self.Q)[0]):
                for j in range(np.shape(self.Q)[1]):
                    if self.states[i][j]!=0:
                        self.Q[i][j]=-np.inf
        self.mu = mu
        self.gamma = gamma
        self.epsilon = epsilon  
    def load_info(self):        
        self.Q = np.load(self.name+'.npy')
    def save_info(self):
        np.savetxt(self.name+'.txt',self.Q)
        np.save(self.name,self.Q)
    def train_move(self,state):
        self.state = state
        #Tied to Tic-Tac-Toe currently
        for i in range(np.shape(self.states)[0]):
            if np.array_equiv(self.states[i][:],state):
                self.index = i
                break       
        #use epsilon-greedy for now
        self.action = self.epsilon_greedy(self.states[self.index])
        return self.action
    def train_update(self,reward,newstate):
        self.Q[self.index,self.action] += self.mu* (reward + self.gamma*np.max(newstate) - self.Q[self.index,self.action])
        self.state = newstate
    #pass in relevant row
    def epsilon_greedy(self,state):
        indices = np.where(state==0)
        # print indices[0]
        if (np.random.rand()<self.epsilon):
            #specific to tic-tac-toe
            pick = np.random.randint(np.shape(indices)[1])           
            return indices[0][pick]            
        else:            
            # print self.Q[self.index]
            return np.argmax(self.Q[self.index])