import hc
import utils
from tabulate import tabulate


def main(map):
    solved_map = hc.hill_climbing(map)
    print(tabulate(solved_map, tablefmt="grid", floatfmt=".2f"))


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

main(map)
