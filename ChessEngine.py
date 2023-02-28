import chess as ch
import random as rd

class Engine:

    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

        self.pieces = {
            None : "0",
            ch.KING : "0",
            ch.PAWN : "1",
            ch.BISHOP : "3",
            ch.KNIGHT : "3",
            ch.ROOK : "5",
            ch.QUEEN : "9"
        }

    def evalFunct(self):
        #Sums up the material values

        compt = 0
        for i in range(64):
            compt += self.squareValue(i)

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
    def squareValue(self, square):
        pieceValue = int(self.pieces[self.board.piece_type_at(square)])

        if self.board.color_at(square) != self.color:
            return -pieceValue
        
        else:
            return pieceValue

    # Min Max Algorithm      
    def engine(self, candidate, depth):
        
        #If max depth is reached or no legal moves are possible
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            # Go with our function evaluation
            return self.evalFunct()
        
        else:
            moveList = list(self.board.legal_moves)
            bestMove = None
            engineTurn = depth % 2 != 0

            #If engine's turn try to maximise the position
            if not engineTurn:
                bestMove = float("inf")

            else:
                bestMove = float("-inf")
            
            #analyse board after deeper moves
            for i in moveList:

                #Play the move in our depth sequence
                self.board.push(i)

                #Rerun the program as a nested function
                currentMove = self.engine(bestMove, depth + 1) 

                #Basic minmax algorithm:
                #If engine's turn see if the value is better than our best move
                if currentMove > bestMove and engineTurn:

                    if depth == 1:
                        move = i

                    bestMove = currentMove

                #If human's turn see if the value is better than our best move
                elif currentMove < bestMove and not engineTurn:
                    bestMove = currentMove

                #Alpha-beta prunning cuts: 
                #(if previous move was made by the engine)
                if candidate != None and currentMove < candidate and not engineTurn:

                    self.board.pop()
                    break

                #(if previous move was made by the human player)
                elif candidate != None and currentMove > candidate and engineTurn:
                    
                    self.board.pop()
                    break
                
                #Undo last move
                self.board.pop()

            #Return result
            if depth > 1:
                #eturn value of a move in the tree
                return bestMove
            else:
                #return the move (only on first move)
                return move

    # Polish Engine
    def getBestMove(self):
        return self.engine(None, 1)