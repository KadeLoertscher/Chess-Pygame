# Imports
from pieces import *


def draw(surface, text, size, x, y, color=WHITE, outline=False, outCol=BLACK):
    """Draws text to a screen with a given font size and x and y coords. If no color is passed in, the text will be
     white by default"""
    font = pg.font.Font(FONT, size)
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.midtop = (x, y)
    if outline:
        outMask = pg.mask.from_surface(textSurf)
        maskSurf = outMask.to_surface(setcolor=outCol, unsetcolor=A_COL)
        maskSurf.set_colorkey(A_COL)

        surface.blit(maskSurf, (textRect.x - 1, textRect.y))
        surface.blit(maskSurf, (textRect.x + 1, textRect.y))
        surface.blit(maskSurf, (textRect.x, textRect.y - 1))
        surface.blit(maskSurf, (textRect.x, textRect.y + 1))

    surface.blit(textSurf, textRect)


class Game:
    def __init__(self):
        # Inits pygame
        pg.init()
        pg.mixer.init()
        # Creates game objects
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        # Loads files
        self.load()

    def load(self):
        # Loads white piece imgs
        self.whiteImgs = []
        for i in range(6):
            img = pg.image.load(os.path.join(imagesFolder, "w_{}_2x_ns.png".format(
                ["pawn", "bishop", "knight", "rook", "queen", "king"][i]))).convert_alpha()
            img = pg.transform.scale(img, (TILE_WIDTH // 2, TILE_HEIGHT // 2))
            self.whiteImgs.append(img)
        # Loads black piece imgs
        self.blackImgs = []
        for i in range(6):
            img = pg.image.load(os.path.join(imagesFolder, "b_{}_2x_ns.png".format(
                ["pawn", "bishop", "knight", "rook", "queen", "king"][i]))).convert_alpha()
            img = pg.transform.scale(img, (TILE_WIDTH // 2, TILE_HEIGHT // 2))
            self.blackImgs.append(img)
        # Loads gradient img
        self.gradientImg = pg.image.load(os.path.join(imagesFolder, "gradient_img.png")).convert_alpha()
        self.gradientImg = pg.transform.scale(self.gradientImg, (TILE_WIDTH, TILE_HEIGHT))
        self.dim = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim.fill(DIM)

    def start(self):
        # Creates sprite groups
        self.allSprites = pg.sprite.LayeredUpdates()
        self.whiteGroup = pg.sprite.Group()
        self.blackGroup = pg.sprite.Group()
        self.selectGroup = pg.sprite.Group()
        # Makes starting pawns
        for x in range(8):
            Pawn(self, "black", x, 1, 0)
        for x in range(8):
            Pawn(self, "white", x, 6, 0)
        # Makes starting bishops
        for x in [2, 5]:
            Bishop(self, "black", x, 0, 1)
        for x in [2, 5]:
            Bishop(self, "white", x, 7, 1)
        # Makes starting knights
        for x in [1, 6]:
            Knight(self, "black", x, 0, 2)
        for x in [1, 6]:
            Knight(self, "white", x, 7, 2)
        # Makes starting rooks
        for x in [0, 7]:
            Rook(self, "black", x, 0, 3)
        for x in [0, 7]:
            Rook(self, "white", x, 7, 3)
        # Makes starting queens
        Queen(self, "black", 3, 0, 4)
        Queen(self, "white", 3, 7, 4)
        # Makes starting kings
        King(self, "black", 4, 0, 5)
        King(self, "white", 4, 7, 5)
        # White starts
        self.wTurn = True
        self.gameEnd = False

    def run(self):
        self.playing = True
        # Main game loop
        while self.playing:
            # Ticks clock
            self.clock.tick(FPS)
            # Checks for events
            self.checkEvents()
            # Updates sprites
            self.update()
            # Draws sprites to screen
            self.draw()

    def gameOver(self):
        self.gameEnd = True

    def inside(self, pos, rect):
        # Checks if a pos is inside a rect and returns true or false depending on the result
        if pos[0] >= rect.x and pos[1] >= rect.y:
            if pos[0] <= rect.right and pos[1] <= rect.bottom:
                return True
        return False

    def getGridPos(self, pos):
        # Gets the grid position of a pos based on a pixel position
        # Starts at -1, -1 (not inside grid at all)
        xpos = -1
        ypos = -1
        # Makes sure pos is in the grid
        if (TILE_OFFSET_X < pos[0] < WIDTH - TILE_OFFSET_X) and (TILE_OFFSET_Y < pos[1] < HEIGHT - TILE_OFFSET_Y):
            # Finds the x position
            for i in range(1, BOARD_COLS + 1):
                if pos[0] < (BOARD_WIDTH * i / BOARD_COLS) + TILE_OFFSET_X:
                    xpos = i - 1
                    break
            # Finds the y position
            for i in range(1, BOARD_ROWS + 1):
                if pos[1] < (BOARD_HEIGHT * i / BOARD_ROWS) + TILE_OFFSET_Y:
                    ypos = i - 1
                    break
        # Returns the found position as a list
        return [xpos, ypos]

    def selectPiece(self, mpos):
        # Finds a piece based on the square that was clicked
        # Gets mouse's grid pos
        mposGrid = self.getGridPos(mpos)
        # Makes sure mouse is in grid
        if mposGrid[0] >= 0 and mposGrid[1] >= 0:
            if self.wTurn:
                group = self.whiteGroup
            else:
                group = self.blackGroup
            # Checks to see if any king is in check
            inCheck = False
            for sprite in group:
                if isinstance(sprite, King):
                    if sprite.inCheck:
                        inCheck = True
            # Goes through each piece of whose turn it is
            for sprite in group:
                # Sees if there is a piece where the player clicked
                if sprite.x == mposGrid[0] and sprite.y == mposGrid[1]:
                    # Sees if player clicked on their current selection
                    for select in self.selectGroup:
                        if select.x == mposGrid[0] and select.y == mposGrid[1]:
                            # Removes selection
                            select.kill()
                            return
                    # Sees if there is already another selection
                    if len(self.selectGroup) > 0:
                        for select in self.selectGroup:
                            # Removes selection
                            select.kill()
                    if inCheck:
                        pass
                    # Makes selection square
                    s = Selection(self, mposGrid[0], mposGrid[1])
                    self.selectGroup.add(s)
                    # Returns player selected a piece
                    return True
        # Returns player may be moving a piece
        return False

    def getSelected(self):
        # Finds the currently selected sprite
        if len(self.selectGroup) > 0:
            for sprite in self.allSprites:
                if sprite not in self.selectGroup:
                    for select in self.selectGroup:
                        if sprite.x == select.x and sprite.y == select.y:
                            # Returns selected sprite
                            return sprite
        else:
            # No sprite is selected
            return None

    def swapTurn(self):
        # Swaps turn
        self.wTurn = not self.wTurn

    def checkEvents(self):
        # Checks for events
        for event in pg.event.get():
            # Close button (quits program)
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            # Mouse release (selects / moves piece)
            if event.type == pg.MOUSEBUTTONUP:
                # Gets pos of mouse
                mouse = pg.mouse.get_pos()
                mouseGrid = self.getGridPos(mouse)
                # Selects piece
                selecting = self.selectPiece(mouse)
                # Moves piece if player didn't just select a piece
                if not selecting:
                    # Gets selected piece
                    selected = self.getSelected()
                    # If a piece is selected
                    if selected:
                        # Gets rid of selection
                        for select in self.selectGroup:
                            select.kill()
                        # Moves selected piece and makes sure it stays in the grid
                        if mouseGrid[0] >= 0 and mouseGrid[1] >= 0:
                            # Castling for a king
                            if isinstance(selected, King):
                                if (mouseGrid[0], mouseGrid[1]) in selected.castleMoves:
                                    # Moves the correct rook to the correct side of the king
                                    if mouseGrid[0] > selected.x:
                                        for sprite in selected.sameGroup:
                                            if isinstance(sprite, Rook):
                                                if sprite.x > selected.x:
                                                    sprite.x = mouseGrid[0] - 1
                                                    selected.x = mouseGrid[0]
                                    else:
                                        for sprite in selected.sameGroup:
                                            if isinstance(sprite, Rook):
                                                if sprite.x < selected.x:
                                                    sprite.x = mouseGrid[0] + 1
                                                    selected.x = mouseGrid[0]
                            selected.move(mouseGrid[0], mouseGrid[1])

    def update(self):
        # Updates all sprites
        self.allSprites.update()
        # White takes a piece
        if not self.wTurn:
            hits = pg.sprite.groupcollide(self.blackGroup, self.whiteGroup, False, False)
            for hit in hits:
                if hit in self.blackGroup:
                    hit.kill()
        # Black takes a piece
        else:
            hits = pg.sprite.groupcollide(self.whiteGroup, self.blackGroup, False, False)
            for hit in hits:
                if hit in self.whiteGroup:
                    hit.kill()

    def drawGrid(self):
        # Draws grid of alternating colors
        alt = 0
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                # Gets color
                if alt % 2 == 0:
                    color = COL1
                else:
                    color = COL2
                # Creates tile
                square = pg.Surface((TILE_WIDTH, TILE_HEIGHT))
                square.fill(color)
                squareRect = square.get_rect()
                squareRect.topleft = ((col * TILE_WIDTH) + TILE_OFFSET_X, (row * TILE_HEIGHT) + TILE_OFFSET_Y)
                self.screen.blit(square, squareRect)
                # Alternates color
                alt += 1
            # Alternates color between rows
            alt += 1

    def draw(self):
        # Fills screen with bg color
        self.screen.fill(BG_COLOR)
        # Draws grid
        self.drawGrid()
        # Draws possible moves if a piece is selected
        selected = self.getSelected()
        if selected:
            # Gets possible moves of piece
            for pos in selected.getMoves():
                # Draws a highlight square to show movement
                x = pos[0]
                y = pos[1]
                s = pg.Surface((TILE_WIDTH, TILE_HEIGHT))
                sRect = s.get_rect()
                sRect.x = x * TILE_WIDTH + TILE_OFFSET_X
                sRect.y = y * TILE_HEIGHT + TILE_OFFSET_Y
                color = S_BLUE
                for sprite in self.allSprites:
                    if sprite not in self.selectGroup:
                        # Makes square red if there is an opposing piece where movement is possible
                        if sprite.x == x and sprite.y == y:
                            color = S_RED
                            break
                        # Square is a castle movement
                        if isinstance(selected, King):
                            if (x, y) in selected.castleMoves:
                                color = S_VIOLET
                                break
                s.fill(color)
                s.set_alpha(HIGHLIGHT_A)
                self.screen.blit(s, sRect)
        # Draws gradients of kings in check
        for sprite in self.allSprites:
            if isinstance(sprite, King):
                if sprite.inCheck:
                    gRect = self.gradientImg.get_rect()
                    gRect.center = sprite.rect.center
                    self.screen.blit(self.gradientImg, gRect)

        # Draws all sprites
        self.allSprites.draw(self.screen)
        # Shows current turn
        if self.wTurn:
            draw(self.screen, "White's Turn", 30, WIDTH / 2, TILE_OFFSET_Y / 2, WHITE, True)
        else:
            draw(self.screen, "Black's Turn", 30, WIDTH / 2, TILE_OFFSET_Y / 2, BLACK, True, WHITE)
        # Shows if the game is over
        if self.gameEnd:
            draw(self.screen, "Checkmate", 80, BOARD_WIDTH / 2 + TILE_OFFSET_X, BOARD_HEIGHT / 2 + TILE_OFFSET_Y - 40,
                 RED, True, BLACK)
        pg.display.flip()

    def pawnMenu(self, pawn):
        # Dims screen
        self.screen.blit(self.dim, (0, 0))
        # Gets colors of buttons for each color
        if pawn.color == "white":
            col = WHITE
            outCol = BLACK
            backCol = WHITE_A
            imgs = self.whiteImgs.copy()
        else:
            col = BLACK
            outCol = WHITE
            backCol = BLACK_A
            imgs = self.blackImgs.copy()
        # Scales new imgs for buttons
        for i in range(len(imgs)):
            imgs[i] = pg.transform.scale(imgs[i], (50, 50))

        # Draws menu ui
        draw(self.screen, "Choose a piece:", 60, WIDTH / 2, HEIGHT / 4, col, True, outCol)
        # Queen circle
        tSurfQ = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        pg.draw.circle(self.screen, col, (WIDTH / 5, HEIGHT / 2), 50, 3)
        pg.draw.circle(tSurfQ, backCol, (WIDTH / 5, HEIGHT / 2), 50)
        self.screen.blit(tSurfQ, (0, 0))
        self.screen.blit(imgs[4], (WIDTH / 5 - imgs[4].get_size()[0] / 2,
                                   HEIGHT / 2 - imgs[4].get_size()[1] / 2))
        # Rook circle
        tSurfR = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        pg.draw.circle(self.screen, col, (WIDTH * 2 / 5, HEIGHT / 2), 50, 3)
        pg.draw.circle(tSurfR, backCol, (WIDTH * 2 / 5, HEIGHT / 2), 50)
        self.screen.blit(tSurfR, (0, 0))
        self.screen.blit(imgs[3], (WIDTH * 2 / 5 - imgs[3].get_size()[0] / 2,
                                   HEIGHT / 2 - imgs[3].get_size()[1] / 2))
        # Bishop circle
        tSurfB = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        pg.draw.circle(self.screen, col, (WIDTH * 3 / 5, HEIGHT / 2), 50, 3)
        pg.draw.circle(tSurfB, backCol, (WIDTH * 3 / 5, HEIGHT / 2), 50)
        self.screen.blit(tSurfB, (0, 0))
        self.screen.blit(imgs[1], (WIDTH * 3 / 5 - imgs[1].get_size()[0] / 2,
                                   HEIGHT / 2 - imgs[1].get_size()[1] / 2))
        # Knight circle
        tSurfK = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        pg.draw.circle(self.screen, col, (WIDTH * 4 / 5, HEIGHT / 2), 50, 3)
        pg.draw.circle(tSurfK, backCol, (WIDTH * 4 / 5, HEIGHT / 2), 50)
        self.screen.blit(tSurfK, (0, 0))
        self.screen.blit(imgs[2], (WIDTH * 4 / 5 - imgs[2].get_size()[0] / 2,
                                   HEIGHT / 2 - imgs[2].get_size()[1] / 2))
        # Waiting in menu
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            # Checks for events
            for event in pg.event.get():
                # Close button (quits program)
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                    quit()
                    pg.quit()
                # Hover over a choice button (changes outline color)
                if event.type == pg.MOUSEMOTION:
                    mouse = pg.mouse.get_pos()
                    # Queen button
                    if self.inside(mouse, pg.Rect((WIDTH / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        pg.draw.circle(self.screen, outCol, (WIDTH / 5, HEIGHT / 2), 50, 3)
                    else:
                        pg.draw.circle(self.screen, col, (WIDTH / 5, HEIGHT / 2), 50, 3)
                    # Rook button
                    if self.inside(mouse, pg.Rect((WIDTH * 2 / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        pg.draw.circle(self.screen, outCol, (WIDTH * 2 / 5, HEIGHT / 2), 50, 3)
                    else:
                        pg.draw.circle(self.screen, col, (WIDTH * 2 / 5, HEIGHT / 2), 50, 3)
                    # Bishop button
                    if self.inside(mouse, pg.Rect((WIDTH * 3 / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        pg.draw.circle(self.screen, outCol, (WIDTH * 3 / 5, HEIGHT / 2), 50, 3)
                    else:
                        pg.draw.circle(self.screen, col, (WIDTH * 3 / 5, HEIGHT / 2), 50, 3)
                    # Knight button
                    if self.inside(mouse, pg.Rect((WIDTH * 4 / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        pg.draw.circle(self.screen, outCol, (WIDTH * 4 / 5, HEIGHT / 2), 50, 3)
                    else:
                        pg.draw.circle(self.screen, col, (WIDTH * 4 / 5, HEIGHT / 2), 50, 3)
                # Clicked a button (chooses a new piece)
                if event.type == pg.MOUSEBUTTONUP:
                    mouse = pg.mouse.get_pos()
                    # Queen button
                    if self.inside(mouse, pg.Rect((WIDTH / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        Queen(self, pawn.color, pawn.x, pawn.y, 4)
                        pawn.kill()
                        waiting = False
                    # Rook button
                    if self.inside(mouse, pg.Rect((WIDTH * 2 / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        Rook(self, pawn.color, pawn.x, pawn.y, 3)
                        pawn.kill()
                        waiting = False
                    # Bishop button
                    if self.inside(mouse, pg.Rect((WIDTH * 3 / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        Bishop(self, pawn.color, pawn.x, pawn.y, 1)
                        pawn.kill()
                        waiting = False
                    # Knight button
                    if self.inside(mouse, pg.Rect((WIDTH * 4 / 5 - 50, HEIGHT / 2 - 50), (100, 100))):
                        Knight(self, pawn.color, pawn.x, pawn.y, 2)
                        pawn.kill()
                        waiting = False

            pg.display.flip()
        # Sees if king is now in check
        for sprite in pawn.oppGroup:
            if isinstance(sprite, King):
                sprite.checkCheck()
                break

    def startScreen(self):
        pass

    def endScreen(self):
        pass
