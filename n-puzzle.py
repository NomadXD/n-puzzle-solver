class Node:
    def __init__(self, tiles, level, f_val):
        """ Initialize the node with the state of the tiles,
            level of the node in the tree, and value of the evaluation
            function f (f = g + h)
        """
        self.tiles = tiles
        self.level = level
        self.f_val = f_val

    def get_empty_tile_indexes(self):
        indexes = []
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                if self.tiles[i][j] == "-":
                    indexes.append([i,j])
        print(indexes)
        return indexes

# sample = [['1','2','3'],['4','-','-'],['6','-','8']]
# level = 0
# f_val = 0

# node = Node(sample,level,f_val)
# node.get_empty_tile_indexes()
    


