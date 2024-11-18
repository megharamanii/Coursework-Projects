from game import *
#copy of nested list of the gameboard

board_copy = []
for i in board:
    wert = []
    for j in i:
        wert.append(j)
    board_copy.append(wert)
    if SPRITE in i:
        y = i.index(SPRITE)
        x = board.index(i)

user_input = 'w'
while user_input != QUIT:
    if user_input not in CONTROLS:
        print('enter a valid move:')
        user_input = input()
        continue
    for i in board_copy:
        print(' '.join(i))
    print()
    user_input = input()
    if user_input == RESTART:
        board_copy = []
        for i in board:
            wert = []
            for j in i:
                wert.append(j)
            board_copy.append(wert)
            if SPRITE in i:
                y = i.index(SPRITE)
                x = board.index(i)
# WHEN INPUT IS MOVING TO THE RIGHT
    elif user_input == 'd':
        # sprite moving alone
        if board_copy[x][y+1] != WALL:
            if board_copy[x][y+1] == EMPTY:
                if board_copy[x][y] == SPRITE_T:
                    board_copy[x][y] = TARGET
                    board_copy[x][y+1] = SPRITE
                    y += 1
                else:
                    board_copy[x][y] = EMPTY
                    board_copy[x][y+1] = SPRITE
                    y += 1
            # sprite moving on the target
            elif board_copy[x][y+1] == TARGET:
                board_copy[x][y+1] = SPRITE_T
                board_copy[x][y] = EMPTY
                y += 1
            # spirte interacts with boxNS
            elif board_copy[x][y+1] == BOX_NS:
                # General movement if nothing is present
                if board_copy[x][y+2] == WALL or board_copy[x][y+2] == BOX_S or board_copy[x][y+2] == BOX_NS:
                    pass
                elif board_copy[x][y+2] == EMPTY:
                    board_copy[x][y+2] = BOX_NS
                    board_copy[x][y+1] = SPRITE
                    board_copy[x][y] = EMPTY
                    y += 1
                # what if sprite is on target and there is target behind the box
                elif board_copy[x][y+2] == TARGET and board_copy[x][y] == SPRITE_T:
                    board_copy[x][y+2] = BOX_S
                    board_copy[x][y+1] = SPRITE
                    board_copy[x][y] == TARGET
                    y += 1
                # what if right next to the BOX_NS had a target
                elif board_copy[x][y+2] == TARGET:
                    board_copy[x][y+2] = BOX_S
                    board_copy[x][y+1] = SPRITE
                    board_copy[x][y] = EMPTY
                    y += 1
                # what if sprite is on target
                elif board_copy[x][y] == SPRITE_T:
                    board_copy[x][y+2] = BOX_NS
                    board_copy[x][y+1] = SPRITE
                    board_copy[x][y] = TARGET
                    y += 1
            # sprite interacts with box_S
            elif board_copy[x][y+1] == BOX_S:
                # General movement if nothing is present
                if board_copy[x][y+2] == WALL or board_copy[x][y+2] == SPRITE or board_copy[x][y+2] == BOX_NS:
                    pass
                elif board_copy[x][y+2] == EMPTY:
                    board_copy[x][y+2] = BOX_NS
                    board_copy[x][y+1] = SPRITE_T
                    board_copy[x][y] = EMPTY
                    y += 1

# WHEN INPUT IS MOVING TO THE LEFT
    elif user_input == 'a':
        # sprite moving alone
        if board_copy[x][y-1] != WALL:
            if board_copy[x][y-1] == EMPTY:
                if board_copy[x][y] == SPRITE_T:
                    board_copy[x][y] = TARGET
                    board_copy[x][y-1] = SPRITE
                    y -= 1
                else:
                    board_copy[x][y] = EMPTY
                    board_copy[x][y-1] = SPRITE
                    y -= 1
            # sprite moving on the target
            elif board_copy[x][y-1] == TARGET:
                board_copy[x][y-1] = SPRITE_T
                board_copy[x][y] = EMPTY
                y -= 1
            # spirte interacts with boxNS
            elif board_copy[x][y-1] == BOX_NS:
                # General movement if nothing is present
                if board_copy[x][y-2] == WALL or board_copy[x][y+2] == BOX_S or board_copy[x][y-2] == BOX_NS:
                    pass
                elif board_copy[x][y-2] == EMPTY:
                    board_copy[x][y-2] = BOX_S
                    board_copy[x][y-1] = SPRITE
                    board_copy[x][y] = EMPTY
                    y -= 1
                # what if sprite is on target and there is target behind the box
                elif board_copy[x][y-2] == TARGET and board_copy[x][y] == SPRITE_T:
                    board_copy[x][y-2] = BOX_S
                    board_copy[x][y-1] = SPRITE
                    board_copy[x][y] = TARGET
                    y -= 1
                # what if right next to the BOX_NS had a target
                elif board_copy[x][y-2] == TARGET:
                    board_copy[x][y-2] = BOX_S
                    board_copy[x][y-1] = SPRITE
                    board_copy[x][y] = EMPTY
                    y -= 1
                # what if sprite is on target
                elif board_copy[x][y] == SPRITE_T:
                    board_copy[x][y-2] = BOX_NS
                    board_copy[x][y-1] = SPRITE
                    board_copy[x][y] = TARGET
                    y -= 1
            # sprite interacts with box_S
            elif board_copy[x][y-1] == BOX_S:
                # General movement if nothing is present
                if board_copy[x][y-2] == WALL or board_copy[x][y-2] == SPRITE or board_copy[x][y-2] == BOX_NS:
                    pass
                elif board_copy[x][y-2] == EMPTY:
                    board_copy[x][y-2] = BOX_NS
                    board_copy[x][y-1] = SPRITE_T
                    board_copy[x][y] = EMPTY
                    y -= 1
