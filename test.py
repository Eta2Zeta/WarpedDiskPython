import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6])
indices = np.where(arr > 3)
print(type(indices[0]))
print(indices[0])  # Output: (array([3, 4, 5]),)
