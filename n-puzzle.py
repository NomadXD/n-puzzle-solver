class Node:
    def __init__(self, tiles, level, f_val):
        """ Initialize the node with the state of the tiles,
            level of the node in the tree, and value of the evaluation
            function f (f = g + h)
        """
        self.tiles = tiles
        self.level = level
        self.f_val = f_val

    def generate_successors(self):
        successors = []
        empty_indexes = self.get_empty_tile_indexes()
        for i in empty_indexes:
            shifted_indexes = [[i[0]+1,i[1]],[i[0]-1,i[1]],[i[0],i[1]+1],[i[0],i[1]-1]]
            for j in shifted_indexes:
                successor = self.validate_index(i[0],i[1],j[0],j[1])
                if successor is not None:
                    successor = Node(successor,self.level+1,0)
                    print(successor.tiles)
                    successors.append(successor)
        #print(successors)
        return successors 


    def get_empty_tile_indexes(self):
        indexes = []
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                if self.tiles[i][j] == "-":
                    indexes.append([i,j])
        print(indexes)
        return indexes


    def validate_index(self,x_old,y_old,x_shifted,y_shifted):
        #print(x_old,y_old,type(x_shifted),type(y_shifted))
        if x_shifted >= 0 and x_shifted < len(self.tiles) and y_shifted >= 0 and y_shifted < len(self.tiles):
            successor_tiles = []
            successor_tiles = self.copy(self.tiles)
            temp_val = successor_tiles[y_shifted][x_shifted]
            successor_tiles[y_shifted][x_shifted] = successor_tiles[y_old][x_old]
            successor_tiles[y_old][x_old] = temp_val
            return successor_tiles
        else:
            return None

    
    def copy(self,root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp



    




# sample = [['1','2','3','4'],['5','6','-','7'],['8','-','9','10'],['11','12','13','14']]
# level = 0
# f_val = 0

# node = Node(sample,level,f_val)
# node.generate_successors()
    


