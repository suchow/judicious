import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for _ in range(9):
    board = judicious.tictactoe(board=board)
    print(board)
