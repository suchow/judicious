import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")
judicious.seed("d539def9-1524-4e01-844f-8852c0232518")

# response = judicious.build_tower(prompt)
N = 2

tower_imgs = []
for i in range(N):
    person = judicious.Person()
    prompt = "Build a tower that (a) uses all the blocks, (b) has only one block touching the ground, and (c) is as wide as possible."
    tower_img = person.build_tower(prompt)
    with open("towers.html", "a+") as f:
        f.write("<img src='{}' width='200' />".format(tower_img))
