import numpy as np
from Basic import Int2Nib

"""
Instruction:
- This module implements round-function operators for 16-bit blocks for picoCrypton blockcipher.
- Use numpy types: pass blocks as numpy.ndarray with shape (4,4) and dtype=np.uint8.
- Functions check .dtype and .shape; plain Python ints/lists will cause TypeError. Convert inputs before calling: np.uint8(value) or np.array(value, dtype=np.uint8).
- Functions print error messages on invalid input and may return None; callers should validate inputs and/or catch exceptions and not rely on printed output for control flow.
- Returned values are numpy arrays or numpy scalars (dtype=np.uint8). Convert to Python int with int(...) when a native int is required.
"""

###################################################################################################
####                                    picoCrypton SBOXes                                     ####
###################################################################################################
def SBOX(x: np.uint8, num: int) -> np.uint8:
    try:
        if x.dtype != np.uint8 or type(num) != int:
            raise TypeError("Inputs must be an integer number.")
        elif x < 0 or x > 15 or num < 0 or num > 3:
            raise ValueError("First Input must be between 0 and 15 and second one must be between 0 and 3.")
        else:
            sbox = np.array([[4, 15, 3, 8, 13, 10, 12, 0, 11, 5, 7, 14, 2, 6, 1, 9],
                             [1, 12, 7, 10, 6, 13, 5, 3, 15, 11, 2, 0, 8, 4, 9, 14],
                             [7, 14, 12, 2, 0, 9, 13, 10, 3, 15, 5, 8, 6, 4, 11, 1],
                             [11, 0, 10, 7, 13, 6, 4, 2, 12, 14, 3, 9, 1, 5, 15, 8]], dtype=np.uint8)
            y = sbox[num][x]
            return y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input type.", e1)
    except ValueError as e2:
        print("Error: Invalid input value.", e2)
###################################################################################################
####                                      Gamma operator                                       ####
###################################################################################################
def Gamma(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 1 or X.min() < 0:
            raise ValueError("Each element of the block must be a binary value.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 2):
                for j in range(0, 2):
                    inNum = X[2 * i][2 * j] * 8 + X[2 * i][2 * j + 1] * 4 + X[2 * i + 1][2 * j] * 2 + X[2 * i + 1][2 * j + 1]
                    num = 2 * i + j
                    outNum = SBOX(inNum, num)
                    B = Int2Nib(outNum)
                    Y[2 * i][2 * j] = B[0]
                    Y[2 * i][2 * j + 1] = B[1]
                    Y[2 * i + 1][2 * j] = B[2]
                    Y[2 * i + 1][2 * j + 1] = B[3]
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                  Inverse Gamma operator                                   ####
###################################################################################################
def InvGamma(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 1 or X.min() < 0:
            raise ValueError("Each element of the block must be a binary value.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 2):
                for j in range(0, 2):
                    inNum = X[2 * i][2 * j] * 8 + X[2 * i][2 * j + 1] * 4 + X[2 * i + 1][2 * j] * 2 + X[2 * i + 1][2 * j + 1]
                    num = 2 * (1 - i) + j
                    outNum = SBOX(inNum, num)
                    B = Int2Nib(outNum)
                    Y[2 * i][2 * j] = B[0]
                    Y[2 * i][2 * j + 1] = B[1]
                    Y[2 * i + 1][2 * j] = B[2]
                    Y[2 * i + 1][2 * j + 1] = B[3]
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                        Pi operator                                        ####
###################################################################################################
def Pi(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 1 or X.min() < 0:
            raise ValueError("Each element of the block must be a binary value.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    for l in range(0, 4):
                        t = np.uint8((i + j + l) % 4)
                        if t == 0:
                            continue
                        else:
                            Y[i][j] = np.uint8(X[l][j] ^ Y[i][j])
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                       Tau operator                                        ####
###################################################################################################
def Tau(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 1 or X.min() < 0:
            raise ValueError("Each element of the block must be a binary value.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    Y[i][j] = X[j][i]
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                       Pi* operator                                        ####
###################################################################################################
def PiStar(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 1 or X.min() < 0:
            raise ValueError("Each element of the block must be a binary value.")
        else:
            Y = Tau(X)
            Y = Pi(Y)
            Y = Tau(Y)
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)


###################################################################################################
####                                      Sigma operator                                       ####
###################################################################################################
def Sigma(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of binary values.")
        elif X.max() > 1 or X.min() < 0 or K.max() > 1 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    Y[i][j] = np.uint8(X[i][j] ^ K[i][j])
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                      Sigma* operator                                       ####
###################################################################################################
def SigmaSt(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of binary values.")
        elif X.max() > 1 or X.min() < 0 or K.max() > 1 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            kt = Tau(K)
            kSt = Pi(kt)
            Y = Sigma(X, kSt)
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                      Round function                                       ####
###################################################################################################
def RF(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of binary values.")
        elif X.max() > 1 or X.min() < 0 or K.max() > 1 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            Z = Gamma(X)
            W = Pi(Z)
            V = Tau(W)
            Y = Sigma(V, K)
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                   Last-Round function                                    #####
###################################################################################################
def LastRF(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of nibbles.")
        elif X.max() > 1 or X.min() < 0 or K.max() > 1 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            Z = Gamma(X)
            W = SigmaSt(Z, K)
            C = Tau(W)
            return C.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)