# WHEN INPUT IS MOVING DOWN
    elif user_input == 's':
        # sprite moving alone
        if board_copy[x+1][y] != WALL:
            if board_copy[x+1][y] == EMPTY:
                if board_copy[x][y] == SPRITE_T:
                    board_copy[x][y] = TARGET
                    board_copy[x+1][y] = SPRITE
                    x += 1
                else:
                    board_copy[x][y] = EMPTY
                    board_copy[x+1][y] = SPRITE
                    x += 1
            # sprite moving on the target
            elif board_copy[x+1][y] == TARGET:
                board_copy[x+1][y] = SPRITE_T
                board_copy[x][y] = EMPTY
                x += 1
            # spirte interacts with boxNS
            elif board_copy[x+1][y] == BOX_NS:
                # General movement if nothing is present
                if board_copy[x+2][y] == WALL or board_copy[x+2][y] == BOX_S or board_copy[x+2][y] == BOX_NS:
                    pass
                elif board_copy[x+2][y] == EMPTY:
                    board_copy[x+2][y] = BOX_S
                    board_copy[x+1][y] = SPRITE
                    board_copy[x][y] = EMPTY
                    x += 1
                # what if sprite is on target and there is target behind the box
                elif board_copy[x+2][y] == TARGET and board_copy[x][y] == SPRITE_T:
                    board_copy[x+2][y] = BOX_S
                    board_copy[x+2][y] = SPRITE
                    board_copy[x][y] = TARGET
                    x += 1
                # what if right next to the BOX_NS had a target
                elif board_copy[x+2][y] == TARGET:
                    board_copy[x+2][y] = BOX_S
                    board_copy[x+2][y] = SPRITE
                    board_copy[x][y] = EMPTY
                    x += 1
                # what if sprite is on target
                elif board_copy[x][y] == SPRITE_T:
                    board_copy[x+2][y] = BOX_NS
                    board_copy[x+1][y] = SPRITE
                    board_copy[x][y] = TARGET
                    x += 1
            # sprite interacts with box_S
            elif board_copy[x+1][y] == BOX_S:
                # General movement if nothing is present
                if board_copy[x+2][y] == WALL or board_copy[x+2][y] == SPRITE or board_copy[x+2][y] == BOX_NS:
                    pass
                elif board_copy[x+2][y] == EMPTY:
                    board_copy[x+2][y] = BOX_NS
                    board_copy[x+2][y] = SPRITE_T
                    board_copy[x][y] = EMPTY
                    x += 1
# WHEN INPUT IS MOVING UP
    elif user_input == 'w':
        # sprite moving alone
        if board_copy[x-1][y] != WALL:
            if board_copy[x-1][y] == EMPTY:
                if board_copy[x][y] == SPRITE_T:
                    board_copy[x][y] = TARGET
                    board_copy[x-1][y] = SPRITE
                    x -= 1
                else:
                    board_copy[x][y] = EMPTY
                    board_copy[x-1][y] = SPRITE
                    x -= 1
            # sprite moving on the target
            elif board_copy[x-1][y] == TARGET:
                board_copy[x-1][y] = SPRITE_T
                board_copy[x][y] = EMPTY
                x -= 1
            # spirte interacts with boxNS
            elif board_copy[x-1][y] == BOX_NS:
                # General movement if nothing is present
                if board_copy[x-2][y] == WALL or board_copy[x-2][y] == BOX_S or board_copy[x-2][y] == BOX_NS:
                    pass
                elif board_copy[x-2][y] == EMPTY:
                    board_copy[x-2][y] = BOX_S
                    board_copy[x-1][y] = SPRITE
                    board_copy[x][y] = EMPTY
                    x -= 1
                # what if sprite is on target and there is target behind the box
                elif board_copy[x-2][y] == TARGET and board_copy[x][y] == SPRITE_T:
                    board_copy[x-2][y] = BOX_S
                    board_copy[x-2][y] = SPRITE
                    board_copy[x][y] = TARGET
                    x -= 1
                # what if right next to the BOX_NS had a target
                elif board_copy[x-2][y] == TARGET:
                    board_copy[x-2][y] = BOX_S
                    board_copy[x-2][y] = SPRITE
                    board_copy[x][y] = EMPTY
                    x -= 1
                # what if sprite is on target
                elif board_copy[x][y] == SPRITE_T:
                    board_copy[x-2][y] = BOX_NS
                    board_copy[x-1][y] = SPRITE
                    board_copy[x][y] = TARGET
                    x -= 1
            # sprite interacts with box_S
            elif board_copy[x-1][y] == BOX_S:
                # General movement if nothing is present
                if board_copy[x-2][y] == WALL or board_copy[x-2][y] == SPRITE or board_copy[x-2][y] == BOX_NS:
                    pass
                elif board_copy[x-2][y] == EMPTY:
                    board_copy[x-2][y] = BOX_NS
                    board_copy[x-2][y] = SPRITE_T
                    board_copy[x][y] = EMPTY
                    x -= 1

print('Goodbye')



