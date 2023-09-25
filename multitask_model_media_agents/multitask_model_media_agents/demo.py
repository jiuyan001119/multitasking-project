import numpy as np
from matplotlib import pyplot as plt
from random import randint

iterations = 1000000
x = np.arange(iterations)
y = np.zeros(iterations)

for i in range(iterations):
    result = 0
    while True:
        pick = randint(1,3)
        if pick == 1:
            result += 3
            break
        elif pick == 2:
            result += 3
        else:
            result += 5
    y[i]=result
print(sum(y)/iterations)
plt.scatter(x,y, s=0.1, color = 'g', marker = 'o')
plt.xlabel("Times of iterations")
plt.ylabel("Total time")
plt.show()