from constraint import *
import random

problem = Problem()

# Defining each space
values = []
for i in range(9):
    for j in range(9):
        values.append(str((i, j)))

# Adding variables
problem.addVariables(
    values,
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
)

# Defining constraints
constraints = []
for i in range(9):
    constraint_1 = []
    constraint_2 = []
    for j in range(9):
        constraint_1.append(str((i, j)))
        constraint_2.append(str((j, i)))
    constraints.append(constraint_1)
    constraints.append(constraint_2)

# Defining box constraints
for i in range(3):
    constraint_set = dict()
    constraint_set[0] = []
    constraint_set[1] = []
    constraint_set[2] = []
    for j in range(9):
        add = 9 * i
        for num, k in enumerate([0, 3, 6]):
            constraint_set[num].append(str((int((j + add) % 3 + k), int((j +
                                                                         add) /
                                                                        3))))
    for u in range(3):
        constraints.append(constraint_set[u])


# Adding constraints
for constraint in constraints:
    problem.addConstraint(AllDifferentConstraint(), constraint)

# Getting values
values = problem.getSolution()

# Taking random cells for filling
unknown = random.choices(list(values.keys()), k=14)
unknown = set.union(set(unknown))

