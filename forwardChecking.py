import numpy as np
from copy import deepcopy
import sys
import collections 
import datetime

def getIndex(ch, currentState):
  return([(ix,iy) for ix, row in enumerate(currentState) for iy, i in enumerate(row) if i == ch])

def findTheCell(r,c):
  row = -1
  col = -1

  # Checking for row
  if(r>=0 and r<=2):
    row = 0
  elif(r>=3 and r<=5):
    row = 1
  elif(r>=6 and r<=8):
    row = 2
  
  # Checking for Column
  if(c>=0 and c<=2):
    col = 0
  elif(c>=3 and c<=5):
    col = 1
  elif(c>=6 and c<=8):
    col = 2
  

  return (row, col)


def checkSafety(num, row, col, arr):
  presentInRow = False
  presentInCol = False
  presentInCell = False


  # Checking for Row
  if(int(num) in arr[row]):
    presentInRow = True
  else:
    presentInRow = False
  
  # Checking for Column
  for i in range(0, len(arr)):
    if(int(arr[i][col]) == int(num)):
      presentInCol = True
      break
  
  
  # Checking for Cell
  cell = findTheCell(row,col)
  if(cell[0] == 0):
    rowLower = 0
    rowUpper = 2
  elif(cell[0] == 1):
    rowLower = 3
    rowUpper = 5
  elif(cell[0] == 2):
    rowLower = 6
    rowUpper = 8
  

  if(cell[1] == 0):
    colLower = 0
    colUpper = 2
  elif(cell[1] == 1):
    colLower = 3
    colUpper = 5
  elif(cell[1] == 2):
    colLower = 6
    colUpper = 8

  for i in range(rowLower, rowUpper + 1):
    for j in range(colLower, colUpper + 1):
      if(arr[i][j] == num):
        presentInCell = True
        break
  if(presentInRow == False and presentInCol == False and presentInCell == False):
    return True
  else:
    # print("row",presentInRow)
    # print("col", presentInCol)
    # print("Cell", presentInCell)
    return False
        

def printTheSudukoState(arr):
  print("")
  # print("The Suduko is:")
  for eachRow in arr:
    for eachColumn in eachRow:
      print(eachColumn, end =" ")
    print("")
  print("")

def getDomain(row,col,arr):
  rowElements = [e for i, e in enumerate(arr[row]) if e != 0]

  columnElements = []
  for i in range(0, len(arr)):
    if (arr[i][col] != 0):
      columnElements.append(arr[i][col])

  # Checking for Cell
  cell = findTheCell(row,col)
  if(cell[0] == 0):
    rowLower = 0
    rowUpper = 2
  elif(cell[0] == 1):
    rowLower = 3
    rowUpper = 5
  elif(cell[0] == 2):
    rowLower = 6
    rowUpper = 8
  

  if(cell[1] == 0):
    colLower = 0
    colUpper = 2
  elif(cell[1] == 1):
    colLower = 3
    colUpper = 5
  elif(cell[1] == 2):
    colLower = 6
    colUpper = 8

  cellElements = []
  for i in range(rowLower, rowUpper + 1):
    for j in range(colLower, colUpper + 1):
      if(arr[i][j] != 0):
        cellElements.append(arr[i][j])
  tempArr = rowElements + columnElements + cellElements
  finalDomain = list(set([1,2,3,4,5,6,7,8,9]) - set(tempArr))
  return finalDomain

