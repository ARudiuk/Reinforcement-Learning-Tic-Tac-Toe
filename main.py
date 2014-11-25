import game
import QBot
import numpy as np
from os import path

name = "test"
bot = QBot.QBot(name)
ttt = game.game()
file_exists = path.isfile(name+'results'+'.npy')
if file_exists:
    results = np.load(name+'results'+'.npy')
else:
    results = np.array([])
for i in range(100000):
    if(i%1000==0):
        print i
    r = ttt.play_with_self(bot)
    results = np.append(results,r)
bot.save_info()
np.save(name+'results',results)
np.savetxt(name+'results'+'.txt',results)


# ttt = game.game()
# ttt.play_with_human()