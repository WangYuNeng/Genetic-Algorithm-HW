from Group import Group

class IterationMgr:
    def __init__(self, popu):
        self.grps = [Group(i, i, True, popu[:, i]) for i in range(popu.shape[1])]
        for grp in self.grps:
            grp.calc_description_length()
        self.name_to_group = {}
        self.ite = 0

    def step(self):
        self.ite += 1
        best_group = None
        best_diff = 0
        for i in range(len(self.grps)):
            for j in range(i+1, len(self.grps)):
                g1, g2 = self.grps[i], self.grps[j]
                name = "({}+{})".format(g1.name, g2.name)
                if name not in self.name_to_group:
                    new_group = Group(g1, g2)
                    new_group.calc_description_length()
                    self.name_to_group[name] = new_group
                cur_group = self.name_to_group[name]
                print(name, cur_group.D_Diff)
                if cur_group.D_Diff < best_diff:
                    best_diff = cur_group.D_Diff
                    best_group = cur_group

        if best_group is None:
            return False
        else:
            self.grps.remove(best_group.g1)
            self.grps.remove(best_group.g2)
            self.grps.append(best_group)
            return True
    
    def log(self):
        print(self.ite, ":")
        description_length = 0
        for grp in self.grps:
            print(grp.name, end=" ")
            description_length += grp.D_Data + grp.D_Model
        print("Description Length={}".format(description_length))
    
    def dump(self, filename):
        with open(filename, "w") as f:
            f.write("%d\n" % (len(self.grps)))
            for grp in self.grps:
                f.write("%d" % (grp.BB_length))
                grp.write_file(f)
                f.write("\n")
