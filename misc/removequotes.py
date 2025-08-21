import pandas as pd


df = pd.read_csv("GQVis_Single_Query.csv")
print(df.head(5))
#df.drop(',', axis=1, inplace=True)
#df.drop('Unnamed: 0', axis=1, inplace=True)

#df.to_csv("GQVis_Single_Query.csv")