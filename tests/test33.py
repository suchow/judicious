import random
import numpy as np

import judicious

print(judicious.context())
print(random.random())
print(np.random.random())

judicious.seed("20fe55ec-0e74-368e-88cb-9fe118920c84")
print(judicious.context())
print(random.random())
print(np.random.random())
