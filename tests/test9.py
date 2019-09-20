import judicious

from multiprocessing import Pool

judicious.register("http://127.0.0.1:5000")

# judicious.seed("1cf82c05-882e-4f8a-935f-2f551ac4daba")

pool = Pool(20)

results = pool.map(judicious.joke, [None for _ in range(20)])

print(results)
