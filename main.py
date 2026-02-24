# Imports
import pygame as pg
import game


def main():
    # Kicks off program
    g = game.Game()
    # Shows main menu
    g.startScreen()
    while g.running:
        # Restarts game
        g.start()
        # Runs game loop
        g.run()
        # Shows game end screen
        g.endScreen()


main()
# Ends program
pg.quit()
quit()
