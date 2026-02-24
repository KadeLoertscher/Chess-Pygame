# Imports
from settings import *


def checkSameColor(piece, x, y):
    # Makes sure spot isn't occupied by friendly piece
    sameCol = False
    for sprite in piece.sameGroup:
        if sprite != piece:
            if sprite.x == x and sprite.y == y:
                sameCol = True
    return sameCol


def getDiagonals(piece):
    # List holding all diagonals
    allDiag = []
    # Gets up and right diagonal squares
    gx = piece.x + 1
    gy = piece.y - 1
    while gx < BOARD_COLS and gy > -1:
        allDiag.append((gx, gy))
        gx += 1
        gy -= 1
    # Gets up and left diagonal squares
    gx = piece.x - 1
    gy = piece.y - 1
    while gx > -1 and gy > -1:
        allDiag.append((gx, gy))
        gx -= 1
        gy -= 1
    # Gets down and left diagonal squares
    gx = piece.x - 1
    gy = piece.y + 1
    while gx > -1 and gy < BOARD_ROWS:
        allDiag.append((gx, gy))
        gx -= 1
        gy += 1
    # Gets down and right diagonal squares
    gx = piece.x + 1
    gy = piece.y + 1
    while gx < BOARD_COLS and gy < BOARD_ROWS:
        allDiag.append((gx, gy))
        gx += 1
        gy += 1
    # Checks for pieces in diagonals
    for sprite in piece.game.allSprites:
        if sprite not in piece.game.selectGroup:
            for pos in allDiag:
                # Gets what diagonal sprite is in
                if (sprite.x, sprite.y) == pos:
                    sIndex = allDiag.index((sprite.x, sprite.y))
                    if sprite.x < piece.x:
                        sDirX = "left"
                    else:
                        sDirX = "right"
                    if sprite.y < piece.y:
                        sDirY = "up"
                    else:
                        sDirY = "down"
                    # Removes any squares that are after the sprite
                    while True:
                        # Goes through each pos in diagonals after the sprite's pos in the list and removes it
                        try:
                            curPos = allDiag[sIndex]
                        # Sprite is at edge of board
                        except IndexError:
                            break
                        # Gets what diagonal the next pos is in
                        if curPos[0] < piece.x:
                            cDirX = "left"
                        else:
                            cDirX = "right"
                        if curPos[1] < piece.y:
                            cDirY = "up"
                        else:
                            cDirY = "down"
                        # Stops removing positions if the next pos is in a new diagonal
                        if cDirX != sDirX or cDirY != sDirY:
                            break
                        allDiag.remove(curPos)
                    break
    # Makes list of extra positions to add
    extraPos = []
    # Looks for opposing pieces around piece and adds them to the extra positions if there are any
    for sprite in piece.oppGroup:
        if sprite.x == piece.x + 1 and sprite.y == piece.y - 1:
            extraPos.append((sprite.x, sprite.y))
        if sprite.x == piece.x + 1 and sprite.y == piece.y + 1:
            extraPos.append((sprite.x, sprite.y))
        if sprite.x == piece.x - 1 and sprite.y == piece.y - 1:
            extraPos.append((sprite.x, sprite.y))
        if sprite.x == piece.x - 1 and sprite.y == piece.y + 1:
            extraPos.append((sprite.x, sprite.y))
    # Adds opposing pieces that may be on the end of a diagonal
    for pos in allDiag:
        # Gets diagonal of pos
        if pos[0] < piece.x:
            pDirX = "left"
        else:
            pDirX = "right"
        if pos[1] < piece.y:
            pDirY = "up"
        else:
            pDirY = "down"
        # Sees what positions are at the end of their diagonals
        try:
            nextPos = allDiag[allDiag.index(pos) + 1]
            if nextPos[0] < piece.x:
                nDirX = "left"
            else:
                nDirX = "right"
            if nextPos[1] < piece.y:
                nDirY = "up"
            else:
                nDirY = "down"
            if pDirX != nDirX or pDirY != nDirY:
                endPoint = {"pos": pos, "dirX": pDirX, "dirY": pDirY}
            else:
                continue
        except IndexError:
            endPoint = {"pos": pos, "dirX": pDirX, "dirY": pDirY}
        # Sees if there is a sprite at the end of a diagonal
        for sprite in piece.oppGroup:
            if endPoint["dirX"] == "right":
                x = 1
            else:
                x = -1
            if endPoint["dirY"] == "up":
                y = -1
            else:
                y = 1
            # Adds sprites position to the extra positions
            if sprite.x == endPoint["pos"][0] + x and sprite.y == endPoint["pos"][1] + y:
                extraPos.append((sprite.x, sprite.y))
    # Adds the new-found positions to previous ones
    allDiag += extraPos
    # Returns the found moves
    return allDiag


