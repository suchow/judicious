import judicious
import numpy as np
import random
import pandas as pd

pre_results = []
post_results = []
training_results = []
def merge(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

def get_numbers():
    df3 = pd.read_csv('https://glassgow.s3.amazonaws.com/csv/numbers.csv')
    df4 = df3[['number1', 'number2']]
    df5 = df4.sample(n=7)
    numberlist1 = []
    numberlist2 = []
    for index, row in df5.iterrows():
        number1 = (row['number1'])
        number2 = (row['number2'])
        numberlist1.append(number1)
        numberlist2.append(number2)
    n = merge(numberlist1,numberlist2)
    return n

def get_faces():
    df1_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv/face_url.csv')
    df2_face = df1_face[['face1','face2']]
    df3_face = df2_face.sample(n=40)
    face1_list = []
    face2_list = []
    face_list = []
    for index, row in df3_face.iterrows():
        face1 = (row['face1'])
        face2 = (row['face2'])
        face1_list.append(face1)
        face2_list.append(face2)
    b = merge(face1_list,face2_list)
    return b

def face_training(number):
    if number == 1:
        df_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv_folder/30_short_gfmt_training.csv')
    elif number == 2:
        df_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv_folder/37_short_gfmt_training.csv')
    elif number == 3:
        df_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv_folder/44_short_gfmt_training.csv')
    elif number == 4:
        df_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv_folder/51_short_gfmt_training.csv')
    elif number == 5:
        df_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv_folder/58_short_gfmt_training.csv')
    elif number == 6:
        df_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv_folder/65_short_gfmt_training.csv')
    elif number == 7:
        df_face = pd.read_csv('https://glassgow.s3.amazonaws.com/csv/face_url%2B2%2B(1)%2B(4)%2B(2).csv')
    else:
        return None
    df_face1 = df_face[['face1','face2']]
    df2_face = df_face1.sample(n=40)
    train_face_list1 = []
    train_face_list2 = []
    for index, row in df2_face.iterrows():
        face1 = (row['face1'])
        face2 = (row['face2'])
        train_face_list1.append(face1)
        train_face_list2.append(face2)
    face_set = merge(train_face_list1, train_face_list2)
    return face_set

pre_post_faces = get_faces()

def pre_post_gfmt(a,b):
    with judicious.Person(lifetime=900) as person:
        math_numbers = get_numbers()
        random.shuffle(pre_post_faces)
        random.shuffle(math_numbers)
        number = random.choice([1,2,3,4,5,6,7,8])
        training_face_set = face_training(number)
        random.shuffle(training_face_set)
        for i in pre_post_faces:
            face1 = i[0]
            face2 = i[1]
            p = person.match_faces_no_feedback(face1,face2)
            pre_results.append(p)
        for i in math_numbers:
            print(math_numbers)
            number1 = i[0]
            number2 = i[1]
            m = person.multiply(number1,number2)
        if number==8:
            for i in math_numbers:
                number1 = i[0]
                number2 = i[1]
                u = person.multiply(number1,number2)
        else:
            for i in training_face_set:
                face1 = i[0]
                face2 = i[1]
                b = person.match_faces_feedback(face1,face2)
                training_results.append(b)
        for i in math_numbers:
            number1 = i[0]
            number2 = i[1]
            c = person.multiply(number1,number2)
        for i in pre_post_faces:
            face1= i[0]
            face2 = i[1]
            d = person.match_faces_no_feedback(face1,face2)
            post_results.append(d)



judicious.map3(pre_post_gfmt, pre_post_faces)

print(pre_results,post_results, training_results)
