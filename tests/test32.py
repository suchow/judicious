import judicious

# judicious.priority(0)
# judicious.register("http://127.0.0.1:5000")
judicious.register("https://imprudent.herokuapp.com")

judicious.priority(0)

for _ in range(100):
    judicious.core.post_task(
        "draw", parameters={
            "thing": "a sheep",
            "width": 200,
            "height": 200
        })
