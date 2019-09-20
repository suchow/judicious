import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

move = judicious.tic_tac_toe([])

print(move)
