from IterationMgr import IterationMgr
import sys
import os
from shutil import copyfile
import numpy as np
from LabClient import LabClient

population_dir = "../population/"
mpm_dir = "../mpm/"
input_file = "../population/popu"
output_file = "../mpm/mpm"

if __name__ == "__main__":
    client = LabClient(sys.argv[1], "B05901025")
    with open(os.path.join(mpm_dir, "init.txt"), "r") as f:
        best_num_group = int(f.readline())

    for geneation in range(1000):
        population_filename = "popu"+str(geneation).zfill(3)+".txt"
        mpm_filename = "mpm"+str(geneation).zfill(3)+".txt"

        client.get_population(population_filename, population_dir)

        with open(os.path.join(population_dir, population_filename)) as f:
            population = np.array([[int(bit) for bit in line[:-1]] for line in f])
        
        mgr = IterationMgr(popu=population)
        while mgr.step():
            pass

        if len(mgr.grps) >= best_num_group:
            max_fitness = client.post_mpm(os.path.join(mpm_dir, "init.txt"), geneation)
            copyfile(os.path.join(mpm_dir, "init.txt"), os.path.join(mpm_dir, mpm_filename))
            print('(post init) %d: %lf' % (geneation, max_fitness))
        else:
            mgr.dump(os.path.join(mpm_dir, mpm_filename))
            os.remove(os.path.join(mpm_dir, "init.txt"))
            copyfile(os.path.join(mpm_dir, mpm_filename), os.path.join(mpm_dir, "init.txt"))
            best_num_group = len(mgr.grps)
            max_fitness = client.post_mpm(os.path.join(mpm_dir, mpm_filename), geneation)
            print('(post dump) %d: %lf' % (geneation, max_fitness))
        if max_fitness == 100:
            break