def getStaights(piece):
    # List holding all straights
    allStrt = []
    # Gets right squares
    gx = piece.x + 1
    gy = piece.y
    while gx < BOARD_COLS:
        allStrt.append((gx, gy))
        gx += 1
    # Gets left squares
    gx = piece.x - 1
    while gx > -1:
        allStrt.append((gx, gy))
        gx -= 1
    # Gets down squares
    gx = piece.x
    gy = piece.y + 1
    while gy < BOARD_ROWS:
        allStrt.append((gx, gy))
        gy += 1
    # Gets up squares
    gy = piece.y - 1
    while gy > -1:
        allStrt.append((gx, gy))
        gy -= 1
    # Checks for pieces in straights
    for sprite in piece.game.allSprites:
        if sprite not in piece.game.selectGroup:
            for pos in allStrt:
                # Gets what straight sprite is in
                if (sprite.x, sprite.y) == pos:
                    sIndex = allStrt.index((sprite.x, sprite.y))
                    if sprite.x < piece.x:
                        sDirX = "left"
                        sDirY = "none"
                    elif sprite.x > piece.x:
                        sDirX = "right"
                        sDirY = "none"
                    elif sprite.y < piece.y:
                        sDirY = "up"
                        sDirX = "none"
                    else:
                        sDirY = "down"
                        sDirX = "none"
                    # Removes any squares that are after the sprite
                    while True:
                        # Goes through each pos in straights after the sprite's pos in the list and removes it
                        try:
                            curPos = allStrt[sIndex]
                        # Sprite is at edge of board
                        except IndexError:
                            break
                        # Gets what straight the next pos is in
                        if curPos[0] < piece.x:
                            cDirX = "left"
                            cDirY = "none"
                        elif curPos[0] > piece.x:
                            cDirX = "right"
                            cDirY = "none"
                        elif curPos[1] < piece.y:
                            cDirY = "up"
                            cDirX = "none"
                        else:
                            cDirY = "down"
                            cDirX = "none"
                        # Stops removing positions if the next pos is in a new straight
                        if cDirX != sDirX or cDirY != sDirY:
                            break
                        allStrt.remove(curPos)
                    break
    # Makes list of extra positions to add
    extraPos = []
    # Looks for opposing pieces around piece and adds them to the extra positions if there are any
    for sprite in piece.oppGroup:
        if sprite.x == piece.x + 1 and sprite.y == piece.y:
            extraPos.append((sprite.x, sprite.y))
        if sprite.x == piece.x - 1 and sprite.y == piece.y:
            extraPos.append((sprite.x, sprite.y))
        if sprite.x == piece.x and sprite.y == piece.y - 1:
            extraPos.append((sprite.x, sprite.y))
        if sprite.x == piece.x and sprite.y == piece.y + 1:
            extraPos.append((sprite.x, sprite.y))
    # Adds opposing pieces that may be on the end of a straight
    for pos in allStrt:
        # Gets straight of pos
        if pos[0] < piece.x:
            pDirX = "left"
            pDirY = "none"
        elif pos[0] > piece.x:
            pDirX = "right"
            pDirY = "none"
        elif pos[1] < piece.y:
            pDirY = "up"
            pDirX = "none"
        else:
            pDirY = "down"
            pDirX = "none"
        # Sees what positions are at the end of their straights
        try:
            nextPos = allStrt[allStrt.index(pos) + 1]
            if nextPos[0] < piece.x:
                nDirX = "left"
                nDirY = "none"
            elif nextPos[0] > piece.x:
                nDirX = "right"
                nDirY = "none"
            elif nextPos[1] < piece.y:
                nDirY = "up"
                nDirX = "none"
            else:
                nDirY = "down"
                nDirX = "none"
            if pDirX != nDirX or pDirY != nDirY:
                endPoint = {"pos": pos, "dirX": pDirX, "dirY": pDirY}
            else:
                continue
        except IndexError:
            endPoint = {"pos": pos, "dirX": pDirX, "dirY": pDirY}
        # Sees if there is a sprite at the end of a straight
        for sprite in piece.oppGroup:
            if endPoint["dirX"] == "right":
                x = 1
            elif endPoint["dirX"] == "left":
                x = -1
            else:
                x = 0
            if endPoint["dirY"] == "up":
                y = -1
            elif endPoint["dirY"] == "down":
                y = 1
            else:
                y = 0
            # Adds sprites position to the extra positions
            if sprite.x == endPoint["pos"][0] + x and sprite.y == endPoint["pos"][1] + y:
                extraPos.append((sprite.x, sprite.y))
    # Adds the new-found positions to previous ones
    allStrt += extraPos
    # Returns the found moves
    return allStrt


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


