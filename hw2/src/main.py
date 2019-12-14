from IterationMgr import IterationMgr
import sys
import os
import numpy as np
from LabClient import LabClient

population_dir = "../population/"
mpm_dir = "../mpm/"
input_file = "../population/popu"
output_file = "../mpm/mpm"

if __name__ == "__main__":
    client = LabClient(sys.argv[1], "B05901025")
    for geneation in range(1000):
        population_filename = "popu"+str(geneation).zfill(3)+".txt"
        mpm_filename = "mpm"+str(geneation).zfill(3)+".txt"

        client.get_population(population_filename, population_dir)

        with open(os.path.join(population_dir, population_filename)) as f:
            population = np.array([[int(bit) for bit in line[:-1]] for line in f])
        
        mgr = IterationMgr(popu=population)
        while mgr.step():
            pass
        mgr.dump(os.path.join(mpm_dir, mpm_filename))

        max_fitness = client.post_mpm(os.path.join(mpm_dir, mpm_filename), geneation)
        print('%d: %lf' % (geneation, max_fitness))
        if max_fitness == 100:
            break
