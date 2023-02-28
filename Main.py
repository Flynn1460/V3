import ChessEngine as ce
import chess as ch

class Main:

    def __init__(self, board=ch.Board):
        self.board = board

    def printLegalMoves(self):
        print("\nLegal Move List : " + str(self.board.legal_moves)[37:-1])
        pass

    def resetGame(self):
        #reset the board
        self.board.reset
        #start another game
        self.startGame()
    
    def gameOver(self):
        print(self.board)
        print(self.board.outcome)

    def playMove(self, colour, turnFirst):
        if turnFirst:
            if colour == "w":
                self.playHumanMove()
            
            elif colour == "b":
                self.playEngineMove(ch.BLACK)
            
        elif not turnFirst:
            if colour == "w":
                self.playEngineMove(ch.WHITE)
            
            elif colour == "b":
                self.playHumanMove()


    #Player's Turn
    def playHumanMove(self):
        try:

            self.printLegalMoves()

            play = input("Your move: ")
            
            self.board.push_san(play)

        except:
            self.playHumanMove()
            
            print(self.board)
            print(self.board.outcome())  


    #Engine's Turn
    def playEngineMove(self, colour):
        print("The engine is thinking...")

        engine = ce.Engine(self.board, self.maxDepth, colour)

        self.board.push(engine.getBestMove())

    #start a game
    def startGame(self):
        # Get player information

        colour, self.maxDepth = None, None
        while colour != "b" and colour != "w" and not isinstance(self.maxDepth, int):
            colour = input("Play as (type 'b' or 'w'): ")
            self.maxDepth = int(input("Choose depth: "))+1 # Note: Depth needs to be bumped by 1 to prevent errors

        print(self.board)


        while not self.board.is_checkmate():

            if colour == "b":
                self.playEngineMove(ch.WHITE)
                print(self.board)

                self.playHumanMove()
                print(self.board)

            if colour == "w":
                self.playHumanMove()
                print(self.board)

                self.playEngineMove(ch.BLACK)
                print(self.board)
            


        self.gameOver()
        self.resetGame()

#create an instance and start a game
newBoard= ch.Board()
game = Main(newBoard)
bruh = game.startGame()
