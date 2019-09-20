import judicious

# judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

scenario = "A drug cartel has hidden 1 kilogram of cocaine somewhere on the person or in the luggage of a passenger on a commercial flight. Where do you think the cocaine might be hidden?"
response = judicious.redact_illicit(scenario)
