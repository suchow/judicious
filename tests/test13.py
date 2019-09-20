import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

decision = judicious.intertemporal_choice(SS=1, LL=2, delay="1 day")

print(decision)
