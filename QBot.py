from os import path
import numpy as np
import itertools as iterT

class QBot:
    def __init__(self,name,mu = 0.7, gamma = 0.4, epsilon = 0.1):
        self.name = name        
        does_file_exist = path.isfile(name+'.npy')
        if does_file_exist:
            print "Bot info exists"
            self.load_info()
        else:
            print "Bot info does not exist, new file will be made."
            #Tied to Tic-Tac-Toe currently
            states = iterT.product("012",repeat = 9)
            #make it a list first so you can do more than just iterator operators on it
            states = list(states)
            #change from char to int
            states = [map(int,x) for x in states]
            #change to numpy array so that stuff doesn't get buggy
            states = np.reshape(states,(3**9,9))
            self.Q = np.random.rand(3**9,9)*0.1-0.05
            for i in range(np.shape(self.Q)[0]):
                for j in range(np.shape(self.Q)[1]):
                    if states[i][j]!=0:
                        self.Q[i][j]=-np.inf
            temp = [[[[[[[[[np.array([0]) for a in range(3)]for b in range(3)] for c in range(3)]for d in range(3)]for e in range(3)]for f in range(3)] for g in range(3)]for h in range(3)]for i in range(3)]
            count=0
            for z in states:
                temp[z[0]][z[1]][z[2]][z[3]][z[4]][z[5]][z[6]][z[7]][z[8]] = self.Q[count]
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
            next_Q = np.max(self.Q[s2[0]][s2[1]][s2[2]][s2[3]][s2[4]][s2[5]][s2[6]][s2[7]][s2[8]])
        if next_Q == -np.inf:
            next_Q = 0        
        self.Q[s[0]][s[1]][s[2]][s[3]][s[4]][s[5]][s[6]][s[7]][s[8]][action] += self.mu * (reward + self.gamma*next_Q - self.Q[s[0]][s[1]][s[2]][s[3]][s[4]][s[5]][s[6]][s[7]][s[8]][action])      
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
            return np.argmax(self.Q[s[0]][s[1]][s[2]][s[3]][s[4]][s[5]][s[6]][s[7]][s[8]])
    def greedy(self,state):
        s = state    
        return np.argmax(self.Q[s[0]][s[1]][s[2]][s[3]][s[4]][s[5]][s[6]][s[7]][s[8]])