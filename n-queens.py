import pygame

pygame.init()
winsize = 90
winmultiplier = 6
height = winsize * winmultiplier
width = height + winsize * 2
solvedBoard = []
buttonOffset = (winsize * 2) // 3



WHITE = (255,255,255)
BLACK  = (0,0,0)
LIGHTGRAY = (100,100,100)
LIGHTBLUE = (0,111,255)

window = pygame.display.set_mode((width,height))
pygame.display.set_caption('N-queens solver')

myfont = pygame.font.SysFont('arial', 30)
instructionFont = pygame.font.SysFont('arial', 20)

solverButton = pygame.Rect(0,0, 100, 50)
solverButton.center = (width // 2, height // 2 + height // 6)

previousPage = pygame.Rect(0, 0, 75, 50)
nextPage = pygame.Rect(0, 0, 75, 50)

previousPage.center = (height + buttonOffset - 10, 100)
nextPage.center = (height + buttonOffset * 2 + 10 ,100)

clearButton = pygame.Rect(0, 0, 75, 50)
clearButton.center = (height + (width - height) // 2, height // 2)

def left_diagonal_check(arr, row, col):
    x1, y1 = (0, 0)
    if row > col:
        x1, y1 = (row - col, 0)
    elif col > row:
        x1, y1 = (0, col - row)
    while ((x1 != len(arr)) and (y1 != len(arr[0]))):
        if arr[x1][y1] == 1:
            return False
        x1 = x1 + 1
        y1 = y1 + 1
    return True


def right_diagonal_check(arr, row, col):
    x1, y1 = (row, col)
    while x1 != 0 and y1 != len(arr) - 1:
        x1 = x1 - 1
        y1 = y1 + 1
    while x1 != len(arr) and y1 >= 0:
        if arr[x1][y1] == 1:
            return False
        x1 = x1 + 1
        y1 = y1 - 1
    return True


def is_valid_move(arr, row, col):
    for i in range(len(arr[0])):# no other 1 in row
        if arr[row][i]:
            return False
    for i in range(len(arr[col])):  # no other 1 in column
        if arr[i][col]:
            return False

    if not (right_diagonal_check(arr, row, col) and left_diagonal_check(arr, row, col)):
        return False

    return True

def array_copier(arr,N):
    array = initalize_array(N)
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            array[i][j] = arr[i][j]
    return array



def solveNQueens(arr,col):
    global solvedBoard
    result = False
    if col >= len(arr[0]) :
        solvedBoard.append(array_copier(arr,len(arr)))
        return True
    for row in range(len(arr[0])):
        if is_valid_move(arr,row,col):
            arr[row][col] = 1
            result = solveNQueens(arr,col + 1) or result
            arr[row][col] = 0

    return result


def draw_chessboard(N):
    cellsize = height // N
    for x in range(N):
        for y in range(N):
            if x % 2 == 0 and y % 2 != 0:
                pygame.draw.rect(window,LIGHTGRAY, (cellsize * x, cellsize * y, cellsize,cellsize ))
            elif x % 2 != 0 and y % 2 == 0:
                pygame.draw.rect(window, LIGHTGRAY, (cellsize * x, cellsize * y , cellsize, cellsize))
    pygame.draw.line(window, BLACK, (0, 0), (cellsize * N, 0))
    pygame.draw.line(window,BLACK,(cellsize * N,0),(cellsize * N,cellsize * N))

def number_of_solutions(page, arr):
    string = '{} / {}'
    instructions = instructionFont.render(string.format(str(page + 1), str(len(arr))), 1, BLACK)
    instructionsRect = instructions.get_rect()
    instructionsRect.center = (height + (width - height) // 2, 50)
    window.blit(instructions,instructionsRect)

    pygame.draw.rect(window, LIGHTGRAY, previousPage)
    pygame.draw.rect(window, LIGHTGRAY, nextPage)
    pygame.draw.rect(window, LIGHTGRAY, clearButton)

    previous = instructionFont.render('Previous', 1, BLACK)
    previousRect = previous.get_rect()
    previousRect.center = previousPage.center
    window.blit(previous,previousRect)

    next = instructionFont.render('Next', 1, BLACK)
    nextRect = next.get_rect()
    nextRect.center = nextPage.center
    window.blit(next,nextRect)

    clear = instructionFont.render('Clear', 1, BLACK)
    clearRect = clear.get_rect()
    clearRect.center = clearButton.center
    window.blit(clear, clearRect)





def populate_cells(arr, N):
    cellsize = height // N
    queensize = cellsize // 1.5
    queenoffset = (cellsize - queensize) // 2
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            if arr[row][col]:

                pygame.draw.rect(window, LIGHTBLUE, (col * cellsize + queenoffset, row * cellsize + queenoffset, queensize,queensize))

def initalize_array(N):
    return [[0 for i in range(N)] for j in range(N)]

def main_menu():
    #Heading
    text = myfont.render('Input number of Queens wanted (4 minimum):',1,BLACK)
    textRect = text.get_rect()
    textRect.center = (width //2 , height // 2 - height // 6)
    window.blit(text,textRect)

    #draws solve button
    pygame.draw.rect(window, LIGHTGRAY, solverButton)

    solvetext = myfont.render('Solve', 1, BLACK)
    solvetextRect = solvetext.get_rect()
    solvetextRect.center = (width // 2, height // 2 + height // 6)
    window.blit(solvetext, solvetextRect)

def input_number(numberString):
    inputText = myfont.render(numberString,1,BLACK)
    inputTextRect = inputText.get_rect()
    inputTextRect.center = (width //2 , height // 2)
    window.blit(inputText, inputTextRect)



run = True
pressed = False
numberString = ''
N = 0
page = 0
solved = False
while run:
    window.fill(WHITE)
    if not pressed or N <= 3:
        main_menu()
        input_number(numberString)
        pressed = False
    elif N > 3:
        arr = initalize_array(N)
        draw_chessboard(N)
        # check if solved so program doesnt solve everytime user changes page
        if solved:
            solveNQueens(arr, 0)
            solved = False
        populate_cells(solvedBoard[page],N)
        number_of_solutions(page,solvedBoard)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.unicode.isdigit():
                numberString += event.unicode
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                numberString = numberString[:-1]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            x = position[0]
            y = position[1]
            if solverButton.collidepoint(x,y) and not pressed:
                if numberString != '':
                    N = int(numberString)
                    numberString = ''
                    pressed = True
                    solved  = True
            elif previousPage.collidepoint(x,y) and page > 0:
                page = page - 1
            elif nextPage.collidepoint(x,y) and page < len(solvedBoard) - 1:
                page = page + 1
            elif clearButton.collidepoint(x,y):
                pressed = False
                solved = False
                solvedBoard = []
                page = 0
        elif event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()

