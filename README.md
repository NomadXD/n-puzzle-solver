# n-puzzle-solver
## Console application screenshot
![ScreenShot](cover.png)

## Run locally

Python 3 should be installed.

```sh

git clone https://github.com/NomadXD/n-puzzle-solver.git
cd n-puzzle-solver
python n-puzzle-solver.py

```

## A* implementation

```py

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

```

## Manhattan distance heuristic function implementation

```py

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

```

## Misplaced tiles heuristic implementation

```py

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

```


