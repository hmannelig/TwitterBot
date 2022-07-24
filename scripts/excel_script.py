import pandas as pd

excel_data = pd.read_excel("resources\@Alm0hada_user_tweets.xlsx")

data = pd.DataFrame(excel_data, columns=['Text'])

data.to_csv('lmohada.txt', sep=' ')