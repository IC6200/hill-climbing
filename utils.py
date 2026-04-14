import copy


OBJECT_EMPTY = None
OBJECT_HOUSE = "C"
OBJECT_HOSPITAL = "H"


MOVE_UP = (0, -1)
MOVE_DOWN = (0, 1)
MOVE_LEFT = (-1, 0)
MOVE_RIGHT = (1, 0)


def is_free_to_move(map, move):
    x, y = move
    return True if map[y][x] == None else False
    """
    Check whether a target position is empty and can be moved into.

    Args:
        map: Matrix (list of lists) representing the board.
        move: Position as (x, y), where x is horizontal and y is vertical.

    Returns:
        bool: True if the target cell is empty (None), False otherwise.
    raise NotImplementedError("is_free_to_move is not implemented yet")
    """




def is_valid_move(map, move):
    x,y = move
    return True if x >= 0 and x< len(map[0]) and y >= 0 and y < len(map) else False

    """
    Check whether a position is inside the matrix boundaries.

    Args:
        map: Matrix (list of lists) representing the board.
        move: Position as (x, y), where x is horizontal and y is vertical.

    Returns:
        bool: True if the position is within bounds, False otherwise.
    raise NotImplementedError("is_valid_move is not implemented yet")
    """

    


def find_objects(map, target_object_symbol):
    filas = len(map)
    columnas = len(map[0]);
    listaTuplas = []
    for i in range(filas):
        for j in range(columnas):
            if map[i][j] == target_object_symbol:
                tupla = (j,i)
                listaTuplas += [tupla]
    return listaTuplas
    """
    Find all coordinates where a given object symbol appears.

    Args:
        map: Matrix (list of lists) representing the board.
        target_object_symbol: Symbol to search for (None, 🏠, or 🏥).

    Returns:
        list[tuple[int, int]]: All matching coordinates as (x, y).
    raise NotImplementedError("find_objects is not implemented yet")
    """


def result(map, hospital_coordinates, target_move):
    newMap = copy.deepcopy(map)
    x,y = hospital_coordinates
    newMap[y][x] = None
    x,y = target_move
    if hospital_coordinates == target_move:
        newMap[y][x] = None
    else:
        newMap[y][x] = OBJECT_HOSPITAL
    return newMap
    """
    Create and return a new map after moving one hospital to a target position.

    Args:
        map: Matrix (list of lists) representing the board.
        hospital_coordinates: Current hospital position as (x, y).
        target_move: Destination position as (x, y).

    Returns:
        list[list]: A deep-copied map with the move applied.
    
    raise NotImplementedError("result is not implemented yet")
    """


def manhattan(pos, pos_2):
    return abs(pos_2[0] - pos[0]) + abs(pos_2[1] - pos[1])
    """
    Compute the Manhattan distance between two coordinates.

    Args:
        pos: First coordinate as (x, y).
        pos_2: Second coordinate as (x, y).

    Returns:
        int: Distance computed as abs(x2 - x1) + abs(y2 - y1).

    raise NotImplementedError("manhattan is not implemented yet")
    """



def cost(map):
    return sum(manhattan(hospital, house) for hospital in find_objects(map, OBJECT_HOSPITAL) for house in find_objects(map, OBJECT_HOUSE))
    """
    Compute total cost as the sum of distances from each hospital to each house.

    Args:
        map: Matrix (list of lists) representing the board.

    Returns:
        int: Total Manhattan-distance cost.
    
    raise NotImplementedError("cost is not implemented yet")
    """

    


def move(pos, pos_2):
    return (pos[0] + pos_2[0], pos[1] + pos_2[1])
    """
    Add two coordinates component-wise.

    Args:
        pos: First coordinate as (x, y).
        pos_2: Second coordinate as (x, y).

    Returns:
        tuple[int, int]: New coordinate as (x1 + x2, y1 + y2).
    raise NotImplementedError("move is not implemented yet")
    """



def actions(map, hospital_position):
    listaValida = []
    for move in [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]:
        x1, y1 = hospital_position
        x2, y2 = move
        newMove = (x1 + x2, y1 + y2)
        if is_valid_move(map, newMove) and is_free_to_move(map, newMove):
            listaValida += [newMove]
    return listaValida
    """
    Return all valid adjacent moves for a hospital in up, down, left, right order.

    Args:
        map: Matrix (list of lists) representing the board.
        hospital_position: Hospital coordinate as (x, y).

    Returns:
        list[tuple[int, int]]: Valid neighboring positions that are in bounds and free.
    raise NotImplementedError("actions is not implemented yet")
    """

    
