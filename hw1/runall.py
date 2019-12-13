import os
import math

XO = "ps"
step = 50

for ell in range(50, 501, 50):
    nInitial = int(4*ell*(math.log(ell)+1))
    command = "sga-c++/sga {} {} 2 0.75 0 -1 -1 50".format(ell, nInitial)
    print(command)
    output = os.popen(command).read()
    
    filename = "output/05/" + XO + "{}.csv".format(ell)
    with open(filename, "w") as f:
        f.write(output)