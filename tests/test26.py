import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

src = "https://s3-us-west-1.amazonaws.com/dlgr-faces/a50682accd4d9fb51cf2cbd8f450c0581e471d55d06673d0072c63b8bb3f1ff1.png"
ranks = judicious.rank_the(
    category=
    "Barack Obama as depicted in <img src='https://s3-us-west-1.amazonaws.com/dlgr-faces/obama.jpg' width='64' />",
    srcs=[src, src, src, src])

print(ranks)

rankings = judicious.map(
    judicious.rank_the,
    [("hello", [src, src, src, src]) for _ in range(3)]
)

print(rankings)
