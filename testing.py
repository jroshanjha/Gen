import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt

x = np.random.randint(0,100)
y = np.random.randint(0,100)

plt.figure(figsize=(5,10))

# sns.lineplot([x, y])
plt.plot(x,y,color='pink')
plt.title('Random distribution')
plt.xlabel("X position")
plt.ylabel("Y position")
plt.show()
