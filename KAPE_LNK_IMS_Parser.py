import pandas as pd

# Import the LNK File 

filepath = input('Enter filepath name: ')
df = pd.read_csv(filepath)

dfs=[]

# Generate the IMS Columns 
hostip = input("Do you know the IP Address? Enter it if you do:   ")
#hostname = input("What is the hostname of the machine?  ")

dfs = df.filter(['SourceCreated', 'MachineID', 'SourceFile', 'TargetIDAbsolutePath'])

#dfs["SourceCreated"]=
dfs["EventName"]="LNK:SourceCreated"
#dfs["Host"]= hostname
dfs['IP']= hostip
dfs["Assessment"]=""
dfs["EventCategory"]="File Folder Access"
dfs["Dest_IP"]=''
dfs["Hash"]=""
dfs["AddedBy"] = "Tony"
dfs["Date"] = pd.to_datetime('today').strftime("%Y-%m-%d")
dfs.rename(columns={'SourceCreated': 'EventTime', 'MachineID': 'Host', 
                    'Source': 'Evidence Description', 
                    'TargetIDAbsolutePath': 'Path'}, inplace=True)


dfs = dfs[['EventTime','EventName', 'Host', 'IP', 'Assessment', 'EventCategory',
            'Path', 'Dest_IP', 'Hash', 'AddedBy','Date']]
dfs.rename(columns={'FirstInteracted': 'DateTime','Value': "Examiner's Comments", 'AbsolutePath': 'Path'}, inplace=True)


dfs.to_excel("LNK_IMSformatted.xlsx", index=False)