def assignNumber(row,col,arr):
  global listOfZeroesFilled
  global initialArray
  global numbersPossible
  tempTuple = (row,col)
  tryArr = deepcopy(arr)
  domain = numbersPossible[str(tempTuple)]
  for eachNumber in domain:
    safe = checkSafety(eachNumber, int(row), int(col), arr)
    if( safe == True):
      arr[row][col] = eachNumber
      if(str(arr) not in allStatesCreated):
        initialArray[row][col] = eachNumber
        tempArr = []
        tempArr.append(row)
        tempArr.append(col)
        listOfZeroesFilled.append(tempArr)
        allStatesCreated.append(str(arr))
        for i in range(0, len(initialArray[row])):
          if(initialArray[row][i] == 0 and (eachNumber in numbersPossible[str((row, i))])):
            # print("Before removing")
            # print(numbersPossible[str((row, i))])
            numbersPossible[str((row, i))].remove(eachNumber)
            # print("After removing")
            # print(numbersPossible[str((row, i))])
        # print("\n\n column")
        for i in range(0,len(initialArray)):
          if(initialArray[i][col] == 0 and (eachNumber in numbersPossible[str((i, col))])):
            # print("Before removing")
            # print(numbersPossible[str((i, col))])
            numbersPossible[str((i, col))].remove(eachNumber)
            # print("Before removing")
            # print(numbersPossible[str((i, col))])
        # print("\n\n cell")
        cell = findTheCell(row,col)
        if(cell[0] == 0):
          rowLower = 0
          rowUpper = 2
        elif(cell[0] == 1):
          rowLower = 3
          rowUpper = 5
        elif(cell[0] == 2):
          rowLower = 6
          rowUpper = 8
        

        if(cell[1] == 0):
          colLower = 0
          colUpper = 2
        elif(cell[1] == 1):
          colLower = 3
          colUpper = 5
        elif(cell[1] == 2):
          colLower = 6
          colUpper = 8

        cellElements = []
        for i in range(rowLower, rowUpper + 1):
          for j in range(colLower, colUpper + 1):
            if(initialArray[i][j] == 0 and (eachNumber in numbersPossible[str((i, j))]) ):
              # print("Before removing")
              # print(numbersPossible[str((i, j))])
              numbersPossible[str((i, j))].remove(eachNumber)
              # print("After removing")
              # print(numbersPossible[str((i, j))])

        break
    # else:
    #   continue
  else:
    if(len(listOfZeroesFilled) != 0):
      latestZero = listOfZeroesFilled[-1]
      r1 = latestZero[0]
      c1 = latestZero[1]
      previousNumber = tryArr[latestZero[0]][latestZero[1]]
      tryArr[latestZero[0]][latestZero[1]] = 0
      initialArray = deepcopy(tryArr)
      listOfZeroesFilled.pop()
      for i in range(0, len(initialArray[r1])):
        if(initialArray[r1][i] == 0 and (previousNumber not in numbersPossible[str((r1, i))]) and (i != c1 )):
          # print("Before removing")
          # print(numbersPossible[str((row, i))])
          numbersPossible[str((r1, i))].append(previousNumber)
          # print("After removing")
          # print(numbersPossible[str((row, i))])
      # print("\n\n column")
      for i in range(0,len(initialArray)):
        if(initialArray[i][c1] == 0 and (previousNumber not in numbersPossible[str((i, c1))]) and (i != r1)):
          # print("Before removing")
          # print(numbersPossible[str((i, col))])
          numbersPossible[str((i, c1))].append(previousNumber)
          # print("Before removing")
          # print(numbersPossible[str((i, col))])
      # print("\n\n cell")
      cell = findTheCell(r1,c1)
      if(cell[0] == 0):
        rowLower = 0
        rowUpper = 2
      elif(cell[0] == 1):
        rowLower = 3
        rowUpper = 5
      elif(cell[0] == 2):
        rowLower = 6
        rowUpper = 8
      

      if(cell[1] == 0):
        colLower = 0
        colUpper = 2
      elif(cell[1] == 1):
        colLower = 3
        colUpper = 5
      elif(cell[1] == 2):
        colLower = 6
        colUpper = 8

      cellElements = []
      for i in range(rowLower, rowUpper + 1):
        for j in range(colLower, colUpper + 1):
          if(initialArray[i][j] == 0 and (previousNumber not in numbersPossible[str((i, j))]) ):
            # print("Before removing")
            # print(numbersPossible[str((i, j))])
            numbersPossible[str((i, j))].append(previousNumber)
            # print("After removing")
            # print(numbersPossible[str((i, j))])
    else:
      global parentArray
      initialArray = parentArray
      global systemVariable
      systemVariable = False

startTime = datetime.datetime.now()
initialArray = []
allStatesCreated = []
listOfZeroesFilled = []
parentArray = []
checker = -1
with open('suduko.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    for line in lines:
      arr = []
      for eachCharacter in line:
        arr.append(int(eachCharacter))
      initialArray.append(arr)
      parentArray.append(arr)

print("The Initial suduko State is:")
printTheSudukoState(initialArray)

numbersPossible = {}
zeroes = getIndex(0,initialArray)
for eachZero in zeroes:
  numbersPossible[str(eachZero)] = [1,2,3,4,5,6,7,8,9]

systemVariable = True

# allZeroes = getIndex(0,initialArray)
# if(len(allZeroes) != 0):
#   firstZero = allZeroes[0]
#   assignNumber(firstZero[0],firstZero[1],initialArray)
# else:
#   systemVariable = False
while systemVariable:
  allZeroes = getIndex(0,initialArray)
  if(len(allZeroes) != 0):
    firstZero = allZeroes[0]
    assignNumber(firstZero[0],firstZero[1],initialArray)
  else:
    systemVariable = False  
print("The Solution is:")
printTheSudukoState(initialArray)
endTime = datetime.datetime.now()
print("The Time taken is:",endTime - startTime)