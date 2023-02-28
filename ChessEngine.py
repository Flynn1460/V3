import chess as ch
import random as rd

class Engine:

    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

    def evalFunct(self):
        #Sums up the material values

        compt = 0
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])

        compt += self.mateOpportunity() + 0.001 * rd.random()
        return compt

    def mateOpportunity(self):
        if self.board.legal_moves.count() == 0:

            if self.board.turn == self.color:
                return float("-inf")
            
            else:
                return float("inf")
            
        else:
            return 0

    # Attach a square to a value
    def squareResPoints(self, square):
        pieceValue = 0
        if(self.board.piece_type_at(square) == ch.PAWN):
            pieceValue = 1
        elif (self.board.piece_type_at(square) == ch.ROOK):
            pieceValue = 5.1
        elif (self.board.piece_type_at(square) == ch.BISHOP):
            pieceValue = 3.33
        elif (self.board.piece_type_at(square) == ch.KNIGHT):
            pieceValue = 3.2
        elif (self.board.piece_type_at(square) == ch.QUEEN):
            pieceValue = 8.8

        if (self.board.color_at(square)!=self.color):
            return -pieceValue
        else:
            return pieceValue

        
    def engine(self, candidate, depth):
        
        #reached max depth of search or no possible moves
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evalFunct()
        
        else:
            #get list of legal moves of the current position
            moveList = list(self.board.legal_moves)
            
            #initialise newCandidate
            newCandidate = None
            #(uneven depth means engine's turn)
            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            
            #analyse board after deeper moves
            for i in moveList:

                #Play move i
                self.board.push(i)

                #Get value of move i (by exploring the repercussions)
                value = self.engine(newCandidate, depth + 1) 

                #Basic minmax algorithm:
                #if maximizing (engine's turn)
                if(value > newCandidate and depth % 2 != 0):
                    #need to save move played by the engine
                    if (depth == 1):
                        move=i
                    newCandidate = value
                #if minimizing (human player's turn)
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value

                #Alpha-beta prunning cuts: 
                #(if previous move was made by the engine)
                if (candidate != None
                 and value < candidate
                 and depth % 2 == 0):
                    self.board.pop()
                    break
                #(if previous move was made by the human player)
                elif (candidate != None 
                and value > candidate 
                and depth % 2 != 0):
                    self.board.pop()
                    break
                
                #Undo last move
                self.board.pop()

            #Return result
            if (depth>1):
                #eturn value of a move in the tree
                return newCandidate
            else:
                #return the move (only on first move)
                return move

    # Polish Engine
    def getBestMove(self):
        return self.engine(None, 1)