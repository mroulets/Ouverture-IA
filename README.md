 <span style="color:gray"> *Project developed for the course "Ouverture-IA"  by Artificial Intelligence Engineering students Maria Paula Roulet, Lauren Durivault and Mounish Badireddi.*</span>

## Introduction
This `Multi Agent Puzzle` project is based on an American game called `"15 Puzzle"` or "Taquin" in french. The goal is to reorganize pieces j in grid nxn by exchanging the position of j by the position of the void until the puzzle is resolved. For this project, we decided to use `Python` to code the algorithm of the game and `Streamlit` to develop a simple [interface](https://mroulets-puzzlemultiagent-app-tv08ho.streamlit.app) to play deployed through to `Docker`.


## Project Demo
https://user-images.githubusercontent.com/75457142/235311803-ccbecb4f-3e69-47a8-b3e8-f4dbd165defb.mp4


## Project Description
Compared to the original game, ours has a multi agent perspective where multiple pieces can move at the same time. This organization is done thanks to `threads` and `semaphore`from the Python packages `Threads`. 

### Puzzle Algorithm
The code represents an implementation of the puzzle game where multiple agents try reach their own target positions on the grid. 
In the structure of our project, the `Puzzle` class is responsible for generating the board and showing the current state of the game grid. When creating an instance of the Puzzle class, the constructor takes two arguments, row_size and fullfilness, row_size is the number of rows and columns in the square grid, and fullfilness is a percentage indicating the number of agents that should be randomly placed on the grid. The showGrid method displays the current state of the game board. Finally it allows to print the puzzle pieces in red or green depending if they are at their target position or not. 

The `Agent` class is implemented as a Thread subclass that represents the agents and their movement logic. The use of threads and semaphore can be found in this class in order to allow the communication and movement between pieces.The semaphore ensures that only one agent can access the message queue at a time. Each time a piece wants to move to its target position, a message will be generated and stocked in a queue. This is made to organize the movement of all the pieces and avoid back and forward shifts. If an agent is the first one to put a message in the queue then it is the main piece and it will go to its target position by using the best path found thanks to the use of the `A* algorithm`. Once the piece arrives to its objective then the semaphore is released and the message is removed and so on. In the case of a piece is not at its target position and it is not the main agent in the queue then messages are transmitted to move each piece of the path to find the nearest void according to the Manhattan distace (using the function getClosestVoid) in order to allow the main one to move. After the agent in the top message of the queue is relocated, the system will wait for the semaphore to be retrieved and execute the corresponding command. As each command in the message stack is completed, it will be removed to enable the next action to take place. 

Lastly the `Message` class represents the message exchanged between agents during their movement.

#### A* Algorithm
The A* algorithm is a pathfinding algorithm used to find the shortest path between two points on a graph or a grid. It is a heuristic algorithm that uses an evaluation function to determine which path to explore next. 

The algorithm maintains two lists of positions: an open list and a closed list. The open list contains positions that have been discovered but not yet explored, while the closed list contains positions that have been explored.

The algorithm works by assigning each positions/agent a score, which is the sum of two values: the cost to reach the position from the starting point (known as the g-score), and an estimate of the remaining cost to reach the destination (known as the h-score). The f-score is the sum of the g-score and the h-score.

At each step, the algorithm selects the positions with the lowest f-score from the open list and expands it, considering its neighbors. For each neighbor, the algorithm calculates its g-score, h-score, and f-score. If the neighbor is already on the open list and the new f-score is lower than its current f-score, the neighbor's f-score is updated. If the neighbor is not on the open list, it is added to the open list.

The algorithm continues to expand positions of agents from the open list until the destination is reached, or the open list is empty, indicating that no path exists between the start and destination points.

A* algorithm guarantees to find the shortest path if the heuristic function used to estimate the remaining cost is admissible and consistent.

### Puzzle WebApp
To have a more user friendly experience we decided to create a webapp. 
The puzzle [interface](https://mroulets-puzzlemultiagent-app-tv08ho.streamlit.app) is constructed by using `Streamlit` and it is deployed through `Docker`. 

We put at the player's disposal some settings that she/he can change according to her/his preferences. Among the options, the grid size, the fulfilness ratio, the frequency of prints of the grid and the time of running can be set. 

Once the options are selected, the submit button allows to run de algorithm and see according to the frequency of prints the initial grid and the current grid and state i. When the puzzle is solved (all agents are at their target position in green) or the running time was reached, a slider is available to see the multiple states i of the grid until the final one. 

#### Configurations
   1. Size of the Grid: this parameter, as the name says, allows the user to determine the size n of the grid nxn he wishes, from 3 to 20.
   2. Frequency of Grid Display: this parameter helps set the frequency, in seconds, you wish to see the grid change from 1 second to 60 seconds.
   3. The Agent Fullfiness: this percentage allows to set the amount of agents present in the puzzle, starting at 30% until 100% filled.
   4. Max Execution Time: is the maximum of seconds that the algorithm will run to find a solution, from 5 seconds until 600 seconds.

If you wish to run one more time the puzzle, you can do so by clicking the New Configuration button. 

### Further Implementation
It is important to now that the higher the ratio of fulfilness the longer it takes to solve the puzzle (if its has a solution) so you have to be aware of the timing you set according to other option. Plus, the lower the amount of voids in the puzzle, the lower the chances to have a solution, so it is possible that sometimes some agents get stucked at some positions because they cannot find a suitable way to get to their target position. It could be interesting to clear up this by first generating the solved version of the puzzle and then disorganize the agents following possible paths. 

In addition, due to some bugs in the Threads packaging it is possible that if you run an important amount of times the interface and the algorithm, the grids do not show the movement of the agents. If this is the case, we ask you to close the webapp, wait a little while and try again. 
