from os import path
import numpy as np
import itertools as iterT

class QBot_Four:
    def __init__(self,name,mu = 0.7, gamma = 0.4, epsilon = 0.1):
        self.name = name        
        does_file_exist = path.isfile(name+'.npy')
        if does_file_exist:
            print "Bot info exists"
            self.load_info()
        else:
            print "Bot info does not exist, new file will be made."
            #Tied to Tic-Tac-Toe currently
            states = iterT.product("012",repeat = 16)
            #make it a list first so you can do more than just iterator operators on it
            states = list(states)
            #change from char to int
            states = [map(int,x) for x in states]
            #change to numpy array so that stuff doesn't get buggy
            states = np.reshape(states,(3**16,16))
            self.Q = np.random.rand(3**16,16)*0.1-0.05
            for i in range(np.shape(self.Q)[0]):
                for j in range(np.shape(self.Q)[1]):
                    if states[i][j]!=0:
                        self.Q[i][j]=-np.inf
            temp = {}
            count=0
            for z in states:
                temp[np.array_str(z)] = self.Q[count]
                count+=1
            self.Q = temp
        self.mu = mu
        self.gamma = gamma
        self.epsilon = epsilon  
    def load_info(self):        
        self.Q = np.load(self.name+'.npy')
    def save_info(self):
        np.save(self.name,self.Q)
    def train_move(self,state):
        #Tied to Tic-Tac-Toe currently
        #use epsilon-greedy for now
        action = self.epsilon_greedy(state)
        return action    
    def train_update(self,reward,state,action):
        #shorten name of state
        s = state
        if reward == 100 or reward == -100:
            next_Q = 0
        if reward == 0:
            #calculate possible future state based on opponent making optimal move, follow by you            
            newstate = np.copy(state)            
            newstate[action] = 1            
            opponent_move = self.greedy((newstate*2)%3)            
            newstate[opponent_move]=2
           
            s2 = newstate
            next_Q = np.max(self.Q[np.array_str(s2)])
        if next_Q == -np.inf:
            next_Q = 0        
        self.Q[np.array_str(s)][action] += self.mu * (reward + self.gamma*next_Q - self.Q[np.array_str(s)][action])      
    #pass in relevant row
    def epsilon_greedy(self,state):        
        if (np.random.rand()<self.epsilon):
            #specific to tic-tac-toe 
            indices = np.where(state==0)
            pick = np.random.randint(np.shape(indices)[1])   
            return indices[0][pick]            
        else:            
            # print self.Q[self.index]
            s = state    
            return np.argmax(self.Q[np.array_str(s)])
    def greedy(self,state):
        s = state    
        return np.argmax(self.Q[np.array_str(s)])