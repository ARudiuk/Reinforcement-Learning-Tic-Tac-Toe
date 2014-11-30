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
                if (result != -1):
                    break
            if((move_count+player)%2==1):
                # need to switch 1 and 2s so that learner looks at relevant states
                learner_move = bot.greedy(np.reshape((self.board*2)%3,(self.board_tile_count,)))
                learner_move_x = learner_move/self.board_size
                learner_move_y = learner_move%self.board_size
                move_error = self.make_move(learner_move_x,learner_move_y, 2)
                if(move_error is True):                    
                    continue
                result = self.check_win()
                if (result != -1):                    
                    break                
            move_count+=1
        self.print_board()
        if result == -1:
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
            # time.sleep(2)
            if((move_count+learner_player)%2==0):
                #reshape for now, move to one dimension later
                learner_move = bot.train_move(np.reshape(self.board,(self.board_tile_count,)))
                learner_move_x = learner_move/self.board_size
                learner_move_y = learner_move%self.board_size
                self.last_board = np.copy(self.board)
                self.last_move = learner_move            
                move_error = self.make_move(learner_move_x,learner_move_y, 1)                
                if(move_error is True):
                    continue
                result = self.check_win()                
                if (result != -1):
                    bot.train_update(100,np.reshape(self.last_board,(self.board_tile_count,)),self.last_move)
                    break
                if (result == -1):
                    bot.train_update(0,np.reshape(self.last_board,(self.board_tile_count,)),self.last_move)
            if((move_count+learner_player)%2==1):
                # need to switch 1 and 2s so that learner looks at relevant states
                learner_move = bot.train_move(np.reshape((self.board*2)%3,(self.board_tile_count,)))
                learner_move_x = learner_move/self.board_size
                learner_move_y = learner_move%self.board_size
                move_error = self.make_move(learner_move_x,learner_move_y, 2)
                if(move_error is True):                    
                    continue
                result = self.check_win()
                if (result != -1):
                    bot.train_update(-100,np.reshape(self.last_board,(self.board_tile_count,)),self.last_move)
                    break                
            move_count+=1
        if result == -1:
            return 0
        else:            
            return int(result)
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
                if self.board[i,0]==self.board[i,1] and self.board[i,1] == self.board[i,2]:
                    return self.board[i,0]
        for i in range(self.board_size):
            if self.board[0,i]!=0:
                if self.board[0,i]==self.board[1,i] and self.board[1,i] == self.board[2,i]:
                    return self.board[0,i]
        if self.board[1,1]!=0:
            if self.board[0,0]==self.board[1,1] and self.board[1,1] == self.board[2,2]:
                return self.board[1,1]
            if self.board[0,2]==self.board[1,1] and self.board[1,1] == self.board[2,0]:
                return self.board[1,1]
        return -1

