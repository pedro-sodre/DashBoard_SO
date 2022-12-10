import os
import time
#cmd = "top -b -n 3 | sed -n '7,1{s/^ *//;s/ *$//;s/  */;/gp;};1q' > out.csv"
#os.system(cmd)
i =0

while  i<=5:
    print("Rodando")
    cmd = "top -b -n 3 | sed -n '7, 50{s/^ *//;s/ *$//;s/  */;/gp;};50q' > out.csv"
    os.system(cmd)
    print("Completo")
    time.sleep(5)
