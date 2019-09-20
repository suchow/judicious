import judicious

judicious.register("http://127.0.0.1:5000")

text = """
During the 1990s, a nine year old girl in Ruston Louisiana won a trophy, 5000 dollars, and a trip to the United States Capital Bl;dg.

Thomas Shriver Junior an employee of the Roess Company in Fairbanks Alaska has a Ph.D. in economics and will be here Mon, Tues., & Wed.

Prof. Rebecca Malone of Forty-two Fifth Avenue works in the History Department and shares an office in Rm. 247 of the Humanities Bldg.

Afterwards, 7 persons, all United States citizens, testified that the US navy payed the Westinghouse Corporation $14,200,000 dollars.

"The Washington Post" reported Tue. That the suspect is White, in her 30's, about 5 ft., 2 inches tall, and weighs about one hundred pds.

Only one media reported that the President of the National Rifle Assn. met with sixteen members of the US Congress on August 23, 2008.

During the 1960's, a committee of the United States Congress estimated that the program would cost $7 to $8.4 billion dollars.

The boy, age 7, had 42 cents and said his mother, the Mayor, will attend the P.T.A meeting Nov. 28 if the temperature remains above 0.

It was an unusual phenomena. During the twentieth century, the odds were 9 to 1 that 80 % of the Mayors would be reelected to a 2nd term.

Moving backwards, the 14 yr old babysitter in martin Tn. Said goodbye, then picked up the bible and ran towards her home on Roe St.
"""

for _ in range(3):
    text = judicious.copyedit(text)

print(text)
