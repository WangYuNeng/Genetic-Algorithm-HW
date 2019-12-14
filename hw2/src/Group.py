import numpy as np

class Group:
    def __init__(self, g1, g2, is_basic=False, genes=None):
        '''
        Recursively construct group with subgroup g1 and g2
        '''
        self.is_basic = is_basic
        if self.is_basic:
            '''
            basic group: one gene
            '''
            self.name = str(g1)
            self.genes = genes
            self.BB_length = 1
            self.popu_size = genes.shape[0]
        else:
            self.name = "({}+{})".format(g1.name, g2.name)
            self.g1 = g1
            self.g2 = g2
            self.BB_length = g1.BB_length + g2.BB_length
            self.popu_size = self.g1.popu_size
        self.gene_types = None
        self.D_Model, self.D_Data, self.D_Diff = None, None, None

    def calc_description_length(self):
        self.__count_gene_types__()
        self.D_Model = (2 ** self.BB_length - 1) * np.log2(self.popu_size)
        genetype_to_count = {}
        for genetype in self.gene_types:
            if genetype in genetype_to_count:
                genetype_to_count[genetype] += 1
            else:
                genetype_to_count[genetype] = 1
        self.D_Data = 0
        for genetype in genetype_to_count:
            # popu_size are cancel out
            self.D_Data += -genetype_to_count[genetype] * np.log2(genetype_to_count[genetype] / self.popu_size)
        if  not self.is_basic:
            self.D_Diff = self.D_Model + self.D_Data - self.g1.D_Model - self.g1.D_Data - self.g2.D_Model - self.g2.D_Data
            
    def write_file(self, file):
        if self.is_basic:
            file.write(" %s" % (self.name))
        else:
            self.g1.write_file(file)
            self.g2.write_file(file)

    def __count_gene_types__(self):
        if self.is_basic:
            self.gene_types = np.array([val for val in self.genes])
        else:
            self.gene_types = self.g1.gene_types * (2 ** self.g2.BB_length) + self.g2.gene_types

