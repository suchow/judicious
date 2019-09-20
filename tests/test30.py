import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

# judicious.seed("c0d87a56-601d-2018-168b-85d8c5581f18")

print(judicious.draw("a sheep", width=200, height=200))

# def feed(transformer, state, n):
#     if n == 0:
#         return state
#     else:
#         return feed(transformer, transformer(state), n - 1)
