import structures


def is_intern(loi: structures.Cayley_Table) -> bool:
    """ Renvoie True si la loi est interne """
    n, m = loi.shape
    if n != m :
        return False
    for i in range(n) :
        for j in range(n) :
            if loi[i,j] < 0 or loi[i,j] >= n :
                return False
    return True

def enrichissement(loi: structures.Cayley_Table):
    """ Renvoie un objet qui munit la loi de la structure ayant le plus de propriétés algébriques """
    if not is_intern(loi):
        return loi
    magma = structures.Magma(loi)
    magma.update_neutre()
    magma.update_assoc()
    if magma.has_neutre and magma.is_assoc:
        monoide = structures.Monoide.upgrade_magma(magma)
        monoide.update_inverse()
        if monoide.is_inverse:
            groupe = structures.Groupe.upgrade_monoide(monoide)  # type: ignore
            return groupe
        return monoide
    return magma

#TODO: Génération rapide de groupes