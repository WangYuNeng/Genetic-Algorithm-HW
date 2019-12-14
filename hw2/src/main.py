from IterationMgr import IterationMgr
import sys
import numpy as np

input_file = "../population/popu"
output_file = "../mpm/mpm"

if __name__ == "__main__":
    popu_num = sys.argv[1]
    input_file += popu_num.zfill(3) + ".txt"
    output_file += popu_num.zfill(3) + ".txt"
    with open(input_file) as f:
        population = np.array([[int(bit) for bit in line[:-1]] for line in f])
    mgr = IterationMgr(popu=population)
    mgr.log()
    while mgr.step():
        mgr.log()
    mgr.dump(output_file)
