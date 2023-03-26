from game import Game
from client import Client
if __name__ == '__main__':
    # client = Client()
    # client.connect()

    game = Game()
    game.launch()

    client = Client()
    client.play()
