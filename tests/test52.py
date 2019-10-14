import judicious

judicious.seed("cc722bf6-e319-cf63-a671-cbae64dfdb0f")

# 1 (complete): 3799aa89-ccae-c268-d0e8-cc4e9ddddee4
# 2 (timeout) : 4d30601d-dfe3-ee53-8594-7fc0aa8e68ec
# 3 (complete): fe07a885-53c3-9a22-c93e-91436e5d8f0c


# 1 (complete): 4f4d13ed-7d1c-cbee-638d-6aee5188c929
# 2 (timeout) : 720ebe41-5987-b9f0-b571-fd7fb50f2b05
# 3 (timeout) : 358e7d25-af92-8a18-23ec-49025aecc87b
# 4 (complete) : cab5c911-741c-8721-d851-483669940626

def experiment():
    with judicious.Person(lifetime=60) as person:
        j1 = person.joke()
        j2 = person.joke()
        j3 = person.joke()
        j4 = person.joke()
        person.complete()
        return [j1, j2, j3, j4]

results = judicious.map3(experiment, [None for _ in range(100)])
print(results)
