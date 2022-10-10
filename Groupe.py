import numpy as np


class Monoid (object) :

    def __init__(self, n, f_trans = None, t_trans = None) :

        self.n = n

        if not f_trans is None :
            self.loi = np.array([[f_trans(a,b) for a in range(n)] for b in range(n)])

        elif not t_trans is None :
            self.loi = t_trans

        else :
            self.loi = np.zeros((n,n), dtype = int)

class Group (Monoid) :
    """
    On cherche à automatiser quelques opérations
    sur les groupes (finis dans un premier temps)
    """

    def __init__(self, n, f_trans = None, t_trans = None) :

        super().__init__(n, f_trans, t_trans)




    def is_gen(self,k) :
        # Un élément se répète ssi k n'est pas générateur
        temp = sorted(self.loi[k])
        for i in range(self.n-1) :
            if temp[i] == temp[i+1] :

                return False
        return True












