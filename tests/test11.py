import judicious

judicious.register("http://127.0.0.1:5000")


for i in range(20):
    agreement = judicious.agree("I enjoy answering questions.")
    print(agreement)
