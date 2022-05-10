from itertools import combinations
from math import sqrt

def combine_possibilities(nodes):
    res = set()
    for node in nodes:
        res = res.union(node.possibilities)
    return res

def combine_groups(nodes):
    res = set()
    for node in nodes:
        res = res.union(node.groups)
    return res

# Contains data/metadata about an individual square
class Node:
    def __init__(self, possibilities):
        self.possibilities = possibilities
        self.groups = set()
    
    def add_group(self, group):
        self.groups.add(group)

# Contains 9 nodes, and represents a row/column/box
class Group:
    def __init__(self, nodes):
        self.nodes = nodes
        for node in nodes:
            node.add_group(self)

    # There's a trim rule that needs to be added: if rows 1 and 4 contain a 2 in the
    # possibilities for columns 1 and 2, and don't include a 2 anywhere else in the
    # possibilities for those rows, 2 needs to be removed from the possibilities of
    # all other squares in columns 1 and 2
    def trim_possibilities(self):
        for num in range(1, len(self.nodes) + 1):
            nodes_with_num = [n for n in self.nodes if num in n.possibilities]
            other_groups = [g for g in combine_groups(nodes_with_num) if g != self]
            for group in other_groups:
                if all([n in group.nodes for n in nodes_with_num]):
                    group.remove_possibility_from_other_nodes(nodes_with_num, num)

        for num_possibilities in range(1, len(self.nodes)):
            for comb in combinations(self.nodes, num_possibilities):
                all_possibilities = combine_possibilities(comb)
                if len(all_possibilities) == num_possibilities:
                    other_nodes = self.nodes.difference(comb)
                    for other_node in other_nodes:
                        other_node.possibilities = other_node.possibilities.difference(all_possibilities)

    def remove_possibility_from_other_nodes(self, nodes, num):
        for node in self.nodes.difference(nodes):
            if num in node.possibilities:
                node.possibilities.remove(num)
    
    def is_solved(self):
        return all([len(node.possibilities) == 1 for node in self.nodes])

# nodes = [
#     Node(set([1, 2])),
#     Node(set([1, 2, 9])),
#     Node(set([1, 2, 3])),
#     Node(set([3, 4])),
#     Node(set([5, 6, 7, 8, 9, 1, 2])),
#     Node(set([5, 6, 9])),
#     Node(set([5, 6, 9])),
#     Node(set([5, 6, 7, 1, 2, 8])),
#     Node(set([5, 6, 9])),
# ]

# nodes = [
#     Node(set([5])),
#     Node(set([3])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
#     Node(set([7])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
# ]

# nodes = [
#     Node(set([3, 5, 6])),
#     Node(set([1, 3, 5])),
#     Node(set([9])),
#     Node(set([7])),
#     Node(set([1, 3, 4, 5, 8])),
#     Node(set([1, 3, 5])),
#     Node(set([3, 4, 5, 6, 8])),
#     Node(set([2])),
#     Node(set([3, 5, 6])),
# ]

# nodes = [
#     Node(set([1, 2, 3])),
#     Node(set([1, 2, 4])),
#     Node(set([1, 2, 3, 5])),
#     Node(set([1, 2, 6, 7])),
#     Node(set([1, 3, 4, 7])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
#     Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9])),
#     Node(set([1, 3, 5, 7])),
#     Node(set([1, 3, 6, 7])),
# ]

# g = Group(set(nodes))
# g.trim_possibilities()
# print([node.possibilities for node in g.nodes])

# board = [
#     ["5","3",".",".","7",".",".",".","."],
#     ["6",".",".","1","9","5",".",".","."],
#     [".","9","8",".",".",".",".","6","."],
#     ["8",".",".",".","6",".",".",".","3"],
#     ["4",".",".","8",".","3",".",".","1"],
#     ["7",".",".",".","2",".",".",".","6"],
#     [".","6",".",".",".",".","2","8","."],
#     [".",".",".","4","1","9",".",".","5"],
#     [".",".",".",".","8",".",".","7","9"]]

board = [
    [".",".","9","7","4","8",".",".","."],
    ["7",".",".",".",".",".",".",".","."],
    [".","2",".","1",".","9",".",".","."],
    [".",".","7",".",".",".","2","4","."],
    [".","6","4",".","1",".","5","9","."],
    [".","9","8",".",".",".","3",".","."],
    [".",".",".","8",".","3",".","2","."],
    [".",".",".",".",".",".",".",".","6"],
    [".",".",".","2","7","5","9",".","."]]

def create_node_matrix(sudoku):
    node_matrix = [[None for _ in range(len(sudoku))] for _ in range(len(sudoku))]
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            if sudoku[i][j] == '.':
                node_matrix[i][j] = Node(set([1, 2, 3, 4, 5, 6, 7, 8, 9]))
            else:
                node_matrix[i][j] = Node(set([int(sudoku[i][j])]))
    return node_matrix

def create_groups(node_matrix):
    groups = []
    for i in range(len(node_matrix)):
        row = []
        for j in range(len(node_matrix[i])):
            row.append(node_matrix[i][j])
        groups.append(Group(set(row)))

    for j in range(len(node_matrix[0])):
        column = []
        for i in range(len(node_matrix)):
            column.append(node_matrix[i][j])
        groups.append(Group(set(column)))
    
    boxes = [[] for _ in range(len(node_matrix))]
    box_size = int(sqrt(len(node_matrix)))
    for i in range(len(node_matrix)):
        for j in range(len(node_matrix[i])):
            box_idx = i // box_size * box_size + j // box_size
            boxes[box_idx].append(node_matrix[i][j])
    for box in boxes:
        groups.append(Group(set(box)))
    
    return groups

def convert_node_matrix_to_str_matrix(node_matrix):
    res = []
    for i in range(len(node_matrix)):
        row = []
        for j in range(len(node_matrix)):
            possibilities = list(node_matrix[i][j].possibilities)
            if len(possibilities) > 1:
                row.append('.')
            else:
                row.append(str(possibilities[0]))
        res.append(row)
    return res

def solve(sudoku):
    node_matrix = create_node_matrix(sudoku)
    groups = create_groups(node_matrix)

    while any([not group.is_solved() for group in groups]):
        for unsolved_group in [group for group in groups if not group.is_solved()]:
            unsolved_group.trim_possibilities()
        for row in convert_node_matrix_to_str_matrix(node_matrix):
            print(row)
        print('')
        print('')
    
    return convert_node_matrix_to_str_matrix(node_matrix)

print(solve(board))