OBJECT_EMPTY = None
OBJECT_HOUSE = "🏠"
OBJECT_HOSPITAL = "🏥"


MOVE_UP = (0, -1)
MOVE_DOWN = (0, 1)
MOVE_LEFT = (-1, 0)
MOVE_RIGHT = (1, 0)


def is_free_to_move(map, move):
    x, y = move

    return not map[y][x]


def is_valid_move(map, move):
    rows_size = len(map)
    columns_size = len(map[0])

    x, y = move

    if y < 0 or y >= rows_size:
        return False

    if x < 0 or x >= columns_size:
        return False

    return True


def find_object(map, target_object_symbol):
    coordinates = []

    for y, rows in enumerate(map):
        for x, object in enumerate(rows):
            if object == target_object_symbol:
                coordinates.append((x, y))

    return coordinates


def result(map, hospital_coordinates, target_move):
    x_hospital, y_hospital = hospital_coordinates
    x_target, y_target = target_move

    map[y_target][x_target] = OBJECT_HOSPITAL
    map[y_hospital][x_hospital] = OBJECT_EMPTY


def manhattan(pos, pos_2):
    x, y = pos
    x_2, y_2 = pos_2

    return abs(x_2 - x) + (y_2 - y)


def move(pos, pos_2):
    return tuple(x + y for x, y in zip(pos, pos_2))


def actions(map, hospital_position):
    actions = []

    move_up = move(hospital_position, MOVE_UP)
    move_down = move(hospital_position, MOVE_DOWN)
    move_left = move(hospital_position, MOVE_LEFT)
    move_right = move(hospital_position, MOVE_RIGHT)

    for possible_move in [move_up, move_down, move_left, move_right]:
        is_valid = is_valid_move(map, possible_move) and is_free_to_move(
            map, possible_move
        )

        if is_valid:
            actions.append(possible_move)

    return actions
