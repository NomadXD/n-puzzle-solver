import random
import copy
import timeit

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
        indexes = []
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                if self.tiles[i][j] == "-":
                    indexes.append([i,j])
        return indexes


    def validate_index(self,y_old,x_old,y_shifted,x_shifted):
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
        return self.h(start.tiles,goal) + start.level

    def h_manhattan(self,start,goal):
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
        misplacements = 0
        for i in range(self.size):
            for j in range(self.size):
                if start[i][j] != goal[i][j] and start[i][j] != '-':
                    misplacements += 1
        return misplacements

    def solve_puzzle(self):
        start_time = timeit.default_timer()
        start = Node(self.start,0,0,None,None)
        goal = self.goal
        start.f_val = self.f(start,goal)

        self.open.append(start)
        count = 0
        while len(self.open) > 0:
            print(count)
            current = self.open[0]
            #print("Selected",current.tiles,current.f_val)
            if self.h(current.tiles,goal) == 0:
                path = []
                while current.predecessor != None:
                    path.append(current.movement)
                    current = current.predecessor
                print(path[::-1])
                stop = timeit.default_timer()
                report = [current.tiles,count,path,stop - start_time]
                f = open("report_1.txt", "a")
                f.write(str(report)+"\n")
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
                    print(successor.tiles, successor.f_val)
                    self.open.append(successor)

            self.closed.append(current)
            del self.open[0]
            self.open.sort(key = lambda x:x.f_val,reverse=False)
            count += 1
            
            
                    
def read_file(file_name):
    tiles = []
    with open(file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    lines = list(filter(None,content))
    for line in lines:
        line = line.split('\t')
        tiles.append(line)

    return tiles

start = read_file('start.txt')
goal = read_file('goal.txt')

modified_goal = copy.deepcopy(goal)
for _ in range(2):
    k = random.randint(0,len(modified_goal)-1)
    l = random.randint(0,len(modified_goal)-1)
    i = random.randint(0,len(modified_goal)-1)
    j = random.randint(0,len(modified_goal)-1)
    temp_1 = modified_goal[i][j]
    modified_goal[i][j] = modified_goal[l][j]
    modified_goal[l][j] = temp_1
   

puzzle = Puzzle(len(modified_goal),modified_goal,goal)
puzzle.solve_puzzle()
print(modified_goal)
print(goal)









# initial_state = [1,5,3,4,2,6,7,8,0]
# goal_state = [0,1,2,3,4,5,6,7,8]
# def calculateManhattan(initial_state):
#     initial_config = initial_state
#     manDict = 0
#     for i,item in enumerate(initial_config):
#         print(i,item)
#         prev_row,prev_col = int(i/ 3) , i % 3
#         goal_row,goal_col = int(item /3),item % 3
#         manDict += abs(prev_row-goal_row) + abs(prev_col - goal_col)
#     print(manDict)
#     return manDict

# calculateManhattan(initial_state)

