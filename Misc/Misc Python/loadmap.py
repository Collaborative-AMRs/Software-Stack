'''
from PIL import Image
import numpy as np
from numpy import asarray


image = Image.open('arena.png')

data = asarray(image)
print(type(data))

print(data.shape)

image2 = Image.fromarray(data)
print(type(image2))


print(image2.mode)
print(image2.size)
np.save('data.npy', data)
print(data)
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
grid = np.load('map.npy')
grid = grid.astype(int)

plt.imshow(grid)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


print(grid)
