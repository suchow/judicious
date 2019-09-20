import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

valid = judicious.prosewash(
    text="A very unique text",
    error_message="This is an error message",
)

print(valid)
