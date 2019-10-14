import judicious

# judicious.register("https://imprudent.herokuapp.com")
# judicious.seed("cc722bf6-e319-cf63-a671-cbae64dfd40f")


def experiment():
    with judicious.Person(lifetime=60) as person:
        if not person.consent():
            return None
        j1 = person.joke()
        j2 = person.joke()
        j3 = person.joke()
        j4 = person.joke()
        person.complete()
        return (j1, j2, j3, j4)


results = judicious.map3(experiment, [None for _ in range(1)])
print(results)
