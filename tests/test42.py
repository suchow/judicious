
import judicious

# judicious.register("http://127.0.0.1:5000")
judicious.register("https://imprudent.herokuapp.com")

r = judicious.chat("Talk about the weather.", N=10)
print(r)