class Selection(pg.sprite.Sprite):
    def __init__(self, game, gx, gy):
        # Layer selects are on
        self._layer = S_LAYER
        # Groups selects are in
        self.allGroups = game.allSprites, game.selectGroup
        super(Selection, self).__init__(self.allGroups)
        # Gets img and rect of select
        self.image = pg.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.image.fill(S_GREEN)
        self.image.set_alpha(HIGHLIGHT_A)
        self.rect = self.image.get_rect()
        # Grid pos of select
        self.x = gx
        self.y = gy
        # Pixel pos of select
        self.rect.x = gx * TILE_WIDTH + TILE_OFFSET_X
        self.rect.y = gy * TILE_HEIGHT + TILE_OFFSET_Y


class Piece(pg.sprite.Sprite):
    def __init__(self, game, col, gx, gy, imgIndex):
        # Base piece class
        # Layer pieces are on
        self._layer = P_LAYER
        # Gets correct img and adds to correct groups based on color
        if col == "white":
            self.image = game.whiteImgs[imgIndex]
            self.allGroups = game.allSprites, game.whiteGroup
        else:
            self.image = game.blackImgs[imgIndex]
            self.allGroups = game.allSprites, game.blackGroup
        super(Piece, self).__init__(self.allGroups)
        self.game = game
        self.imgIndex = imgIndex
        # Color of piece
        self.color = col
        # Gets rect of img
        self.rect = self.image.get_rect()
        # Piece's grid position
        self.x = gx
        self.y = gy
        # Places piece
        self.rect.centerx = (self.x * TILE_WIDTH) + TILE_OFFSET_X + TILE_WIDTH / 2
        self.rect.centery = (self.y * TILE_HEIGHT) + TILE_OFFSET_Y + TILE_HEIGHT / 2

    def update(self):
        self.rect.centerx = (self.x * TILE_WIDTH) + TILE_OFFSET_X + TILE_WIDTH / 2
        self.rect.centery = (self.y * TILE_HEIGHT) + TILE_OFFSET_Y + TILE_HEIGHT / 2

    def getMoves(self):
        posMoves = []
        # Gets all positions on board and returns them (piece can move anywhere)
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                sameCol = checkSameColor(self, gx, gy)
                if sameCol:
                    continue
                posMoves.append((gx, gy))
        return posMoves

    def legalMove(self, gx, gy):
        # Checks to see if a move puts king in check
        sOldX = self.x
        sOldY = self.y
        self.x = gx
        self.y = gy
        killedSprite = False
        for sprite in self.sameGroup:
            if isinstance(sprite, King):
                for spriteO in self.oppGroup:
                    # Sees if taking a piece would keep king out of check
                    if self.x == spriteO.x and self.y == spriteO.y:
                        killedSprite = True
                        oldX = spriteO.x
                        oldY = spriteO.y
                        oldIndex = spriteO.imgIndex
                        oldColor = spriteO.color
                        oldType = type(spriteO)
                        spriteO.kill()
                        break
                sprite.checkCheck()
                # Respawns piece if it wouldn't have saved the king
                if killedSprite:
                    oldType(self.game, oldColor, oldX, oldY, oldIndex)
                if sprite.inCheck:
                    self.x = sOldX
                    self.y = sOldY
                    return False
                else:
                    break
        self.x = sOldX
        self.y = sOldY
        return True

    def move(self, gx, gy):
        # Makes sure move is valid
        if (gx, gy) in self.getMoves():
            # Sets piece's position
            legal = self.legalMove(gx, gy)
            if legal:
                # Swaps turn of game
                self.x = gx
                self.y = gy
                self.game.swapTurn()
                # Checks to see if any kings are now in check
                for sprite in self.oppGroup:
                    if isinstance(sprite, King):
                        sprite.checkCheck()
                        if sprite.inCheck:
                            # Checks for checkmate
                            if len(sprite.getMoves()) == 0:
                                allMoves = []
                                for piece in sprite.sameGroup:
                                    if piece != sprite:
                                        moves = piece.getMoves()
                                        for move in moves:
                                            if piece.legalMove(move[0], move[1]):
                                                allMoves.append(move)
                                if len(allMoves) == 0:
                                    self.game.gameOver()

    @property
    def sameGroup(self):
        # Gets the color of the group that the piece is in
        if self.color == "white":
            return self.game.whiteGroup
        else:
            return self.game.blackGroup

    @property
    def oppGroup(self):
        # Gets opposing group of piece
        if self.color == "white":
            return self.game.blackGroup
        else:
            return self.game.whiteGroup


