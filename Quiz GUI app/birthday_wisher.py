import datetime
import pandas as pd
import random

today = datetime.datetime.now()
today_tuple = (today.month,today.day)

data = pd.read_csv("birthdays.csv")
data_dict = {(birth_data["month"],birth_data["day"]): birth_data for (index,birth_data) in data.iterrows()}
if today_tuple in data_dict:
    person = data_dict[today_tuple]
    letter_path = f'letter_templates/letter_{random.randint(1,3)}.txt'
    with open(letter_path,"r") as letter:
        contents = letter.read()
        contents = contents.replace("[NAME]",person["name"])
        print(contents) 
