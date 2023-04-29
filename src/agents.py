import random
import time
from threading import Thread, Semaphore
from puzzle import Puzzle
from message import Message

class Agent(Thread): 
    
    semaphore = Semaphore(1)
    message = []
    
    def __init__(self, current_postition, target_position):
        Thread.__init__(self)
        self.current_position = current_postition
        self.target_position = target_position
        Puzzle.grid[self.current_position[0]][self.current_position[1]] = self
        Puzzle.agents.append(self)
        self.running = True
        
    def run(self):
        while self.running:
            self.semaphore.acquire()
            self.move_agent()
            self.semaphore.release()
            time.sleep(0.05)
    
    #fonction to move the agent 
    def move_agent(self):   
        # check if there is a message already
        if len(Agent.message) == 0:
            Agent.message.append(Message(self, self, self.target_position))
                    
        if len(Agent.message) > 0:
            # check if thread is the master
            if Agent.message[0].sender == self:
                # master is at target position
                if self.current_position == self.target_position:
                    Agent.message = []
                    return
                
                # master is not at target position and cannot move
                if len(Agent.message) > 1:
                    return 
                
                # get best path to target position
                best_next_position = self.AStar_algorithm(self.target_position)[1]
                # check if best next position is void, if true then move
                if Puzzle.grid[best_next_position[0]][best_next_position[1]] == None:
                    Puzzle.grid[self.current_position[0]][self.current_position[1]] = None
                    self.current_position = best_next_position
                    Puzzle.grid[self.current_position[0]][self.current_position[1]] = self                   
                    return 
                else: 
                    path2void = Puzzle.grid[best_next_position[0]][best_next_position[1]].getClosestVoid()
                    Agent.message.append(Message(self, Puzzle.grid[path2void[0][0]][path2void[0][1]], path2void[1]))
                    # send all messages in best path
                    for idx in range(len(path2void)-2):    
                        sender = Puzzle.grid[path2void[idx][0]][path2void[idx][1]]
                        receiver = Puzzle.grid[path2void[idx+1][0]][path2void[idx+1][1]]  
                        if receiver == None:
                            return                  
                        Agent.message.append(Message(sender, receiver, path2void[idx+2]))                    
                    return
            else:
                # current thread is not master
                if Agent.message[-1].receiver == self:
                    Puzzle.grid[self.current_position[0]][self.current_position[1]] = None
                    self.current_position = Agent.message[-1].position
                    Puzzle.grid[self.current_position[0]][self.current_position[1]] = self
                    Agent.message.pop(-1)
                    return
                
    def getClosestVoid(self):    
        lsVoid = []
        # get a list of void positions
        for row in range(0, Puzzle.row_size):
            for col in range(0, Puzzle.col_size):
                if Puzzle.grid[row][col] == None:
                    lsVoid.append((row,col))

        lsDistance = []
        # get the closest void position
        for void in lsVoid:
            lsDistance.append((sum(abs(value1 - value2) for value1, value2 in zip(self.current_position, void)), void))
        bestVoid = random.choice(list(filter(lambda distInf : distInf == min(lsDistance, key=lambda x: x[0]), lsDistance)))[1]
        return self.AStar_algorithm(bestVoid)
                
    # A* algorithm to get best path
    def AStar_algorithm(self, objective_position):
        # dictionary of remaining distance, done distance, and their sum distance
        ghf = dict({self.current_position: [0, 0, 0]})      
        # dictionary of parents      
        parents = dict({self.current_position: None})
        
        open_list = [self.current_position]       
        closed_list = []
                
        while len(open_list) > 0:
            choice = open_list[0]
            for position in open_list:
                if ghf[position][2] < ghf[choice][2]:
                    choice = position
        
            if choice == objective_position:
                path = []
                while choice != None:
                    path.append(choice)
                    choice = parents[choice]   
                path.reverse()
                return path
            
            open_list.remove(choice)
            closed_list.append(choice)
            
            # all possible neighbors of choice position
            for new in random.sample([(0,-1), (0,1), (-1,0), (1,0)], k=4):
                neighbor = (choice[0] + new[0], choice[1] + new[1])
                # check position is in the grid
                if neighbor[0] < 0 or neighbor[0] >= Puzzle.row_size or neighbor[1] < 0 or neighbor[1] >= Puzzle.col_size:
                    continue
                # check if neighbor is in closed list
                if neighbor in closed_list:
                    continue
                # check if neighbor is void
                if Puzzle.grid[neighbor[0]][neighbor[1]] == None:
                    newg = ghf[choice][0] + 1
                    newh = abs(neighbor[0] - objective_position[0]) + abs(neighbor[1] - objective_position[1]) #manhattan distance
                    newf = newg + newh
                else:
                    if Puzzle.grid[neighbor[0]][neighbor[1]] == Agent.message[0].sender:
                        continue
                    
                    # weights of paths to target position
                    weight = Puzzle.row_size**2
                    # check if neighbor is at target position
                    if Puzzle.grid[neighbor[0]][neighbor[1]].target_position == neighbor:
                        weight = weight*2
                    newg = ghf[choice][0] + weight
                    newh = abs(neighbor[0] - objective_position[0]) + abs(neighbor[1] - objective_position[1]) #manhattan distance
                    newf = newg + newh
                    
                # check new neighbor has already been tested 
                if neighbor not in open_list:
                    open_list.append(neighbor)
                    ghf[neighbor] = [newg, newh, newf]
                    parents[neighbor] = choice
                else:
                    # new score is better than old score
                    if newf < ghf[neighbor][2]:
                        ghf[neighbor] = [newg, newh, newf]
                        parents[neighbor] = choice
                    
