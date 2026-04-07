import utils


def hill_climbing(map):
    current_map = map
    current_cost = utils.cost(current_map)

    while True:
        best_map = current_map
        best_cost = current_cost

        for hospital in utils.find_objects(current_map, utils.OBJECT_HOSPITAL):
            for candidate_move in utils.actions(current_map, hospital):
                candidate_map = utils.result(current_map, hospital, candidate_move)
                candidate_cost = utils.cost(candidate_map)

                if candidate_cost < best_cost:
                    best_map = candidate_map
                    best_cost = candidate_cost

        if best_cost < current_cost:
            current_map = best_map
            current_cost = best_cost
        else:
            break

    return current_map
    """
    Optimize a board by repeatedly choosing the best local move.

    This function should implement classic hill climbing: on each iteration,
    evaluate every one-step move for every hospital, choose the neighbor with
    the lowest cost, and move there only if it strictly improves the current
    cost. Stop when no improving neighbor exists.

    Pseudocode (Python-style):
        current_map = map
        current_cost = utils.cost(current_map)

        while True:
            best_map = current_map
            best_cost = current_cost

            for hospital in utils.find_objects(current_map, utils.OBJECT_HOSPITAL):
                for candidate_move in utils.actions(current_map, hospital):
                    candidate_map = utils.result(current_map, hospital, candidate_move)
                    candidate_cost = utils.cost(candidate_map)

                    if candidate_cost < best_cost:
                        best_map = candidate_map
                        best_cost = candidate_cost

            if best_cost < current_cost:
                current_map = best_map
                current_cost = best_cost
            else:
                break

        return current_map

    Args:
        map: Matrix (list of lists) representing the board.

    Returns:
        list[list]: A map configuration with locally minimized cost.
    """

    raise NotImplementedError("hill_climbing is not implemented yet")
