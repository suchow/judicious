import judicious
import pandas as pd
import random


def causal_inference_test():
    with judicious.Person(lifetime=6000) as person:
        df = pd.read_csv("https://causalimg.s3.amazonaws.com/causal_story_img.csv")
        faceA_list = df['image1'].tolist()
        faceB_list = df['image2'].tolist()
        generative = df['generative'].tolist()
        preventative = df['preventative'].tolist()
        for i in range(len(faceA_list)):
            initial_judgment = person.matching_confidence(faceA_list[i], faceB_list[i])
        rndm = [True,False]
        c = random.choice(rndm)
        if c==True:
            for i in range(len(faceA_list)):
                gen_judgement = person.matching_confidence_with_cause(faceA_list[i], faceB_list[i], generative[i])
                print(gen_judgement)
        else:
            for i in range(len(faceA_list)):
                prev_judgement = person.matching_confidence_with_cause(faceA_list[i], faceB_list[i], preventative[i])
                print(prev_judgement)

judicious.map3(causal_inference_test, [_ for _ in range(3)])
