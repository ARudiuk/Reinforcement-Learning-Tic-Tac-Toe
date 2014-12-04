import numpy as np
import sys
import time
class game:
    def __init__(self,board_size=3):
        self.board_size = board_size
        self.board_tile_count = self.board_size*self.board_size
        self.board = np.zeros((self.board_size,self.board_size),dtype=np.int)
        self.players = [0,'x','o']

    def play_with_human(self,bot):
        move_count = 0
        player = np.random.randint(2)
        if player == 0:
            print "You go first!"
        if player == 1:
            print "You go second!"        
        while(move_count<self.board_tile_count):            
            if((move_count+player)%2==0):
                self.print_board()
                human_move = self.human_move()
                move_error = self.make_move(human_move/self.board_size,human_move%self.board_size, 1)
                if(move_error is True):
                    continue
                result = self.check_win()
                if (result == 1):
                    break
            if((move_count+player)%2==1):
                # need to switch 1 and 2s so that learner looks at relevant states
                learner_move = bot.greedy(-1*self.board)
                learner_move_x = learner_move/self.board_size
                learner_move_y = learner_move%self.board_size
                move_error = self.make_move(learner_move_x,learner_move_y, -1)
                if(move_error is True):                    
                    continue
                print self.board
                result = self.check_win()
                if (result == -1):                    
                    break                
            move_count+=1
        self.print_board()
        if result == 0:
            print "Draw, No Winner! Get Good Scrub"
        else:
            print self.players[int(result)], "Wins!"

    def play_with_self(self,bot):
        self.board = np.zeros((self.board_size,self.board_size),dtype=np.int)
        move_count = 0
        #which player number is the learning bot? 1 or 2
        learner_player = np.random.randint(2)
        #go until board is filled
        while(move_count<self.board_tile_count):  
            # self.print_board()
            # time.sleep(1)
            if((move_count+learner_player)%2==0):
                #reshape for now, move to one dimension later
                learner_move = self.check_if_winning_move_exists(1)
                if learner_move == -1:                    
                    learner_move = bot.train_move(self.board)
                learner_move_x = learner_move/self.board_size
                learner_move_y = learner_move%self.board_size
                self.last_move = np.copy(learner_move)
                self.last_state = np.copy(self.board)
                move_error = self.make_move(learner_move_x,learner_move_y, 1) 
                if(move_error is True):                    
                    continue
                result = self.check_win()                
                if (result == 1):
                    bot.train_update(1,0,0,self.last_move,self.last_state)
                    break                
            if((move_count+learner_player)%2==1):
                # need to switch 1 and 2s so that learner looks at relevant states
                learner_move = self.check_if_winning_move_exists(-1)
                if learner_move == -1:                    
                    learner_move = bot.train_move(-1*self.board)
                learner_move_x = learner_move/self.board_size
                learner_move_y = learner_move%self.board_size
                move_error = self.make_move(learner_move_x,learner_move_y, -1)
                if(move_error is True):
                    continue
                result = self.check_win()                
                if (result == -1):
                    bot.train_update(0,1,0,self.last_move,self.last_state)
                    break
                if (result == 0 and move_count != self.board_tile_count-1 and move_count != 0):
                    bot.train_update(0,0,0,self.last_move,self.last_state)
            move_count+=1
        if result == 0:
            bot.train_update(0,0,1,self.last_move,self.last_state)
            return 0
        else:            
            return int(result)
    def check_if_winning_move_exists(self,player):        
        for i in range(np.shape(self.board)[0]):
            for j in range(np.shape(self.board)[1]):
                if(self.board[i][j]==0):
                    self.board[i][j]=player
                    winning_player = self.check_win()
                    if winning_player == 0:
                        self.board[i][j]=0
                    else:
                        self.board[i][j]=0
                        return j+i*self.board_size
        return -1


    def make_move(self,x,y,player):
        if(self.board[x,y]==0):
            self.board[x,y]=player
        else:
            print "Invalid Move"
            return True           

    def simple_ai_move(self):
        #use incredibly bad AI
        for i in range(np.shape(self.board)[0]):
            for j in range(np.shape(self.board)[1]):
                if(self.board[i][j]==0):
                    return i,j
    def human_move(self):
        move = raw_input("Where do you want to place your piece?")
        move = int(move)
        return move 

    def print_board(self):
        for i in range(np.shape(self.board)[0]):
            for j in range(np.shape(self.board)[1]):
                pos = i*np.shape(self.board)[1]+(j)
                if self.board[i,j] == 0:
                    sys.stdout.write(str(pos))
                else:
                    sys.stdout.write(self.players[int(self.board[i,j])])
                sys.stdout.write(' | ')
            sys.stdout.write('\n')
            if(i<np.shape(self.board)[0]-1):
                for j in range(np.shape(self.board)[1]):
                    sys.stdout.write('- - ')
                sys.stdout.write('\n')
        print '\n'

    def check_win(self):
        for i in range(self.board_size):
            if self.board[i,0]!=0:
                if self.board_size == 3 and self.board[i,0]==self.board[i,1] and self.board[i,1] == self.board[i,2]:
                    return self.board[i,0]
                if self.board_size == 4 and self.board[i,0]==self.board[i,1] and self.board[i,1] == self.board[i,2] and self.board[i,2] == self.board[i,3]:
                    return self.board[i,0]
        for i in range(self.board_size):
            if self.board[0,i]!=0:
                if self.board_size == 3 and self.board[0,i]==self.board[1,i] and self.board[1,i] == self.board[2,i]:
                    return self.board[0,i]
                if self.board_size == 4 and self.board[0,i]==self.board[1,i] and self.board[1,i] == self.board[2,i] and self.board[2,i] == self.board[3,i]:
                    return self.board[0,i]        
        if self.board[1,1]!=0 and self.board_size == 3:
            if self.board[0,0]==self.board[1,1] and self.board[1,1] == self.board[2,2]:
                return self.board[1,1]
            if self.board[0,2]==self.board[1,1] and self.board[1,1] == self.board[2,0]:
                return self.board[1,1]
        if self.board_size == 4:
            if self.board[1,1]!=0 and self.board[0,0]==self.board[1,1] and self.board[1,1] == self.board[2,2] and self.board[2,2] == self.board[3,3]:
                return self.board[1,1]
            if self.board[1,2]!=0 and self.board[0,3]==self.board[1,2] and self.board[1,2] == self.board[2,1] and self.board[2,1] == self.board[3,0]:
                return self.board[0,3]
        return 0