class Pawn(Piece):
    def __init__(self, game, col, gx, gy, imgIndex):
        super(Pawn, self).__init__(game, col, gx, gy, imgIndex)
        # Variable that sees if the pawn has made its first move
        self.moved = False

    def move(self, gx, gy):
        # Makes sure move is valid
        if (gx, gy) in self.getMoves():
            # Sets piece's position
            legal = self.legalMove(gx, gy)
            if legal:
                # Swaps turn of game
                self.x = gx
                self.y = gy
                self.game.swapTurn()
                self.moved = True
                # Checks to see if any kings are now in check
                for sprite in self.oppGroup:
                    if isinstance(sprite, King):
                        sprite.checkCheck()
                        if sprite.inCheck:
                            # Checks for checkmate
                            if len(sprite.getMoves()) == 0:
                                allMoves = []
                                for piece in sprite.sameGroup:
                                    if piece != sprite:
                                        moves = piece.getMoves()
                                        for move in moves:
                                            if piece.legalMove(move[0], move[1]):
                                                allMoves.append(move)
                                if len(allMoves) == 0:
                                    self.game.gameOver()

    def update(self):
        self.rect.centerx = (self.x * TILE_WIDTH) + TILE_OFFSET_X + TILE_WIDTH / 2
        self.rect.centery = (self.y * TILE_HEIGHT) + TILE_OFFSET_Y + TILE_HEIGHT / 2
        # Checks to see if pawn made it to final row
        if self.color == "white":
            finalRow = 0
        else:
            finalRow = BOARD_ROWS - 1
        # Opens menu to promote pawn
        if self.y == finalRow:
            self.game.pawnMenu(self)

    def getMoves(self):
        # Gets pawn's possible moves
        posMoves = []
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                inFront1 = False
                inFront2 = False
                # Pawn can only move straight 1 spot (or 2 of it hasn't moved)
                if gx == self.x:
                    # Pawn can move two spots if it hasn't moved
                    if not self.moved:
                        dist = 2
                    else:
                        dist = 1
                    # Makes sure there isn't a piece in front of the pawn
                    for sprite in self.game.allSprites:
                        if sprite not in self.game.selectGroup:
                            if self.color == "white":
                                if sprite.x == self.x and sprite.y == self.y - 1:
                                    inFront1 = True
                                if dist == 2:
                                    if sprite.x == self.x and sprite.y == self.y - 2:
                                        inFront2 = True
                            else:
                                if sprite.x == self.x and sprite.y == self.y + 1:
                                    inFront1 = True
                                if dist == 2:
                                    if sprite.x == self.x and sprite.y == self.y + 2:
                                        inFront2 = True
                    if inFront1:
                        continue
                    # Makes sure pawn doesn't move backwards
                    if self.color == "white":
                        if gy > self.y:
                            continue
                    else:
                        if gy < self.y:
                            continue
                    sameCol = checkSameColor(self, gx, gy)
                    if sameCol:
                        continue
                    # Makes sure pawn doesn't move too far
                    if abs(self.y - gy) <= dist:
                        # Makes sure pawn can't take piece two spots away
                        if abs(self.y - gy) == dist:
                            if inFront2:
                                continue
                        posMoves.append((gx, gy))
                else:
                    # Checks for pieces diagonal to pawn to take
                    for sprite in self.game.allSprites:
                        if sprite not in self.game.selectGroup:
                            if abs(sprite.x - self.x) == 1:
                                if self.color == "white":
                                    if sprite.y < self.y and abs(sprite.y - self.y) == 1:
                                        if (sprite.x, sprite.y) not in posMoves:
                                            sameCol = checkSameColor(self, sprite.x, sprite.y)
                                            if not sameCol:
                                                posMoves.append((sprite.x, sprite.y))
                                else:
                                    if sprite.y > self.y and abs(sprite.y - self.y) == 1:
                                        if (sprite.x, sprite.y) not in posMoves:
                                            sameCol = checkSameColor(self, sprite.x, sprite.y)
                                            if not sameCol:
                                                posMoves.append((sprite.x, sprite.y))
        # Returns possible moves
        return posMoves


