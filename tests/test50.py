import judicious

judicious.register("http://127.0.0.1:5000")

results = judicious.map3(judicious.joke, [None for _ in range(3)])

print(results)
