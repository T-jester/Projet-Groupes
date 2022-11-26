import numpy as np
from typing import Any, Tuple
from numpy.typing import NDArray


Cayley_Table = NDArray[np.int64]

#TODO: pretty printer

class Magma:

    def __init__(self, loi: Cayley_Table) -> None:
        n, m = loi.shape
        self.cardinal = n
        self.loi = loi


    def update_neutre(self) -> None:
        """ Recherche l'élément neutre """
        if not hasattr(self, "has_neutre"):
            for i in range(self.cardinal) :
                for j in range(self.cardinal):
                    if self.loi[i, j] != j or self.loi[i, j] != self.loi[j, i]:
                        break
                else:
                    self.neutre = i
                    self.has_neutre = True
                    return
        self.has_neutre = False


    def update_assoc(self) -> None:
        """ Vérifier si la loi est associative """
        if not hasattr(self, "is_assoc"):
            for i in range(self.cardinal):
                for j in range(self.cardinal):
                    element_gauche = self.loi[i, j]
                    for k in range(self.cardinal):
                        element_droite = self.loi[j, k]
                        if self.loi[element_gauche, k] != self.loi[i, element_droite]:
                            self.is_assoc = False
                            return
            self.is_assoc = True


    def update_commutatif(self) -> None:
        """ Vérifier si la loi est commutative"""
        # Deux éléments commutent ssi loi[i,j]== loi[j,i]
        if not hasattr(self, "is_comm"):
            for i in range(self.cardinal) :
                for j in range(i+1,self.cardinal) :
                    if self.loi[i,j] != self.loi[j,i] :
                        self.is_comm = False
                        return
            self.is_comm = True

    def update_inverse(self) -> None:
        """ Vérifier si tout élément admet un inverse """
        if not hasattr(self, "has_inverse"):
            if not self.has_neutre:
                has_inverse = False
                return
            inverse_list = [-1]*self.cardinal
            for i in range(self.cardinal):
                for potential_inverse in range(self.cardinal):
                    if self.loi[i, potential_inverse] == self.neutre and self.loi[potential_inverse, i] == self.neutre:
                        inverse_list[i] = potential_inverse
            if -1 in inverse_list:
                self.is_inverse = False
            else:
                self.is_inverse = True
            self.inverse = np.array(inverse_list)

    
    def rename(self,i,j) :
        """
        Echange le nom de deux éléments.
        Par exemple pour avoir l'élément neutre en 0.
        """
        I = np.eye(self.cardinal)
        I[i,i] = I[j,j] = 0
        I[i,j] = I[j,i] = 1
        # Changement de base
        self.loi = I.dot(self.loi.dot(I))
        # Pas vraiment optimal mais court et joli


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
    

class Monoide(Magma):

    def __init__(self, loi: Cayley_Table, neutre: int) -> None:
        super().__init__(loi)
        self.has_neutre = True
        self.neutre = neutre
        self.is_assoc = True

    @classmethod
    def upgrade_magma(cls, magma: Magma):
        if not hasattr(magma, "has_neutre") or not magma.has_neutre:
            return magma
        return cls(magma.loi, magma.neutre)



class Groupe(Monoide):

    def __init__(self, loi: Cayley_Table, neutre: int, inverse: NDArray[np.int64]) -> None:
        super().__init__(loi, neutre)
        self.has_inverse = True
        self.inverse = inverse


    @classmethod
    def upgrade_monoide(cls, monoide: Monoide):
        if not hasattr(monoide, "is_inverse") or not monoide.is_inverse:
            return monoide
        return cls(monoide.loi, monoide.neutre, monoide.inverse)

    #TODO: test this function
    def is_gen(self,k) :
        """
        Renvoie True si le groupe est cyclique et est engendré par k.
        """
        if hasattr(self, "has_gen"):
            # Un élément se répète ssi k n'est pas générateur
            temp = sorted(self.loi[k])
            for i in range(self.cardinal-1) :
                if temp[i] == temp[i+1] :
                    return False
            return True

    #TODO: test this function
    def centre(self) :
        rez = []
        for i in range(self.cardinal) :
            commute = True
            for j in range(self.cardinal) :
                if self.loi[i,j] != self.loi[j,i] :
                    commute = False
                    break

            if commute :
                rez.append(i)
        return rez

    #TODO: test this function
    def possibilites(self, elem, n) :
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

    