import numpy as np
import sys
import TicTacToeMLP
import time
class game:
    def __init__(self):
        self.board = np.zeros((3,3),dtype=np.int)
        self.players = [0,'x','o']

    def play_with_human(self,bot):
        move_count = 0
        player = np.random.randint(2)
        if player == 0:
            print "You go first!"
        if player == 1:
            print "You go second!"
        while(move_count<9):            
            if((move_count+player)%2==0):
                self.print_board()
                human_move = self.human_move()
                move_error = self.make_move(human_move/3,human_move%3, 1)
                if(move_error is True):
                    continue
                result = self.check_win()
                if (result != -1):
                    break
            if((move_count+player)%2==1):
                # need to switch 1 and 2s so that learner looks at relevant states
                learner_move = bot.greedy(np.reshape((self.board*2)%3,(9,)))
                learner_move_x = learner_move/3
                learner_move_y = learner_move%3
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
        self.board = np.zeros((3,3),dtype=np.int)
        move_count = 0
        #which player number is the learning bot? 1 or 2
        learner_player = np.random.randint(2)
        #go until 9 moves
        while(move_count<9):  
            # self.print_board()
            # time.sleep(2)
            if((move_count+learner_player)%2==0):
                #reshape for now, move to one dimension later
                learner_move = bot.train_move(np.reshape(self.board,(9,)),format='TD')
                learner_move_x = learner_move/3
                learner_move_y = learner_move%3
                self.last_board = np.copy(self.board)
                self.last_move = learner_move            
                move_error = self.make_move(learner_move_x,learner_move_y, 1)
                if(move_error is True):
                    continue
                result = self.check_win()                
                if (result != -1):
                    bot.train_update(100,np.reshape(self.last_board,(9,)),self.last_move,format='TD')
                    break
                if (result == -1):
                    bot.train_update(0,np.reshape(self.last_board,(9,)),self.last_move,format='TD')
            if((move_count+learner_player)%2==1):
                # need to switch 1 and 2s so that learner looks at relevant states
                learner_move = bot.train_move(np.reshape((self.board*2)%3,(9,)),format='TD')
                learner_move_x = learner_move/3
                learner_move_y = learner_move%3
                move_error = self.make_move(learner_move_x,learner_move_y, 2)
                if(move_error is True):                    
                    continue
                result = self.check_win()
                if (result != -1):
                    bot.train_update(-100,np.reshape(self.last_board,(9,)),self.last_move,format='TD')
                    break                
            move_count+=1
        if result == -1:
            return 0
        else:            
            return int(result)

    def play_with_self_mlp(self, bot):
        self.board = np.zeros((3,3),dtype=np.int)
        move_count = 0
        #which player number is the learning bot? 1 or 2
        learner_player = np.random.randint(2)
        #go until 9 moves
        while(move_count<9):
            # self.print_board()
            # time.sleep(2)
            if((move_count+learner_player)%2==0):
                #reshape for now, move to one dimension later
                learner_move = bot.train_move(np.reshape(self.board,(9,)),format='mlp',1)
                learner_move_x = learner_move/3
                learner_move_y = learner_move%3
                self.last_board[move_count] = np.copy(self.board)
                self.last_move[move_count] = learner_move
                move_error = self.make_move(learner_move_x,learner_move_y, 1)
                if(move_error is True):
                    continue
                result = self.check_win()
                if (result != -1):
                    bot.train_update(100,np.reshape(self.last_board,(9,move_count)),self.last_move[move_count],format='mlp')
                    break
                if (result == -1 and move_count == 9):
                    bot.train_update(0,np.reshape(self.last_board,(9,move_count)),self.last_move[move_count],format='mlp')
                    break
            if((move_count+learner_player)%2==1):
                # need to switch 1 and 2s so that learner looks at relevant states
                learner_move = bot.train_move(np.reshape((self.board*2)%3,(9,)),format='mlp',2)
                learner_move_x = learner_move/3
                learner_move_y = learner_move%3
                move_error = self.make_move(learner_move_x,learner_move_y, 2)
                if(move_error is True):
                    continue
                result = self.check_win()
                if (result != -1):
                    bot.train_update(-100,np.reshape(self.last_board,(9,move_count)),self.last_move[move_count],format='mlp')
                    break
                if (result == -1 and move_count == 0):
                    bot.train_update(0,np.reshape(self.last_board,(9,move_count)),self.last_move[move_count],format='mlp')
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
        for i in range(np.shape(self.board)[0]):
            if self.board[i,0]!=0:
                if self.board[i,0]==self.board[i,1] and self.board[i,1] == self.board[i,2]:
                    return self.board[i,0]
        for i in range(np.shape(self.board)[1]):
            if self.board[0,i]!=0:
                if self.board[0,i]==self.board[1,i] and self.board[1,i] == self.board[2,i]:
                    return self.board[0,i]
        if self.board[1,1]!=0:
            if self.board[0,0]==self.board[1,1] and self.board[1,1] == self.board[2,2]:
                return self.board[1,1]
            if self.board[0,2]==self.board[1,1] and self.board[1,1] == self.board[2,0]:
                return self.board[1,1]
        return -1

