class Allist_:
    def __init__(self, left, right, valuespace):
        self.all_list = left + right
        self.all_ = {}
        self.valuespace = valuespace
        for species in self.all_list:
            self.all_[species] = self.valuespace[species]
        self.all_key = self.all_.keys()
        self.all_value = self.all_.values()

valuespace1 = {'cl2' : 1.0e-14, 'hocl' : 3.30e-5, 'cl2o' : 1.0e-14, 'cl_' : 1.0e-14, 'cl3_' : 1.0e-14, 'ocl_' : 1.0e-14, 'br2' : 1.0e-14, 'hobr' : 1.0e-14, 'br2o' : 1.0e-14, 'br_' : 3.47e-5, 'br3_' : 1.0e-14, 'obr_' : 1.0e-14,'brcl' : 1.0e-14, 'br2cl_' : 1.0e-14, 'brcl2_' : 1.0e-14, 'brocl' : 1.0e-14,'hp' : 1.00e-7, 'oh_' : 1.00e-7, 'nap' : 1.07e-3}
left1 = ['hocl', 'br_']
right1 = ['hobr', 'cl_']
LIST1 = Allist_(left1, right1, valuespace1)
print(LIST1.all_value)
print(LIST1.all_key)
print(LIST1.all_)



