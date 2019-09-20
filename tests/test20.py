import math

import judicious

judicious.register("http://127.0.0.1:5000")

# judicious.register("https://imprudent.herokuapp.com")


def f(x):
    return 50.5 + 49.5 * math.sin(math.pi / 2 + x / (5 * math.pi))


summary = judicious.learn_function(f, num_trials=10)

print(summary)
