import numpy as np
import generation


# Quelle est la structure donnée par la loi suivante?
loi = np.array([[0,1,2,3],
                [1,3,2,1],
                [2,2,2,2],
                [3,1,2,0]])


structure = generation.enrichissement(loi)

print(type(structure))

# La table de Z/3Z
loi = np.array([[0, 1, 2],
                [1, 2, 0],
                [2, 0, 1]])

structure = generation.enrichissement(loi)

print(type(structure))

# Groupe de Klein
loi = np.array([[0, 1, 2, 3],
                [1, 0, 3, 2],
                [2, 3, 0, 1],
                [3, 2, 1, 0]])

structure = generation.enrichissement(loi)

print(type(structure))

# Z/4Z
loi = np.array([[0, 1, 2, 3],
                [1, 0, 3, 2],
                [2, 3, 1, 0],
                [3, 2, 0, 1]])

structure = generation.enrichissement(loi)

print(type(structure))
