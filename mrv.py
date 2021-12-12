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
  tryArr = deepcopy(arr)
  domain = getDomain(row,col,arr)
  for eachNumber in domain:
    # safe = checkSafety(eachNumber, int(row), int(col), arr)
    # if( safe == True):
    arr[row][col] = eachNumber
    if(str(arr) not in allStatesCreated):
      initialArray[row][col] = eachNumber
      tempArr = []
      tempArr.append(row)
      tempArr.append(col)
      listOfZeroesFilled.append(tempArr)
      allStatesCreated.append(str(arr))
      break
    # else:
    #   continue
  else:
    if(len(listOfZeroesFilled) != 0):
      latestZero = listOfZeroesFilled[-1]
      tryArr[latestZero[0]][latestZero[1]] = 0
      initialArray = deepcopy(tryArr)
      listOfZeroesFilled.pop()
    else:
      global parentArray
      initialArray = parentArray
      global systemVariable
      systemVariable = False
      # global checker 
      # checker = 1

    




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

def getMRV(zeroArray):
  weights = []
  for eachZero in zeroArray:
    weights.append(len(getDomain(eachZero[0],eachZero[1], initialArray)))
  return weights.index(min(weights))



# initialArray = [[4, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0], [0, 0, 8, 1, 0, 2, 9, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0], [0, 0, 2, 6, 0, 9, 5, 0, 0], [8, 0, 0, 2, 0, 3, 0, 0, 9], [0, 0, 5, 0, 1, 0, 3, 0, 0]]
# print("The Initial suduko State is:")
# printTheSudukoState(initialArray)
# allZeroes = getIndex(0,initialArray)
# if(len(allZeroes) != 0):
#   firstZero = allZeroes[0]
#   assignNumber(firstZero[0],firstZero[1],initialArray)
# else:
#   systemVariable = False

systemVariable = True

# zeroArray = getIndex(0, initialArray)
# print(len(zeroArray))
# weights = []
# for eachZero in zeroArray:
#   weights.append(len(getDomain(eachZero[0],eachZero[1], initialArray)))
# print(len(weights))
# print(weights.index(min(weights)))

while systemVariable:
  allZeroes = getIndex(0,initialArray)
  if(len(allZeroes) != 0):
    MRV_index = getMRV(allZeroes)
    firstZero = allZeroes[MRV_index] #this is responsible for getting the MRV
    assignNumber(firstZero[0],firstZero[1],initialArray)
  else:
    systemVariable = False  
print("The Solution is:")
printTheSudukoState(initialArray)
endTime = datetime.datetime.now()
print("The Time taken is:",endTime - startTime)