import judicious

# judicious.register("http://127.0.0.1:5000")
judicious.register("https://imprudent.herokuapp.com")
# judicious.seed(2938472374293847239874)

src = "https://images.unsplash.com/photo-1489069313310-63735a4f3010"

label = judicious.core.post_task("label", parameters={"src": src})

print(label)
