class Node:
    def __init__(self, tiles, level, f_val, movement, predecessor):
        """ Initialize the node with the state of the tiles,
            level of the node in the tree, and value of the evaluation
            function f (f = g + h)
        """
        self.tiles = tiles
        self.level = level
        self.f_val = f_val
        self.movement = movement
        self.predecessor = predecessor 

    def generate_successors(self):
        successors = []
        empty_indexes = self.get_empty_tile_indexes()
        for i in empty_indexes:
            shifted_indexes = [[i[0]+1,i[1]],[i[0]-1,i[1]],[i[0],i[1]+1],[i[0],i[1]-1]]
            print(shifted_indexes)
            for j in shifted_indexes:
                #print(j)
                if not (j[0] >= 0 and j[0] < len(self.tiles) and j[1] >= 0 and j[1] < len(self.tiles)):
                    continue

                if i[0] < j[0]:
                    movement = (self.tiles[j[0]][j[1]],"Down")
                elif i[0] > j[0]:
                    movement = (self.tiles[j[0]][j[1]],"Up")
                elif i[1] > j[1]:
                    movement = (self.tiles[j[0]][j[1]],"Right")
                elif i[1] < j[1]:
                    movement = (self.tiles[j[0]][j[1]],"Left")
                else:
                    pass 
                successor = self.validate_index(i[0],i[1],j[0],j[1])
                successor = Node(successor,self.level+1,0,movement,self)
                #print(successor.tiles)
                successors.append(successor)
                # if successor is not None:
                #     successor = Node(successor,self.level+1,0,movement,self)
                #     print(successor.tiles)
                #     successors.append(successor)
        #print(successors)
        return successors 


    def get_empty_tile_indexes(self):
        indexes = []
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                if self.tiles[i][j] == "-":
                    indexes.append([i,j])
        #print(indexes)
        return indexes


    def validate_index(self,y_old,x_old,y_shifted,x_shifted):
        #print(x_old,y_old,type(x_shifted),type(y_shifted))
        #if y_shifted >= 0 and y_shifted < len(self.tiles) and x_shifted >= 0 and x_shifted < len(self.tiles):
        successor_tiles = []
        successor_tiles = self.copy(self.tiles)
        temp_val = successor_tiles[y_shifted][x_shifted]
        #print(temp_val)
        #print(successor_tiles[])
        successor_tiles[y_shifted][x_shifted] = successor_tiles[y_old][x_old]
        successor_tiles[y_old][x_old] = temp_val
        #print(successor_tiles)
        return successor_tiles
        #else:
            #return None

    
    def copy(self,root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

class Puzzle:
    def __init__(self):
        self.size = 4
        self.open = []
        self.closed = []
        self.start = [['1','4','-','7'],['9','2','3','5'],['6','-','10','13'],['8','11','14','12']]
        #self.start = [['1','2','3'],['4','5','-'],['6','-','7']]
        #self.goal = [['1','2','3'],['4','5','6'],['7','-','-']]
        self.goal = [['1','4','7','5'],['9','2','3','-'],['-','11','10','13'],['6','8','14','12']]

    def f(self,start,goal):
        #print(start.tiles)
        return self.h(start.tiles,goal) + start.level

    def h(self,start,goal):
        misplacements = 0
        for i in range(self.size):
            for j in range(self.size):
                if start[i][j] != goal[i][j] and start[i][j] != '-':
                    misplacements += 1
        return misplacements

    def solve_puzzle(self):
        start = Node(self.start,0,0,None,None)
        goal = self.goal
        start.f_val = self.f(start,goal)

        self.open.append(start)
        count = 0
        while len(self.open) > 0:
            current = self.open[0]
            print("New It",current.tiles)
            print("H",self.h(current.tiles,goal))
            if self.h(current.tiles,goal) == 0:
                path = []
                while current.predecessor != None:
                    path.append(current.movement)
                    current = current.predecessor
                print(path[::-1])
                break

            for successor in current.generate_successors():
                is_closed = False
                for closed_node in self.closed:
                    if closed_node.tiles == successor.tiles:
                        is_closed = True
                        break
                if(is_closed):
                    continue

                # if successor in self.open and successor.level > current.level:
                #     continue

                if successor not in self.open:
                    successor.f_val = self.f(successor,goal)
                    print("")
                    print("  | ")
                    print("  | ")
                    print(" \\\'/ \n")
                    for i in successor.tiles:
                        for j in i:
                            print(j,end=" ")
                        print("")
                    #print("Tiles",successor.tiles)
                    print("f_val",successor.f_val)
                    print("level",successor.predecessor)
                    self.open.append(successor)
                    print(len(self.open))
            self.closed.append(current)
            del self.open[0]
            print(len(self.closed))
            self.open.sort(key = lambda x:x.f_val,reverse=False)
            #for i in self.open:
                #print(i.f_val)
            #print(self.open)
            #print(self.closed)
            #count+= 1
            print("===========================================================================")
            # if(count == 5):
            #     break
            





    




#sample = [['1','2','3','4'],['5','6','-','7'],['8','-','9','10'],['11','12','13','14']]
# sample = [['1','2','3'],['4','5','-'],['6','7','8']]
# level = 0
# f_val = 0

# node = Node(sample,level,f_val)
# node.generate_successors()
    
puzzle = Puzzle()
puzzle.solve_puzzle()


