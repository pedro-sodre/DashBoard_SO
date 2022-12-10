import os
#cmd = "top -b -n 3 | sed -n '7,1{s/^ *//;s/ *$//;s/  */;/gp;};1q' > out.csv"
#os.system(cmd)
cmd = "top -b -n 3 | sed -n '7, 50{s/^ *//;s/ *$//;s/  */;/gp;};50q' > out.csv"

os.system(cmd)