class Bishop(Piece):
    def getMoves(self):
        # Gets possible moves for bishop
        posMoves = []
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                # Makes sure piece isn't the same color
                sameCol = checkSameColor(self, gx, gy)
                if sameCol:
                    continue
                # Gets diagonals from piece and sees if coords are in them
                if (gx, gy) not in getDiagonals(self):
                    continue
                posMoves.append((gx, gy))
        # Returns possible moves
        return posMoves


class Knight(Piece):
    def getLs(self):
        # List of possible l shapes
        dirs = [(2, 1), (-2, 1), (2, -1), (-2, -1),
                (1, 2), (-1, 2), (1, -2), (-1, -2)]
        ls = []
        # Adds possible new positions to l list
        for dir in dirs:
            ls.append((self.x + dir[0], self.y + dir[1]))
        # Returns possible moves
        return ls

    def getMoves(self):
        # Gets possible moves for knight
        posMoves = []
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                # Makes sure piece isn't the same color
                sameCol = checkSameColor(self, gx, gy)
                if sameCol:
                    continue
                # Makes sure position is in possible ls
                if (gx, gy) not in self.getLs():
                    continue
                posMoves.append((gx, gy))
        # Returns possible moves
        return posMoves


class Rook(Piece):
    def __init__(self, game, col, gx, gy, imgIndex):
        super(Rook, self).__init__(game, col, gx, gy, imgIndex)
        # Variable that sees if the pawn has made its first move
        self.moved = False

    def move(self, gx, gy):
        # Makes sure move is valid
        if (gx, gy) in self.getMoves():
            # Sets piece's position
            legal = self.legalMove(gx, gy)
            if legal:
                # Swaps turn of game
                self.x = gx
                self.y = gy
                self.game.swapTurn()
                self.moved = True
                # Checks to see if any kings are now in check
                for sprite in self.oppGroup:
                    if isinstance(sprite, King):
                        sprite.checkCheck()
                        if sprite.inCheck:
                            # Checks for checkmate
                            if len(sprite.getMoves()) == 0:
                                allMoves = []
                                for piece in sprite.sameGroup:
                                    if piece != sprite:
                                        moves = piece.getMoves()
                                        for move in moves:
                                            if piece.legalMove(move[0], move[1]):
                                                allMoves.append(move)
                                if len(allMoves) == 0:
                                    self.game.gameOver()

    def getMoves(self):
        # Gets possible moves for rook
        posMoves = []
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                # Makes sure piece isn't the same color
                sameCol = checkSameColor(self, gx, gy)
                if sameCol:
                    continue
                # Makes sure pos is in a straight
                if (gx, gy) not in getStaights(self):
                    continue
                posMoves.append((gx, gy))
        # Returns possible moves
        return posMoves


class Queen(Piece):
    def getMoves(self):
        # Gets possible moves for queen
        posMoves = []
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                # Makes sure piece isn't the same color
                sameCol = checkSameColor(self, gx, gy)
                if sameCol:
                    continue
                # Combines both diagonal moves and straight moves for queen movement
                strtMoves = getStaights(self)
                diagMoves = getDiagonals(self)
                moves = strtMoves + diagMoves
                # Makes sure pos is in possible moves
                if (gx, gy) not in moves:
                    continue
                posMoves.append((gx, gy))
        # Returns possible moves
        return posMoves


