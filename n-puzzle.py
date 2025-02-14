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
        """ Generate successor nodes for each of 
            the neighbouring nodes. Returns an 
            array of Nodes
        """
        successors = []
        empty_indexes = self.get_empty_tile_indexes()
        for i in empty_indexes:
            shifted_indexes = [[i[0]+1,i[1]],[i[0]-1,i[1]],[i[0],i[1]+1],[i[0],i[1]-1]]
            for j in shifted_indexes:
                
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
                successors.append(successor)
        return successors 


    def get_empty_tile_indexes(self):
        """ Helper function to get the
            indexes of empty tiles
        """
        indexes = []
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                if self.tiles[i][j] == "-":
                    indexes.append([i,j])
        return indexes


    def validate_index(self,y_old,x_old,y_shifted,x_shifted):
        """ Helper function to validate
            the indexes
        """
        successor_tiles = []
        successor_tiles = self.copy(self.tiles)
        temp_val = successor_tiles[y_shifted][x_shifted]
        successor_tiles[y_shifted][x_shifted] = successor_tiles[y_old][x_old]
        successor_tiles[y_old][x_old] = temp_val
        return successor_tiles
    

    
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
    def __init__(self,size,start,goal):
        self.size = size
        self.open = []
        self.closed = []
        self.start = start
        self.goal = goal

    def f(self,start,goal):
        """Function that calculates
            f. f = g + h. h used here is 
            manhattan distance. If you want to 
            use misplaced tiles replace,
            self.h_manhattan with self.h
        """
        return self.h_manhattan(start.tiles,goal) + start.level

    def h_manhattan(self,start,goal):
        """Function to calculate
            total manhattan distance between
            two states
        """
        tmd = 0
        coor_dict = {}
        for i in range(self.size):
            for j in range(self.size):
                if start[i][j] in coor_dict.keys():
                    coor_dict[start[i][j]].append([i,j])
                elif start[i][j] != '-':
                    coor_dict[start[i][j]] = []
                    coor_dict[start[i][j]].append([i,j])

                if goal[i][j] in coor_dict.keys():
                    coor_dict[goal[i][j]].append([i,j])
                elif goal[i][j] != '-':
                    coor_dict[goal[i][j]] = []
                    coor_dict[goal[i][j]].append([i,j])

        for key ,value in coor_dict.items():
            tmd += abs(value[0][0]-value[1][0]) + abs(value[0][1]-value[1][1])
        return tmd
     
    
    def h(self,start,goal):
        """ Function to calculate misplaced 
            tiles heuristic
        """
        misplacements = 0
        for i in range(self.size):
            for j in range(self.size):
                if start[i][j] != goal[i][j] and start[i][j] != '-':
                    misplacements += 1
        return misplacements

    def solve_puzzle(self):
        """ Function to solve
            the puzzle
        """
        print("Solving........")
        start = Node(self.start,0,0,None,None)
        goal = self.goal
        start.f_val = self.f(start,goal)

        self.open.append(start)
        count  = 0
        while len(self.open) > 0:
            current = self.open[0]
            if self.h(current.tiles,goal) == 0:
                path = []
                while current.predecessor != None:
                    path.append(current.movement)
                    current = current.predecessor
                print(path[::-1])
                print("Number of iterations:{0}".format(count))
                f = open("output.txt", "w")
                f.write(str(path[::-1]))
                f.close()
                break

            for successor in current.generate_successors():
                is_closed = False
                for closed_node in self.closed:
                    if closed_node.tiles == successor.tiles:
                        is_closed = True
                        break
                if(is_closed):
                    continue

                if successor not in self.open:
                    successor.f_val = self.f(successor,goal)
                    self.open.append(successor)

            self.closed.append(current)
            del self.open[0]
            self.open.sort(key = lambda x:x.f_val,reverse=False)
            count += 1
            
            
            
            
        
            
def read_file(file_name):
    """Helper function to 
        read data from a file
    """
    tiles = []
    with open(file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    lines = list(filter(None,content))
    for line in lines:
        line = line.split('\t')
        tiles.append(line)

    return tiles






if __name__ == "__main__":
    print("""\
    
███╗   ██╗              ██████╗ ██╗   ██╗███████╗███████╗██╗     ███████╗              ███████╗ ██████╗ ██╗    ██╗   ██╗███████╗██████╗ 
████╗  ██║              ██╔══██╗██║   ██║╚══███╔╝╚══███╔╝██║     ██╔════╝              ██╔════╝██╔═══██╗██║    ██║   ██║██╔════╝██╔══██╗
██╔██╗ ██║    █████╗    ██████╔╝██║   ██║  ███╔╝   ███╔╝ ██║     █████╗      █████╗    ███████╗██║   ██║██║    ██║   ██║█████╗  ██████╔╝
██║╚██╗██║    ╚════╝    ██╔═══╝ ██║   ██║ ███╔╝   ███╔╝  ██║     ██╔══╝      ╚════╝    ╚════██║██║   ██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║ ╚████║              ██║     ╚██████╔╝███████╗███████╗███████╗███████╗              ███████║╚██████╔╝███████╗╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═══╝              ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝              ╚══════╝ ╚═════╝ ╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                                                                                                                                                                                                                                          
    """)
    
    
    choice = 0
    while choice != 2:
        print("------------------------------------------------------------------------------------------------------------------------------")
        print("Main menu:")
        print("1 - Solve a puzzle")
        print("2 - Exit")
        choice = int(input("Please enter your choice:"))
        if (choice == 1):
            print("""\
                Example start/goal configuration. 

                1	4	-	7
                9	2	3	5
                6	-	10	13
                8	11	14	12

                The puzzle should be created in tab delimitted format.
                Empty location is represented with -
                Provide a file name of the start/goal configuration below
            """)
            start_file = input("Start configuration filename:")
            goal_file = input("Goal configuration filename:")
            start = read_file(start_file)
            goal = read_file(goal_file)
            puzzle = Puzzle(len(start),start,goal)
            puzzle.solve_puzzle()



        
        
            


