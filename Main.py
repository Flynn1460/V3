import ChessEngine as ce
import chess as ch

class Main:

    def __init__(self, board=ch.Board):
        self.board = board

    def printLegalMoves(self):
        print("\nLegal Move List : " + str(self.board.legal_moves)[37:-1])
        pass

    #Player's Turn
    def playHumanMove(self):
        try:

            self.printLegalMoves()

            play = input("Your move: ")
            
            self.board.push_san(play)

        except:
            self.playHumanMove()

    #Engine's Turn
    def playEngineMove(self, maxDepth, color):
        engine = ce.Engine(self.board, maxDepth, color)

        self.board.push(engine.getBestMove())

    #start a game
    def startGame(self):
        #get human player's color
        color, maxDepth = None, None
        while color != "b" and color != "w" and not isinstance(maxDepth, int):
            color = input("Play as (type 'b' or 'w'): ")
            maxDepth = int(input("Choose depth: "))+1

        if color=="b":
            while (self.board.is_checkmate()==False):
                print("The engine is thinking...")
                self.playEngineMove(maxDepth, ch.WHITE)
                print(self.board)
                self.playHumanMove()
                print(self.board)
            print(self.board)
            print(self.board.outcome())    
        elif color=="w":
            while (self.board.is_checkmate()==False):
                print(self.board)
                self.playHumanMove()
                print(self.board)
                print("The engine is thinking...")
                self.playEngineMove(maxDepth, ch.BLACK)
            print(self.board)
            print(self.board.outcome())
        #reset the board
        self.board.reset
        #start another game
        self.startGame()

#create an instance and start a game
newBoard= ch.Board()
game = Main(newBoard)
bruh = game.startGame()
