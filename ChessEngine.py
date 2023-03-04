import chess as ch
import random as rd

class OtherFuncs:
    def  __init__(self):
        pass

    def flipColour(self, colour):
        if colour == ch.WHITE:
            return ch.BLACK
        if colour == ch.BLACK:
            return ch.WHITE


class PieceMaps:
    def __init__(self, board):
        self.board = board

        self.pieceRef = {
            "1" : "Pawn",
            "2" : "Knight",
            "3" : "Bishop",
            "4" : "Rook",
            "5" : "King",
            "6" : "Queen",
            "None" : "Blank"
        }

        self.enginePawnMap =  [
            .0, .0, .0, .0, .0, .0, .0, .0,
            .1, .1, .1, .1, .1, .1, .1, .1,
            .1, .2, .2, .2, .2, .2, .2, .2,
            .2, .3, .4, .6, .6, .4, .3, .2,
            .2, .3, .4, .6, .6, .4, .3, .2,
            .1, .2, .2, .2, .2, .2, .2, .2,
            .1, .1, .1, .1, .1, .1, .1, .1,
            .0, .0, .0, .0, .0, .0, .0, .0,
        ]

    def getSquareItem(self, square):
        squarePiece = self.pieceRef[str(self.board.piece_type_at(square))]

        if squarePiece == "Pawn":
            return float(self.enginePawnMap[square])
        
        elif squarePiece == "Blank":
            return 0
        
        else:
            return 0


class EvaluatePosition:
    def __init__(self, board, colour):
        self.board = board
        self.colour = colour

        self.littleTools = OtherFuncs()

        self.pieces = {
            None : "0",
            ch.KING : "0",
            ch.PAWN : "1",
            ch.BISHOP : "3",
            ch.KNIGHT : "3",
            ch.ROOK : "5",
            ch.QUEEN : "9"
        }

    # Mating Threats
    def mateOpportunity(self, colour):
        if self.board.legal_moves.count() == 0:

            if self.board.turn == colour:
                return float("-inf")
            
            else:
                return float("inf")
            
        else:
            return 0

    # Attach a square to a value
    def squareValue(self, square, colour):
        pieceValue = int(self.pieces[self.board.piece_type_at(square)])


        if self.board.color_at(square) == colour:
            return pieceValue * -1
    
        elif self.board.color_at(square) == self.littleTools.flipColour(colour):
            return pieceValue

        else:
            return 0
      


    # Evaluate the position    
    def evalPosition(self, colour):
        #Sums up the material values

        newMap = PieceMaps(self.board)


        compt = 0
        for i in range(64):
            compt += self.squareValue(i, colour)

        compt += self.mateOpportunity(colour)

        return compt


class Engine:

    def __init__(self, board, maxDepth):
        self.board = board
        self.maxDepth = maxDepth
        self.totPossMoves = 0

        self.littleTools = OtherFuncs()

    def alphaBetaPruning(self, candidate, currentMove, engineTurn):
        #Alpha-beta prunning cuts: 
        #(if previous move was made by the engine)
        if candidate != None and currentMove < candidate and not engineTurn:
            self.board.pop()
            return

        #(if previous move was made by the human player)
        elif candidate != None and currentMove > candidate and engineTurn:
            self.board.pop()
            return

    # Min Max Algorithm      
    def engine(self, candidate, depth, colour):
        
        #If max depth is reached or no legal moves are possible
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            # Go with our function evaluation
            self.totPossMoves += 1

            boardEval = EvaluatePosition(self.board, colour)

            return boardEval.evalPosition(self)
        
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
                currentMove = self.engine(bestMove, depth + 1, self.littleTools.flipColour(colour)) 

                #Basic minmax algorithm:
                #If engine's turn see if the value is better than our best move
                if currentMove > bestMove and engineTurn:

                    if depth == 1:
                        move = i

                    bestMove = currentMove

                #If human's turn see if the value is better than our best move
                elif currentMove < bestMove and not engineTurn:
                    bestMove = currentMove

                self.alphaBetaPruning(candidate, currentMove, engineTurn)
                
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
    def getBestMove(self, colour):
        engineResults = self.engine(None, 1, colour)

        print(self.maxDepth, " - ", self.totPossMoves)
        self.totPossMoves = 0

        return engineResults