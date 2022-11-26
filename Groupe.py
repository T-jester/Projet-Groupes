import numpy as np


class Monoid (object) :

    def __init__(self, n, f_trans = None, t_trans = None) :

        self.n = n

        if not f_trans is None :
            self.loi = np.array([[f_trans(a,b) for a in range(n)] for b in range(n)])

        elif not t_trans is None :
            self.loi = np.array(t_trans)

        else :
            self.loi = np.zeros((n,n), dtype = int)



    def associativ(loi) :
        """ Renvoie True si la loi est associative """
        n = len(loi)
        for i in range(n) :
            for j in range(n) :
                for k in range(n) :
                    if loi[loi[i,j],k] != loi[i,loi[j,k]] :
                        return False, (i,j)
        return True



    def is_abelian(self) :
        """ Renvoie True si le groupe est commutatif """

        # Deux éléments commutent ssi loi[i,j]== loi[j,i]
        for i in range(self.n) :
            for j in range(i+1,self.n) :
                if self.loi[i,j] != self.loi[j,i] :
                    return False
        return True



    def neutre(self) :
        """ Recherche l'élément neutre """
        for i in range(self.n) :
            if self.loi[i,:].all() == self.loi[:,i].all() :
                return i
        raise Exception ("Pas d'élément neutre")


    def is_intern(loi) :
        """ Renvoie True si la loi est interne """
        n = len(loi)
        if n != len(loi[0]) :
            raise Exception (" Loi mal définie ")

        for i in range(n) :
            for j in range(n) :
                if loi[i,j] < 0 or loi[i,j] >= n :
                    return False
        return True


    def inv(self,i) :
        """ Renvoie l'inverse de l'élément i """
        for j in range(self.n) :
            if self.loi[i,j] == self.loi[j,i] == 1 :
                return j
        raise Exception ("Pas d'inverse")


    def is_group(self) :
        """ Renvoie True si loi de groupe """

        try :
            e = self.neutre()
        except :
            return False

        for i in range(self.n) :
            if i != e :
                has_inv = False
                for j in range(self.n) :
                    if j!= e :
                        if self.loi[i,j] < 0 or self.loi[i,j] >= self.n :
                            return False

                        if self.loi[i,j]==self.loi[j,i]==e :
                            has_inv = True

                        for k in range(self.n) :
                            try : # si self.loi[i,j] vérifie pas loi interne bug
                                if self.loi[self.loi[i,j],k] != self.loi[i,self.loi[j,k]] :
                                    return False
                            except :
                                return False

                if not has_inv :
                    return False
        return True

class Group (Monoid) :
    """
    On cherche à automatiser quelques opérations sur les groupes (finis dans un premier temps)
    """

    def __init__(self, n, f_trans = None, t_trans = None) :

        super().__init__(n, f_trans, t_trans)




    def is_gen(self,k) :
        """
        Renvoie True si le groupe est cycique et est engendré par k.
        """

        # Un élément se répète ssi k n'est pas générateur
        temp = sorted(self.loi[k])
        for i in range(self.n-1) :
            if temp[i] == temp[i+1] :

                return False
        return True



    def rename(self,i,j) :
        """
        Echange le nom de deux éléments.
        Par exemple pour avoir l'élément neutre en 0.
        """
        I = np.eye(self.n)
        I[i,i] = I[j,j] = 0
        I[i,j] = I[j,i] = 1
        # Changement de base
        self.loi = I.dot(self.loi.dot(I))
        # Pas vraiment optimal mais court et joli



    def centre(self) :
        rez = []
        for i in range(self.n) :
            commute = True
            for j in range(self.n) :
                if self.loi[i,j] != self.loi[j,i] :
                    commute = False
                    break

            if commute :
                rez.append(i)
        return rez



    def possibilites(elem, n) :
        """
        Renvoie la liste des mots de taille n possibles sur l'alphabet elem.
        """
        rez = []
        temp = [0]*n

        if elem is None :
            def aux(i,temp) :
                if i>=n :
                    return
                for e in (0,i) :
                    temp[i] = e
                    aux(i+1,temp)

        else :
            def aux(i,temp) :
                if i>=n :
                    return
                for e in elem :
                    temp[i] = e
                    aux(i+1,temp)

        aux(0,temp)
        return rez


    def produit(self, elem_list) :
        """ Renvoie le produit des éléments de elem_list """
        if len(elem_list) == 0 :
            return

        w = elem_list[0]
        k = 1
        while k<len(elem_list) :
            w = self.loi[w,elem_list[k]]
            k+=1
        return w








## Exemples :

g = Monoid(4)
g.loi = np.array([[0,1,2,3],
                  [1,3,2,1],
                  [2,2,2,2],
                  [3,1,2,0]])


g2 = Group(4)
g2.loi = np.array([[0,1,2,3],
                   [1,2,3,0],
                   [2,3,0,1],
                   [3,0,1,2]])










## Avec un truc déjà existant mais pas très dur à coder
# Montrer que le groupe A défini ci dessous est stable par conjugaison
from sympy.combinatorics.permutations import Permutation

A = [Permutation([], size = 5),
     Permutation([[0,1],[2,3]], size = 5),
     Permutation([[0,2],[1,3]], size = 5),
     Permutation([[0,3],[1,2]], size = 5)]

A5 = []
for i in range(5):
    for j in range(5) :
        for k in range(5):
            for l in range(5) :
                for m in range(5) :
                    # on vérifie que c'est une permutation
                    if len({i,j,k,l,m}) == 5:
                        a = Permutation([i,j,k,l,m], size = 5)
                        # on vérifie que c'est dans \mathfrac{A}_5
                        if a.signature() == 1:
                            A5.append(a)


for sigma in A5 :
    # on vérifie que sigma est dans G_x
    if sigma(4) == 4 :
        for a in A :
            prod = sigma*a*(sigma**(-1))
            if not prod in A:
                print(False)
print(True)
