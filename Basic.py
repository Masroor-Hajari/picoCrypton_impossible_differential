import numpy as np

"""
Instruction:
- This module provides utilities for the 16-bit block cipher "picoCrypton" and its operations.

- Pass values using the types annotated on each function (e.g., np.uint8 to represent bit values,
  Python int for RandInt bounds). Convert/validate inputs before calling.

- Callers should catch exceptions raised by these functions; do not rely on printed error messages
  for control flow.
"""

###################################################################################################
####                   Convert an integer to the corresponding 4-bit nibble                    ####
###################################################################################################
def Int2Nib(n: np.uint8) -> np.uint8:
    try:
        if n.dtype != np.uint8:
            raise TypeError(f"Input must be an integer value.")
        elif n < 0 or n > 15:
            raise ValueError(f"Input must be an integer value between 0 and 15.")
        else:
            B = np.array([], dtype = np.uint8)
            t = n
            B = np.append(B, (t // 8))
            t = t - B[0] * 8
            B = np.append(B, (t // 4))
            t = t - B[1] * 4
            B = np.append(B, (t // 2))
            t = t - B[2] * 2
            B = np.append(B, t)
            return B.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                  The integer represtentation of a hexadecimal character                   ####
###################################################################################################
def Hex2Int(x: str) -> np.uint8:
    try:
        if type(x) != str:
            raise TypeError(f"Input must be a hexadecimal string.")
        elif len(x) != 1 or x not in "0123456789abcdefABCDEF":
            raise ValueError(f"Input must be a hexadecimal string of length 1.")
        else:
            y = int(x, 16)
            y = np.array([y], dtype = np.uint8)
            return y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)
    
###################################################################################################
####                        The hexadecimal represtation of an integer                         ####
###################################################################################################
def Int2Hex(x: np.uint8) -> str:
    try:
        if x.dtype != np.uint8:
            raise TypeError(f"Input must be an integer number.")
        elif x < 0 or x > 15:
            raise ValueError(f"Input must be an integer between 0 and 15.")
        else:
            if x < 10:
                y = chr(x + 48)
            else:
                y = chr(x + 87)
            return y

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                                  Random integer genrator                                  ####
###################################################################################################
def RandInt(a: int, b: int, inclusive: bool) -> np.uint8:
    try:
        if type(a) != int or type(b) != int or type(inclusive) != bool:
            raise TypeError("Bounds must be integers. The thitd parameter must be a boolean value.")
        if a > b:
            raise ValueError("The lower bound must be less than or equal to the upper bound.")
        else:
            rng = np.random.default_rng()
        if inclusive:
            y = rng.integers(a, b + 1)
            return y.astype(np.uint8)
        else:
            try:
                if a == b and inclusive == False:
                    raise ValueError("The lower and upper bounds must be different when the range is exclusive.")
                else:
                    y = rng.integers(a, b)
                    return y.astype(np.uint8)

            except ValueError as e3:
                print("Error: Invalid input.", e3)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                               Random integer list genrator                                ####
###################################################################################################
def RndList(upBound: int, N: int) -> list:
    try:
        if type(upBound) != int or type(N) != int:
            raise TypeError("Two inputs must be a non-negative integer numbers.")
        elif upBound < N:
            raise ValueError("number of required random numbers must be less than upper bound.")
        else:
            mid = (upBound - 1) // 2
            if N <= mid:
                bl = True
            else:
                bl = False
                N = upBound - N
                totalList = []
                for i in range(0, upBound):
                    totalList.append(i)
            ctr = 0
            randomList = []
            while ctr < N:
                rng = np.random.default_rng()
                rand = rng.integers(0, upBound)
                if ctr == 0:
                    randomList.append(int(rand))
                    ctr += 1
                else:
                    bl2 = False
                    for i in range(0, ctr):
                        if rand == randomList[i]:
                            bl2 = True
                            break
                    if bl2 == False:
                        randomList.append(int(rand))
                        ctr += 1
            if bl == False:
                totalSet = set(totalList)
                randomSet = set(randomList)
                randomDiffSet = totalSet - randomSet
                randomList = list(randomDiffSet)
            return randomList

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input vlaue.", e2)

###################################################################################################
####                                Generating a Random Vector                                 ####
###################################################################################################
def RndVector(N: int) -> np.uint8:
    try:
        if type(N) != int:
            raise TypeError("Input must be an integer number.")
        elif N >= 4096 or N < 0:
            raise ValueError("In put must be a positive number between 0 and 4095.")
        else:
            num3 = N % 16
            temp = (N - num3) // 16
            num2 = temp % 16
            temp = (temp - num2) // 16
            num1 = temp % 4
            num0 = (temp - num1) // 4
            randomVector = np.array([num0, num1, num2, num3])
            return randomVector.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input vlaue.", e2)
###################################################################################################
####                                   Address modification                                    ####
###################################################################################################
def AddressModifiy(Address: str) -> str:
    try:
        if type(Address) != str:
            raise TypeError("Invalid address.")
        else:
            Address.replace("\\", "\\\\")
            modifyAddress = Address
            return modifyAddress

    except TypeError as e:
        print("Error: Invalid input.", e)




