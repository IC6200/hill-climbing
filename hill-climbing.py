import utils
from tabulate import tabulate


def hill_climbing(map):

    return None


map = [
    [
        None,
        None,
        None,
        None,
        utils.OBJECT_HOSPITAL,
        None,
        None,
        None,
        utils.OBJECT_HOUSE,
        None,
    ],
    [None, None, utils.OBJECT_HOUSE, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [
        None,
        utils.OBJECT_HOUSE,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        utils.OBJECT_HOSPITAL,
    ],
    [None, None, None, None, None, None, utils.OBJECT_HOUSE, None, None, None],
]


print(tabulate(map, tablefmt="grid", floatfmt=".2f"))
