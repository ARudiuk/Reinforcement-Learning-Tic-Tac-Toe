from os import path
import numpy as np
import itertools as iterT
import tdann
import time

class QBot_Threefxn:
    def __init__(self,name,nhidden,board_size,mu = 0.2, gamma = 0.7, epsilon = 0.2,learning_rate=0.4):
        self.name = name
        self.board_size = board_size
        self.nhidden = nhidden
        self.learning_rate = learning_rate
        does_file_exist = path.isfile(name+'weights1'+'.npy')
        self.ann = tdann.ANN(self.board_size*3+1,3,self.nhidden,learning_rate=self.learning_rate)
        if does_file_exist:
            print "Bot info exists"
            self.load_info()
        if not does_file_exist:
            print "Bot info does not exist"
        # else:
        #     print "Bot info does not exist, new file will be made."
        #     self.ann = ann.ann(self.board_size*2+1,2,self.nhidden,learning_rate=self.learning_rate)
        self.mu = mu
        self.gamma = gamma
        self.epsilon = epsilon
    def load_info(self):
        temp1 = np.load(self.name+'weights1'+'.npy')
        temp2 = np.load(self.name+'weights2'+'.npy')
        self.ann.weights1 = temp1
        self.ann.weights2 = temp2
    def save_info(self):
        np.save(self.name+'weights1',self.ann.weights1)
        np.save(self.name+'weights2',self.ann.weights2)
    def convert_state(self,state):
        temp = np.array([])
        state = np.reshape(state,(1,self.board_size))
        for i in range(np.shape(state)[1]):
            if(state[0][i]==0):
                temp = np.append(temp,0)
                temp = np.append(temp,0)
                temp = np.append(temp,1)
            if(state[0][i]==1):
                temp = np.append(temp,1)
                temp = np.append(temp,0)
                temp = np.append(temp,0)
            if(state[0][i]==-1): 
                temp = np.append(temp,0)
                temp = np.append(temp,1)
                temp = np.append(temp,0)
        return temp
    def train_move(self,state):
        #Tied to Tic-Tac-Toe currently
        #use epsilon-greedy for now 
        old_state = np.reshape(np.copy(state),(1,self.board_size))
        state=self.convert_state(state)
        action = self.epsilon_greedy(state,old_state)
        return action    
    def train_update(self,reward1,reward2,reward3,move_list,state_list):
        local_mu = self.mu
        move_size = len(move_list)        
        state = self.convert_state(state_list[0])
        # error = self.mu * (reward + self.gamma*next_Q - self.Q[s[0]][s[1]][s[2]][s[3]][s[4]][s[5]][s[6]][s[7]][s[8]][action])      
        self.ann.update_weights(state,move_list[0],np.array([reward1,reward2,reward3]),local_mu)
        local_mu = local_mu*0.7        
        for i in range(1,move_size):
            state = self.convert_state(state_list[i])
            # error = self.mu * (reward + self.gamma*next_Q - self.Q[s[0]][s[1]][s[2]][s[3]][s[4]][s[5]][s[6]][s[7]][s[8]][action])      
            self.ann.update_weights(state,move_list[i],np.array([reward1,reward2,reward3]),local_mu)
            local_mu = local_mu*0.7             
    #pass in relevant row
    def epsilon_greedy(self,state,old_state):
        old_state = np.reshape(old_state,(self.board_size,))
        indices = np.where(old_state==0)
        if (np.random.rand()<self.epsilon):
            pick = np.random.randint(np.shape(indices)[1])   
            return indices[0][pick]            
        else:            
            # print self.Q[self.index] 
            win_value = -1
            win_index = -1
            # loss_value = np.inf
            # loss_index = np.inf
            draw_value = -1
            draw_index = -1
            for i in range(np.shape(indices)[1]):
                temp = self.ann.forward_pass(state,indices[0][i])                
                if temp[0][0]>win_value and temp[0][0]>temp[0][1]:
                    win_value = temp[0][0]
                    win_index = indices[0][i]
                # if temp[0][1]<loss_value:
                #     loss_value = temp[0][1]
                #     loss_index = indices[0][i]
                if temp[0][2]>draw_value:
                    draw_value = temp[0][2]
                    draw_index = indices[0][i]
            if(win_value>-1):
                return win_index
            else:
                return draw_index
    def greedy(self,state):
        old_state = np.reshape(np.copy(state),(1,self.board_size))
        old_state = np.reshape(old_state,(self.board_size,))         
        state = self.convert_state(state)       
        indices = np.where(old_state==0)
        # print self.Q[self.index] 
        win_value = -1
        win_index = -1
        # loss_value = np.inf
        # loss_index = np.inf
        draw_value = -1
        draw_index = -1
        for i in range(np.shape(indices)[1]):
            temp = self.ann.forward_pass(state,indices[0][i]) 
            print temp
            if temp[0][0]>win_value and temp[0][0]>temp[0][1]:
                win_value = temp[0][0]
                win_index = indices[0][i]
            # if temp[0][1]<loss_value:
            #     loss_value = temp[0][1]
            #     loss_index = indices[0][i]
            if temp[0][2]>draw_value:
                draw_value = temp[0][2]
                draw_index = indices[0][i]
        if(win_value>-1):
            return win_index
        else:
            return draw_index