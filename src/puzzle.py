import random
import math
import re
from color_print import ColorPrint as CP


class Puzzle:
    agents = []
    grid = []
    # initialize the board with the size of the puzzle  
    def __init__(self, row_size, fullfilness):
        self.fullfilness = fullfilness/100
        self.row_size = self.col_size = Puzzle.row_size = Puzzle.col_size = row_size
        self.grid_size = self.row_size ** 2
        
        # randomly generate the position of the agents and values
        pos = [(row,col) for row in range(0,self.row_size) for col in range(0,self.col_size)]
        self.max_agents = self.grid_size-1
        self.nbAgents = math.ceil(self.max_agents * self.fullfilness)
        
        self.target = random.sample(pos, k=self.nbAgents)
        self.position = random.sample(pos, k=self.nbAgents)
        
        Puzzle.grid = [[None for _ in range(self.col_size)] for _ in range(self.row_size)]
        
    
    def showGrid():
        for rowGrid in Puzzle.grid:
          for cellGrid in rowGrid:
              if cellGrid is None:
                CP.print_bold("..", end="  ")
                continue

              threadNumb = str(re.findall(r'Thread-\d+', str(cellGrid))[0].split('-')[-1])
              if cellGrid.current_position == cellGrid.target_position:
                 CP.print_pass(threadNumb, end="  ")
                 continue
              CP.print_fail(threadNumb, end="  ")     
          print('\n')
          
      
    def streamlitShowGrid():
      dictThread = {}
      lsThread = []
      for rowGrid in Puzzle.grid:
        curTR = """<tr>"""
        for cellGrid in rowGrid:
          if cellGrid is None:
            continue
          threadNumb = str(re.findall(r'Thread-\d+', str(cellGrid))[0].split('-')[-1])
          lsThread.append(int(threadNumb))
      dictThread = {threadNumb : str(i+1) for i, threadNumb in enumerate(sorted(lsThread, reverse=False))}
      
        
        
      backgroundColor = "#FDF8F2"
      borderColor = "#FFFFFF"
      succesColor, failedColor = "#94C199", "#F9777B"
      
      
      sumTR = """"""      
      for rowGrid in Puzzle.grid:
        curTR = """<tr>"""
        for cellGrid in rowGrid:
          if cellGrid is None:
            curTR += f"""<td style="border:3px solid {borderColor}; font-size:50px; color:{backgroundColor}">-</td>"""
            continue

          threadNumb = str(re.findall(r'Thread-\d+', str(cellGrid))[0].split('-')[-1])
          threadNumb = dictThread[int(threadNumb)]
          threadNumb = f'0{threadNumb}' if int(threadNumb) < 10 else threadNumb 
          if cellGrid.current_position == cellGrid.target_position:
            curTR += f"""<td style="border:3px solid {borderColor}"><span style="color:{succesColor}; font-size:50px">{threadNumb}</span></td>"""
            continue
          curTR += f"""<td style="border:3px solid {borderColor}"><span style="color:{failedColor}; font-size:50px">{threadNumb}</span></td>"""
        curTR += """</tr>"""
        sumTR += curTR
      
      tableGRID = f"""
        <div style="text-align:center">
          <div style="text-align:center; border-radius:15px; background-color:{backgroundColor}; padding:15px; display:inline-block">
            <table style="background-color:{backgroundColor}">
              {sumTR}
            </table>
          </div>
        </div>
      """
      
      return tableGRID
    
    
    # def streamlitShowGrid():
    #   printGRID = """"""
      
    #   for rowGrid in Puzzle.grid:
    #     for cellGrid in rowGrid:
    #       if cellGrid is None:
    #         printGRID += """<span style="color:black; margin-left:20px; margin-right:20px; border: 1px solid black; width:100px">[]</span>"""
    #         continue

    #       threadNumb = str(re.findall(r'Thread-\d+', str(cellGrid))[0].split('-')[-1])
    #       if cellGrid.current_position == cellGrid.target_position:
    #         printGRID += f"""<span style="color:green; font-size:50px; margin-left:20px; margin-right:20px; border: 1px solid black; width:100px">{threadNumb}</span>"""
    #         continue
    #       printGRID += f"""<span style="color:red; font-size:50px; margin-left:20px; margin-right:20px; border: 1px solid black; width:100px">{threadNumb}</span>"""
    #     printGRID += """<br>"""
        
    #   printGRID = f"""
    #     <div style="text-align:center">
    #       <div style="text-align:center; background-color:white; padding:20px; display:inline-block">
    #         <div style="border: 3px solid black">
    #           {printGRID}
    #         </div>
    #       </div>
    #     </div>
    #   """
      
    #   return printGRID