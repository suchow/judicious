import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

src = "https://s3-us-west-1.amazonaws.com/dlgr-faces/a50682accd4d9fb51cf2cbd8f450c0581e471d55d06673d0072c63b8bb3f1ff1.png"
dimorphism = judicious.dimorphism(src=src)

print(dimorphism)
