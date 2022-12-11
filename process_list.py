import os
import subprocess
import pandas as pd
#cmd = "top -b -n 3 | sed -n '7,1{s/^ *//;s/ *$//;s/  */;/gp;};1q' > out.csv"
#os.system(cmd)
cmd = "top -b -n 3 | sed -n '7, 50{s/^ *//;s/ *$//;s/  */;/gp;};50q' > out.csv"

os.system(cmd)

command_data = subprocess.run("top -b -n 1 | sed -n '7, 50{s/^ *//;s/ *$//;s/  */;/gp;};50q'", shell=True, capture_output=True).stdout.decode().strip()

columns = command_data.split("\n")[0].split(";")
rows = command_data[command_data.index("\n")+1:]

dataframe = pd.DataFrame([row.split(";") for row in rows.split('\n')], columns=columns)

print (columns)
print(rows)

print(dataframe)

