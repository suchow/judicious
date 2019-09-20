import judicious

from multiprocessing import Pool

judicious.register("http://127.0.0.1:5000")

judicious.seed("7bd60c63-a334-c6ca-429f-beae6b094ec3")

results = judicious.map(judicious.joke, [None for _ in range(3)])
print(results)
