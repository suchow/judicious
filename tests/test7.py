import judicious

# judicious.priority(0)
# judicious.register("http://127.0.0.1:5000")
judicious.register("https://imprudent.herokuapp.com")

judicious.priority(0)

words = [
    "bibulous",
    "captious",
    "embonpoint",
    "hypnopompic",
    "opsimath",
    "pule",
    "uxoricide",
    "valetudinarian",
    "legerdemain",
    "tricorn",
]

for word in words:
    definition = judicious.core.post_task("define", parameters={"word": word})

print(definition)
