import game
import QBot_Three
import QBot_Four
import QBot_Threefxn
import numpy as np
from os import path

name = "9hidden"
bot = QBot_Threefxn.QBot_Threefxn(name,50,9,mu=0.7,learning_rate=0.2,epsilon=0.01)

# ttt = game.game(board_size = 3)
# file_exists = path.isfile(name+'results.gz')
# train_start= 0
# iterations = 100000
# if file_exists:
#     results = np.loadtxt(name+'results.gz')
#     iteration_size = np.shape(results)[0]
# else:
#     results = np.array([])
# temp = np.zeros((iterations,))
# results = np.append(results,temp)
# for i in range(iterations):
#     if(i%1000==0):
#         print i    
#     r = ttt.play_with_self(bot)
#     results[train_start+i] = r    
# bot.save_info()
# np.savetxt(name+'results.gz',results)


ttt = game.game(board_size = 3)
ttt.play_with_human(bot)