import judicious as j

# BASE_URL = "http://imprudent.herokuapp.com"
BASE_URL = "http://127.0.0.1:5000"

j.register(BASE_URL)

r = j.collect("joke")
print(r)
