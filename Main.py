import chess as ch, ChessEngine as ce

class Main:

    def __init__(self, board):
        self.board = board
        self.colour, self.maxDepth = None, -1
        self.gamePlayer = 1

    def printLegalMoves(self):
        print("\nLegal Move List : " + str(self.board.legal_moves)[37:-1])

    def resetGame(self):
        self.board.reset
        self.startGame()
        self.colour, self.maxDepth = ch.WHITE, None

    def gameOver(self):
        print(self.board)
        print(self.board.outcome)

    def playMove(self, turnFirst, boardPrint):
        if turnFirst ==  "comp":
            self.playEngineMove(ch.WHITE)
            print(self.board)
            self.playEngineMove(ch.BLACK)


        elif turnFirst:
            if self.colour == "w":
                self.playHumanMove()
            
            elif self.colour == "b":

                self.colour = "w"
                self.playEngineMove(ch.WHITE)
            
        elif not turnFirst:
            if self.colour == "w":

                self.colour = "b"
                self.playEngineMove(ch.BLACK)
            
            elif self.colour == "b":
                self.playHumanMove()
        
        if boardPrint:
            print(self.board)

    #Player's Turn
    def playHumanMove(self):
        try:
            self.printLegalMoves()

            play = input("Your move : ")
            self.board.push_san(play)

        except:
            self.playHumanMove()

    #Engine's Turn
    def playEngineMove(self, colour):
        print("Processing...")

        engine = ce.Engine(self.board, self.maxDepth)

        self.board.push(engine.getBestMove(colour))

    #Run Game
    def startGame(self):
        # Get player information

        while True:
            try:
                self.gamePlayer = int(input("Singleplayer (1), Computer vs Computer (0) : "))
                if self.gamePlayer == 0 or self.gamePlayer == 1:
                    self.gamePlayer = bool(self.gamePlayer)
                    break
                    
                else:
                    continue
            
            except:
                continue

        while not self.maxDepth > 1:
            try:
                if self.gamePlayer:
                    while self.colour != "w" and self.colour != "b":
                        self.colour = input("Play as (type 'w' or 'b'): ")

                self.maxDepth = int(input("Choose engine depth (recommended 4) : ")) # Note: Depth needs to be bumped by 1 to prevent errors

            except ValueError:
                print("ERROR: Invalid Depth, set value to 4")
                self.maxDepth = 4


        print(str(self.board)+"\n")



        while not self.board.is_checkmate():
            if not self.gamePlayer:
                self.playMove("comp", True)

            if self.gamePlayer:
                self.playMove(True, True)
                self.playMove(False, True)

        self.gameOver()
        self.resetGame()


#create an instance and start a game
newBoard = ch.Board()
game = Main(newBoard)
runGame = game.startGame()