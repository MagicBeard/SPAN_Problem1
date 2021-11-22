import os
import pandas as pd

#Retrieve path:
dir_path = os.path.dirname(os.path.realpath(__file__))

#Ask user for input file name:
print ("Please make sure the input file is in the same directory as this script.")
print ("Enter the input text file name with extension:")
inputFilePath = dir_path + "\\" + input()

#Opening txt file:

df_input=pd.read_csv(inputFilePath, sep=',',header =None,names=['Line1','Line2'])

#Ditermining number of lines:
line_count = len(df_input)

#Seperating values:
df = pd.DataFrame()
df['Team name 1'] = df_input['Line1'].str.replace('\d+', '', regex=True).str.strip()
df['Team 1 score'] = df_input['Line1'].str.replace('\D+', '', regex=True).str.strip()
df['Team 1 score'] = pd.to_numeric(df['Team 1 score'])
df['Team name 2'] = df_input['Line2'].str.replace('\d+', '', regex=True).str.strip()
df['Team 2 score'] = df_input['Line2'].str.replace('\D+', '', regex=True).str.strip()
df['Team 2 score'] = pd.to_numeric(df['Team 2 score'])

#Create dataframe for results:
df2 = pd.DataFrame(columns = ['Team Name', 'Points'])

for i in range(line_count):
    if df.at[i, "Team 1 score"] > df.at[i, "Team 2 score"]:
        entry1 = {'Team Name': df.at[i, "Team name 1"], 'Points': 3}
        df2 = df2.append(entry1, ignore_index = True)
        

    elif df.at[i, "Team 1 score"] < df.at[i, "Team 2 score"]:
        entry1 = {'Team Name': df.at[i, "Team name 2"], 'Points': 3}
        df2 = df2.append(entry1, ignore_index = True)

    elif df.at[i, "Team 1 score"] == df.at[i, "Team 2 score"]:
        entry1 = {'Team Name': df.at[i, "Team name 1"], 'Points': 1}
        entry2 = {'Team Name': df.at[i, "Team name 2"], 'Points': 1}
        df2 = df2.append(entry1, ignore_index = True)
        df2 = df2.append(entry2, ignore_index = True)

df2['Points'] = pd.to_numeric(df2['Points'])

#Pivot and sort the results:
df3 = pd.pivot_table(df2, index = 'Team Name', values=['Points', 'Team Name'],aggfunc='sum',)
df3['Team Name'] = df3.index
df3=df3.reset_index(drop=True)
df3 = df3[['Team Name', 'Points']]

df3.sort_values(['Points', 'Team Name'],ascending=[False, True], inplace= True)
df3=df3.reset_index(drop=True)

#Add positions:
line_count2 = len(df3)

for i in range (len(df3)):
    df3.iloc[i, 0] = str(i+1) + ". " + str(df3.iloc[i, 0])

#Output:
df3.to_csv(dir_path + "\\" + 'OutputFile.csv', sep = ',', header = False, index = False)
print ('The results have been saved in an output file in the same directory as the input file.')