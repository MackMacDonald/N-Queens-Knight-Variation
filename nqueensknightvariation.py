from timeit import default_timer as timer
from heapq import heappush, heappop, heappushpop

import numpy as np
import random
import argparse

from visuals import draw_solution

def dfs_get_branch(current_node):
    row_indexes = []

    while current_node != "-":
        row_indexes.append(current_node[0][0])
        current_node = current_node[1]

    return row_indexes

def dfs_adjacent_nodes(current_node, grid_size, parent_row_indexes):
    adjacent = []

    # All of the nodes in the column to the right
    for x in range(grid_size):
        if (x not in parent_row_indexes):
            neighbour = ((x, current_node[0][1] + 1), current_node)
            if dfs_conflicts(neighbour[0], parent_row_indexes) == 0:
                adjacent.append(neighbour)

    return adjacent


def dfs_conflicts(new_node, parent_row_indexes):
    # knight checks
    if (len(parent_row_indexes) > 0):    
        if (parent_row_indexes[0] == new_node[0]-2 or parent_row_indexes[0] == new_node[0]+2):
            return 1
    if (len(parent_row_indexes) > 1):
        if (parent_row_indexes[1] == new_node[0]-1 or parent_row_indexes[1] == new_node[0]+1):
            return 1

    # diagonal conflicts
    for i in range(1, new_node[1]+1):
        upper_left_diag_row = new_node[0] - i
        lower_left_diag_row = new_node[0] + i

        if parent_row_indexes[i-1] == upper_left_diag_row:
            return 1
        if parent_row_indexes[i-1] == lower_left_diag_row:
            return 1

    return 0


def dfs_n_queens_knight_variant(grid_size):
    current_node = None
    stack = []
    row_indexes = []

    # Fill stack with starter nodes
    for x in range(grid_size):
        new_node = ((x, 0),"-")
        stack.append(new_node)

    while stack:
        # Current node is the front of the stack
        current_node = stack.pop()

        # Success
        if current_node[0][1] == grid_size - 1:
            break

        row_indexes = dfs_get_branch(current_node)

        # Check if adjacent nodes have conflicts
        for x in dfs_adjacent_nodes(current_node, grid_size, row_indexes):
            stack.append(x)

    optimal_path = dfs_get_branch(current_node)
    optimal_path.reverse()

    return optimal_path


def genetic_fitness_function(candidate_solution):
    fitness = 0
    index = 0

    for x in candidate_solution:
        # knight move checks
        if index - 1 >= 0:
            if candidate_solution[index - 1] == x + 2:
                fitness += 1
            if candidate_solution[index - 1] == x - 2:
                fitness += 1
        if index - 2 >= 0:
            if candidate_solution[index - 2] == x + 1:
                fitness += 1
            if candidate_solution[index - 2] == x - 1:
                fitness += 1

        # diagonal conflicts
        for i in range(1, index+1):
            upper_left_diag_row = x - i
            lower_left_diag_row = x + i

            if candidate_solution[index-i] == upper_left_diag_row:
                fitness += 1
            if candidate_solution[index-i] == lower_left_diag_row:
                fitness += 1

        # increment index
        index += 1


    # avoid divide by zero
    if fitness == 0:
        return 100
    else:
        return 1 / fitness

# Order 1 crossover
def genetic_operator(parent_list):
    children = []
    parent_one = parent_list[0][2]
    parent_two = parent_list[1][2]

    indexes = random.sample(range(0, len(parent_one) - 1), 2)
    indexes.sort()

    parent_one_cut = parent_one[indexes[0] : indexes[1]]
    parent_two_cut = parent_two[indexes[0] : indexes[1]]

    child_one = [x for x in parent_two if x not in parent_one_cut]
    child_two = [x for x in parent_one if x not in parent_two_cut]

    children.append(child_one[: indexes[0]] + parent_one_cut + child_one[indexes[0] :])
    children.append(child_two[: indexes[0]] + parent_two_cut + child_two[indexes[0] :])

    child_one = children[0]
    child_two = children[1]

    return children

# randomly select 2 integers for a swap 10% of the time
def genetic_mutation(children_list):
    for x in children_list:
        rand = random.randint(1, 10)
        if rand <= 1:
            indexes = random.sample(range(0, len(x)), 2)
            x[indexes[0]], x[indexes[1]] = x[indexes[1]], x[indexes[0]]
    return children_list


def genetic_n_queens_knight_variant(n):
    iterations = 0
    inital_population = 100
    candidate_solutions = []
    candidate_board = []
    optimal_solution = ""

    # Used to break ties in the min heap
    counter = 0

    # inital population of candidate solutions
    for x in range(inital_population):
        candidate = np.random.permutation(n).tolist()
        if not any(candidate in x for x in candidate_solutions):
            heappush(candidate_solutions, (genetic_fitness_function(candidate), counter, candidate))
            counter += 1
            candidate_board.append(candidate)

    # main loop
    while not optimal_solution:
        children = []
        mutated_children = []

        # check if optimal solution was found
        highest_fitness = max(candidate_solutions)
        if highest_fitness[0] == 100:
            optimal_solution = highest_fitness[2]
            break

        children = genetic_operator(random.choices(candidate_solutions, k=2))
        mutated_children = genetic_mutation(children)

        # check fitness of children
        for child in mutated_children:
            fitness = genetic_fitness_function(child)
            if child not in candidate_board:
                # child has higher fitness than weakest of candidates
                if (fitness > min(candidate_solutions)[0]):
                    heappushpop(candidate_solutions, (fitness, counter, child))
                    counter += 1
                    candidate_board.append(child)

        iterations += 1

        # stop if algorithm is stuck at local minimum
        if iterations == 50000:
            optimal_solution = heappop(candidate_solutions)[2]
            break

    return (optimal_solution, iterations, genetic_fitness_function(optimal_solution))

def main():
    parser = argparse.ArgumentParser(description="Calculate solution for N-Queens Knight variation problem.")
    parser.add_argument('algorithm', choices=['genetic', 'dfs'], help='algorithm to execute')
    parser.add_argument('n', type=int, help='number of queens and size of board')
    args = parser.parse_args()

    if args.n < 10:
        print("n value too small, n must be >= 10")
    else:
        if args.algorithm == "genetic":
            start = timer()
            solution = genetic_n_queens_knight_variant(args.n)
            end = timer()

            conflicts = 0
            if solution[2] != 100:
                conflicts = 1 / solution[2]

            print(f'Time taken: {(end-start)} solution: {solution[0]} iterations: {solution[1]} conflicts: {conflicts}')
            draw_solution(solution[0])

        elif args.algorithm == "dfs":
            start = timer()
            solution = dfs_n_queens_knight_variant(args.n)
            end = timer()
            print(f'Time taken: {(end-start)} solution: {solution}')
            draw_solution(solution)


if __name__ == "__main__":
    main()
