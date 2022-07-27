import itertools
from operator import le
import random
from subprocess import call
from turtle import width

from sympy import N


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells)==self.count and self.count !=0:
            print('Mine identifeled' ,self.cells)
            return self.cells
        else:
            return set()
    
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells
        else:
            return set()
        
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=-1
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


        


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            
            

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

            
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(call)
        self.mark_safe(cell)

        new_sentence_call = set()

        for i in range(cell[0] -1 ,cell[0]+2):
            for j in range(cell[1]-1 , cell[1] +2 ):

                if (i,j) == cell:
                    continue

                if (i,j) == self.safes:
                    continue

                if(i,j)==self.mines:
                  count=count-1 
                  continue
                

                
                if 0 <= i< self.height and 0<= j < self.width:
                    new_sentence_call.add((i,j)) 
        print(f'Move on cell:{cell} has add sentence to knowledge {new_sentence_call}={count}')
        self.knowledge.append(Sentence(new_sentence_call , count))

        knowledge_change= True

        while knowledge_change:
            knowledge_change= False

            safe =set()
            mines = set()

        for sentence in self.knowledge:
         safe = safe.union(sentence.known_safes())
         mines = mines.union(sentence.known_mines())

         if safe:
             knowledge_change = True
             for safes in safe:
                 self.mark_safe(safes)
        
        if mines :
            knowledge_change= True
            for min in mines:
                self.mark_mine(min)

        empty = Sentence(set(),0)
        self.knowledge[:] = [ x for x in self.knowledge if x!= empty]


        for sentence_1 in self.knowledge:
            for sentence_2 in self.knowledge: 

                if sentence_1.cells == sentence_2.cells:
                    continue 

                if sentence_1.cells== set() and sentence_1.count > 0:
                    print('Error _ sentence with no cells and count created')
                    raise ValueError

                if sentence_1.cells.issubset(sentence_2.cells):
                    new_sentence_call = sentence_2.cells - sentence_1.cells
                    new_sentence_count = sentence_2.count - sentence_1.count


                    new_sentence= Sentence(new_sentence_call,new_sentence_count)

                    if new_sentence  not in self.knowledge:
                        knowledge_change=True
                        print('New Inferred Knowledage',new_sentence,'form',sentence_1,'and ',sentence_2)
                        self.knowledge.append(new_sentence)



        print('Current AI KB Knowloage',len(self.knowledge))
        print('Know mines',self.mines)
        print ('Safe Move Remainig',self.safes - self.moves_made)

        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_move = self.safes - self.moves_made

        if safe_move:
            print("Making a safe move! safes moves available",len(safe_move))
            return random.choice(list(safe_move))


        return None

    
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves={}
        Mines=8
        
        num_mines_left= Mines - len(self.mines)
        space_left= (self.height * self.width)-(len(self.moves_made)+ len(self.mines))

        if space_left==0:
            return None

        basic_pr=num_mines_left/space_left

        for i in range(0,self.height):
            for j in range(0,self.width):
                if(i,j) not in self.moves_made and (i,j) not in self.mines:
                    moves[(i,j)]=basic_pr

        if moves and not self.knowledge:
            move= random.choice(list(moves.keys()))
            print('AI selecting random move wwith basic probbility',move)
            return move

        elif moves:
            for sentence in self.knowledge:
                num_cells= len(sentence.cells)
                count=sentence.count
                min_pro= count / num_cells

                for cell in sentence.cells:
                    if moves[cell]< min_pro:
                        moves[cell]=min_pro
            
            move_list=[[x,moves[x]] for x in moves]
            move_list.sort(key=lambda x:x[1])
            bast_por=move_list[0][1]

            bast_move=[x for x in move_list if x[1]==bast_por]
            move=random.choice(bast_move)[0]
            print('AI selcting random move wwith mine proabability uusing KB:',move)

            return move



    


        
