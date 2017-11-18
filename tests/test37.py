import judicious

src = "http://www.newyorker.com/wp-content/uploads/2017/11/171120_contest-690.jpg"
judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

caption = judicious.caption(src)
