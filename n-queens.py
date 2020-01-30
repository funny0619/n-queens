def left_diagonal_check(arr,row,col):
    newList = []
    x1, y1 = (0, 0)
    if row > col:
        x1, y1 = (row - col, 0)
    elif col > row:
        x1, y1 = (0, col - row)
    while ((x1 != len(arr)) and (y1 != len(arr[0]))):
        newList.append(arr[x1][y1])
        x1 = x1 + 1
        y1 = y1 + 1
    if sum(newList) > 0:
        return False
    else:
        return True

def right_diagonal_check(arr,row,col):
    newList = []
    x1,y1 = (row,col)
    while x1 != 0 and y1 != len(arr)-1:
        x1 = x1 - 1
        y1 = y1 + 1
    while x1 != len(arr) and y1 >= 0:
        newList.append(arr[x1][y1])
        x1 = x1 + 1
        y1 = y1 - 1
    if sum(newList) > 0:
        return False
    else:
        return True

def isvalidmove(arr,row,col):
    for i in range(row,len(arr)): #no other 1 in row
        if arr[i].count(1) > 0:
            return False
        else:
            count = 0
            for i in range(len(arr[col])): #no other 1 in column
                if arr[i][col] == 1:
                    count = count + 1
            if count > 0:
                return False
            else: #no other 1 in diagonal
                if right_diagonal_check(arr,row,col) and left_diagonal_check(arr,row,col):
                    return True
                else:
                    return False

def solveNQueens(arr,col):
    if col >= len(arr[0]) :
        print(arr)
        return True
    for row in range(len(arr[0])):
        if isvalidmove(arr,row,col):
            arr[row][col] = 1
            if solveNQueens(arr, col + 1):
                return True
            arr[row][col] = 0

    return False


chessArray = [[0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]]
solveNQueens(chessArray,0)
