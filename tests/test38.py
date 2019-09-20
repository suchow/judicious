import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")

(letter, correct) = judicious.identify_letter(alphabet=["C", "D"], lightness=0.80)
print((letter, correct))
