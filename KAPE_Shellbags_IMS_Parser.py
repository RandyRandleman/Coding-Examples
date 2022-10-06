import pandas as pd 

# Import the File
filepath = input('Enter filepath or filename name: ')
df = pd.read_csv(filepath)

# Create the 3 DataFrames 

dfs=[]
dfs1=[]
dfs2=[]

# Generate the IMS Columns 
user = input('What is the Username of the shellbags output?:    ')
hostip = input("Do you know the IP Address? Enter it if you do:   ")
hostname = input("What is the hostname of the machine?  ")

# Generate for FirstInteraction 

dfs1 = df.filter(['AbsolutePath', 'Value', 'FirstInteracted',]) # maybe add HasExplored
dfs1["User"]= user 
dfs1["Host"] = hostname
dfs1['EventName']= 'Shellbags:FirstInteracted'
dfs1['IP']= hostip 
dfs1["Assessment"]=''
dfs1["EventCategory"]="File Folder Access"
dfs1["Dest_IP"]=''
dfs1["Hash"]=''
dfs1["AddedBy"] = "Tony"
dfs1["Date"] = pd.to_datetime('today').strftime("%Y-%m-%d")
dfs1 = dfs1[['FirstInteracted', 'EventName', 'Host', 'User', 'IP', 'Assessment', 'EventCategory',
            'AbsolutePath', 'Value', 'Dest_IP', 'Hash', 'AddedBy','Date']]
dfs1.rename(columns={'FirstInteracted': 'DateTime','Value': "Examiner's Comments", 'AbsolutePath': 'Path'}, inplace=True)

# Generate for LastInteraction

dfs2 = df.filter(['AbsolutePath', 'Value', 'LastInteracted', 'HasExplored'])
dfs2["User"] = user
dfs2["Host"] = hostname
dfs2['EventName'] = 'Shellbags:LastInteracted'
dfs2['IP'] = hostip
dfs2["Assessment"] = ''
dfs2["EventCategory"] = "File Folder Access"
dfs2["Dest_IP"] = ''
dfs2["Hash"] = ''
dfs2["AddedBy"] = "Tony"
dfs2["Date"] = pd.to_datetime('today').strftime("%Y-%m-%d")
dfs2 = dfs2[['LastInteracted', 'EventName', 'Host', 'User', 'IP', 'Assessment', 'EventCategory',
            'AbsolutePath', 'Value', 'Dest_IP', 'Hash', 'AddedBy','Date']]
dfs2.rename(columns={'LastInteracted': 'DateTime','Value': "Examiner's Comments", 'AbsolutePath': 'Path'}, inplace=True)

# Generate the IMS 

dfs1 = dfs1[dfs1['DateTime'].notna()]
dfs2 = dfs2[dfs2['DateTime'].notna()]

dfinal = pd.concat([dfs1, dfs2])

# Keyword Searching 

# Dictionaries for Assessment Column 
keywords = ["KAPE", "EZParser", "Github", "chainsaw"]

dfinal['keyword'] = dfinal["Examiner's Comments"].str.findall('|'.join(keywords)).apply(set).str.join(', ')

for keyword in keywords:
    dfinal[keyword] = dfinal["Examiner's Comments"].str.contains(keyword)

# Fill in Assessment based on the Keywords

dfinal.loc[dfinal.keyword != "", 'Assessment'] = 'Suspicious'

# Output 
dfinal.to_excel("Shellbags_IMSformatted.xlsx", index=False)
