import judicious

# Afterwards, 7 persons, all United States citizens, testified that the US navy payed the Westinghouse Corporation $14,200,000 dollars.
# Seven United States citizens testified that the US Navy paid the Westinghouse Corporation 14.2 million dollars.
# Seven United States citizens testified that the US Navy paid the Westinghouse Corporation 14.2 million dollars.
# 7 US citizens testified that the US Navy paid the Westinghouse Corporation 14.2 million dollars.
# 7 US citizens testified that the US Navy paid the Westinghouse Corporation 14.2 million dollars.
# Seven U.S. citizens testified that the U.S. Navy paid the Westinghouse Corporation 14.2 million dollars.

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

text = "Afterwards, 7 persons, all United States citizens, testified that the US navy payed the Westinghouse Corporation $14,200,000 dollars."

for _ in range(2):
    text = judicious.spellcheck(text)
    print(text)
