from enum import Enum
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
    
    def __str__(self):
        return str(list(self.possibilities)[0])

class GroupType(Enum):
    ROW = 1,
    COLUMN = 2,
    BOX = 3

# Contains 9 nodes, and represents a row/column/box
class Group:
    def __init__(self, nodes, group_type):
        self.nodes = nodes
        self.group_type = group_type
        for node in nodes:
            node.add_group(self)

    def trim_possibilities(self):
        for num in range(1, len(self.nodes) + 1):
            nodes_with_num = [n for n in self.nodes if num in n.possibilities]
            other_groups = [g for g in combine_groups(nodes_with_num) if g != self]
            for group in other_groups:
                if all([n in group.nodes for n in nodes_with_num]):
                    group.remove_possibilities_from_other_nodes(nodes_with_num, [num])

        for num_nodes in range(1, len(self.nodes)):
            for comb in combinations(self.nodes, num_nodes):
                all_possibilities = combine_possibilities(comb)
                if len(all_possibilities) == num_nodes:
                    other_nodes = self.nodes.difference(comb)
                    for other_node in other_nodes:
                        other_node.possibilities = other_node.possibilities.difference(all_possibilities)

    def remove_possibilities_from_other_nodes(self, nodes, nums):
        for node in self.nodes.difference(nodes):
            node.possibilities = node.possibilities.difference(nums)
    
    def is_solved(self):
        return all([len(node.possibilities) == 1 for node in self.nodes])
    
    def has_x_or_fewer_nodes_with_num(self, num_nodes, num):
        return len(self.get_nodes_with_num(num)) <= num_nodes
    
    def get_nodes_with_num(self, num):
        return set([node for node in self.nodes if num in node.possibilities])

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

# g = Group(set(nodes), GroupType.ROW)
# g.trim_possibilities()
# print([node.possibilities for node in g.nodes])

# easy for the algo
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

# harder for the algo (failing leetcode test case after first attempt)
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

# board = [
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."]]

# fail
# board = [
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".","2",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".","2",".",".","2","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".",".",".",".",".",".",".","."],
#     [".",".","2",".",".","2",".",".","2"]]

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
        groups.append(Group(set(row), GroupType.ROW))

    for j in range(len(node_matrix[0])):
        column = []
        for i in range(len(node_matrix)):
            column.append(node_matrix[i][j])
        groups.append(Group(set(column), GroupType.COLUMN))
    
    boxes = [[] for _ in range(len(node_matrix))]
    box_size = int(sqrt(len(node_matrix)))
    for i in range(len(node_matrix)):
        for j in range(len(node_matrix[i])):
            box_idx = i // box_size * box_size + j // box_size
            boxes[box_idx].append(node_matrix[i][j])
    for box in boxes:
        groups.append(Group(set(box), GroupType.BOX))
    
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
                # TODO remove
                if len(possibilities):
                    row.append(str(possibilities[0]))
                else:
                    row.append('0')
        res.append(row)
    return res

def get_nodes_with_num(groups, num):
    nodes = set()
    for group in groups:
        nodes = nodes.union(group.get_nodes_with_num(num))
    return nodes

def get_all_groups_with_node_with_num(groups, num, group_type):
    columns = set()
    for group in groups:
        nodes_with_num = group.get_nodes_with_num(num)
        for node in nodes_with_num:
            for node_group in node.groups:
                if node_group.group_type == group_type:
                    columns.add(node_group)
    return columns

# This function handles situations like the following:
# 
# R1 possibilities:     [2, ...], [2, ...], [...], [2, ...], [  ... ], [...], [...], [...], [...]
# R2 possibilities:     [2, ...], [  ... ], [...], [2, ...], [  ... ], [...], [...], [...], [...]
# R3 possibilities:     [2, ...], [2, ...], [...], [2, ...], [  ... ], [...], [...], [...], [...]
# R4 possibilities:     [2, ...], [2, ...], [...], [  ... ], [2, ...], [...], [...], [...], [...]
#
# In row 4, the 2s in columns 1 and 2 should be trimmed from the possibilities because a 2 must go
# in one of the 3 spots in row 1, one of the 2 spots in row 2, and one of the 3 spots in row 3.
# In every case, a 2 must appear in column 1 and column 2 within the top 3 rows, meaning it can't
# appear in column 1 or 2 in row 4.

def trim_by_group_sets(rows, columns):
    for num in range(1, len(rows) + 1):
        for num_nodes in range(2, len(rows)):
            rows_with_x_or_fewer_nodes_with_num = [group for group in rows if group.has_x_or_fewer_nodes_with_num(num_nodes, num)]
            nodes_with_num = get_nodes_with_num(rows_with_x_or_fewer_nodes_with_num, num)
            all_columns = get_all_groups_with_node_with_num(rows_with_x_or_fewer_nodes_with_num, num, GroupType.COLUMN)
            if len(all_columns) == len(rows_with_x_or_fewer_nodes_with_num):
                for column in all_columns:
                    column.remove_possibilities_from_other_nodes(nodes_with_num, [num])

    for num in range(1, len(rows) + 1):
        for num_nodes in range(2, len(rows)):
            columns_with_x_or_fewer_nodes_with_num = [group for group in columns if group.has_x_or_fewer_nodes_with_num(num_nodes, num)]
            nodes_with_num = get_nodes_with_num(columns_with_x_or_fewer_nodes_with_num, num)
            all_rows = get_all_groups_with_node_with_num(columns_with_x_or_fewer_nodes_with_num, num, GroupType.ROW)
            if len(all_rows) == len(columns_with_x_or_fewer_nodes_with_num):
                for row in all_rows:
                    row.remove_possibilities_from_other_nodes(nodes_with_num, [num])

def solve(sudoku):
    node_matrix = create_node_matrix(sudoku)
    groups = create_groups(node_matrix)
    rows = groups[0:9]
    columns = groups[9:18]

    while any([not group.is_solved() for group in groups]):
        for unsolved_group in [group for group in groups if not group.is_solved()]:
            unsolved_group.trim_possibilities()
        
        trim_by_group_sets(rows, columns)

        for row in convert_node_matrix_to_str_matrix(node_matrix):
            print(row)
        print('')
        print('')
        # return
    
    return convert_node_matrix_to_str_matrix(node_matrix)

print(solve(board))