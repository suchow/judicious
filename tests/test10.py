import random

import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

levels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] * 10
random.shuffle(levels)

results = []
for i, level in enumerate(levels):
    results.append(judicious.compare_numerosity(level, 100 - level))

print(results)