class King(Piece):
    def __init__(self, game, col, gx, gy, imgIndex):
        super(King, self).__init__(game, col, gx, gy, imgIndex)
        # Variable that sees if the pawn has made its first move
        self.moved = False
        self.inCheck = False
        self.castleMoves = []

    def move(self, gx, gy):
        # Makes sure move is valid
        if (gx, gy) in self.getMoves():
            # Sets piece's position
            legal = self.legalMove(gx, gy)
            if legal:
                # Swaps turn of game
                self.x = gx
                self.y = gy
                self.game.swapTurn()
                self.moved = True
                # Checks to see if any kings are now in check
                for sprite in self.oppGroup:
                    if isinstance(sprite, King):
                        sprite.checkCheck()
                        if sprite.inCheck:
                            # Checks for checkmate
                            if len(sprite.getMoves()) == 0:
                                allMoves = []
                                for piece in sprite.sameGroup:
                                    if piece != sprite:
                                        moves = piece.getMoves()
                                        for move in moves:
                                            if piece.legalMove(move[0], move[1]):
                                                allMoves.append(move)
                                if len(allMoves) == 0:
                                    self.game.gameOver()

    def checkCheck(self):
        # Sees if king is in check or not
        for moves in self.getAllMoves(self.x, self.y):
            if (self.x, self.y) in moves:
                self.inCheck = True
                return
        self.inCheck = False

    def possibleMoves(self):
        # Used to find possible moves for king without checking for other pieces' moves
        # Gets possible moves for king
        posMoves = []
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                # Makes sure piece isn't the same color
                sameCol = checkSameColor(self, gx, gy)
                if sameCol:
                    continue
                # Makes sure both x and y are within one spot of king
                if abs(gx - self.x) > 1 or abs(gy - self.y) > 1:
                    continue
                posMoves.append((gx, gy))
        return posMoves

    def getAllMoves(self, gx, gy):
        # Makes sure king doesn't put itself into check by getting possible moves of opposing pieces
        allMoves = []
        for sprite in self.oppGroup:
            if not isinstance(sprite, King) and not isinstance(sprite, Pawn):
                allMoves.append(sprite.getMoves())
            elif isinstance(sprite, King):
                allMoves.append(sprite.possibleMoves())
            elif isinstance(sprite, Pawn):
                pMoves = sprite.getMoves()
                if sprite.color == "white":
                    if gy < sprite.y and abs(gy - sprite.y) == 1:
                        if abs(gx - sprite.x) == 1:
                            pMoves.append((gx, gy))
                else:
                    if gy > sprite.y and abs(gy - sprite.y) == 1:
                        if abs(gx - sprite.x) == 1:
                            pMoves.append((gx, gy))
                allMoves.append(pMoves)

        return allMoves

    def getMoves(self):
        # Gets possible moves for king
        posMoves = []
        for gx in range(BOARD_COLS):
            for gy in range(BOARD_ROWS):
                self.castleMoves = []
                blocked = False
                # Makes sure piece isn't the same color
                sameCol = checkSameColor(self, gx, gy)
                if sameCol:
                    continue
                # Makes sure both x and y are within one spot of king
                if abs(gx - self.x) > 1 or abs(gy - self.y) > 1:
                    continue
                # Makes sure king doesn't put itself into check
                allMoves = self.getAllMoves(gx, gy)
                for move in allMoves:
                    if (gx, gy) in move:
                        blocked = True
                        break
                if blocked:
                    continue
                posMoves.append((gx, gy))
        # Castling
        cDirs = []
        # Makes sure king isn't in check and hasn't moved
        if not self.moved and not self.inCheck:
            for sprite in self.sameGroup:
                if isinstance(sprite, Rook):
                    # Makes sure rook hasn't moved
                    if not sprite.moved:
                        # King side rook
                        if sprite.x > self.x:
                            cBlocked = False
                            # Makes sure each tile between king and rook isn't occupied and not in check
                            for cx in range(self.x, 7):
                                for sprite2 in self.game.allSprites:
                                    if sprite2 not in self.game.selectGroup:
                                        if sprite2 != self:
                                            if sprite2.x == cx and sprite2.y == self.y:
                                                cBlocked = True
                                                break
                                for lst in allMoves:
                                    if abs(cx - self.x) <= 2:
                                        if (cx, self.y) in lst:
                                            cBlocked = True
                                            break
                                if cBlocked:
                                    break
                            if not cBlocked:
                                cDirs.append("right")
                        # Queen side rook
                        else:
                            cBlocked = False
                            for cx in range(1, self.x):
                                for sprite2 in self.game.allSprites:
                                    if sprite2 not in self.game.selectGroup:
                                        if sprite2 != self:
                                            if sprite2.x == cx and sprite2.y == self.y:
                                                cBlocked = True
                                                break
                                for lst in allMoves:
                                    if abs(cx - self.x) <= 2:
                                        if (cx, self.y) in lst:
                                            cBlocked = True
                                            break
                                if cBlocked:
                                    break
                            if not cBlocked:
                                cDirs.append("left")
        # Adds possible castles to possible moves and its own list
        if "left" in cDirs:
            self.castleMoves.append((self.x - 2, self.y))
            posMoves.append((self.x - 2, self.y))
        if "right" in cDirs:
            self.castleMoves.append((self.x + 2, self.y))
            posMoves.append((self.x + 2, self.y))

        # Returns possible moves
        return posMoves
