import game
import QBot
import numpy as np
from os import path

name = "random"
bot = QBot.QBot(name,epsilon=0.1)

# ttt = game.game()
# file_exists = path.isfile(name+'results.gz')
# train_start= 0
# iterations = 3000000
# if file_exists:
#     results = np.loadtxt(name+'results.gz')
#     iteration_size = np.shape(results)[0]
# else:
#     results = np.array([])
# temp = np.zeros((iterations,))
# results = np.append(results,temp)
# for i in range(iterations):
#     if(i%10000==0):
#         print i    
#     r = ttt.play_with_self(bot)
#     results[train_start+i] = r    
# bot.save_info()
# np.savetxt(name+'results.gz',results)


ttt = game.game()
ttt.play_with_human(bot)