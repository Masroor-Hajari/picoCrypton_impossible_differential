import numpy as np

"""
Instruction:
- KS_Operators.py executes key-schedule operation process of picoCrypton block cipher.
- All inputs and outputs use numpy types:
    - Blocks: numpy with shape (4, 4) and dtype=np.uint8.
    - Single nibble values: numpy scalar or 0-dim numpy array with dtype=np.uint8.
    - Round/index parameters: plain Python int.
"""

###################################################################################################
####                                     Updating process                                      ####
###################################################################################################
def Updt(MK: np.uint8, r: int) -> list:
    try:
        m, n = MK.shape
        if type(r) != int or r < 1 or r > 12:
            raise TypeError("The second input must be an integer value between 1 and 12.")
        elif m != 4 or n != 4 or MK.max() > 1 or MK.min() < 0:
            raise ValueError("The first input must be a binary 4x4 matrix.")
        else:
            KS = []
            KS.append(MK.copy())
            for n in range(1, r + 1):
                Temp = np.array([
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                    ], dtype = np.uint8)
                for i in range(0, 3):
                    for j in range(0, 4):
                        Temp[i][j] = KS[n - 1][(i + 1)][j]
                for i in range(0, 3):
                    Temp[3][i] = KS[n - 1][0][i + 1]
                Temp[3][3] = KS[n - 1][0][0]
                KS.append(Temp.copy())
            return KS

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                                    Extracting process                                     ####
###################################################################################################
def Ext(KS: np.uint8, r: int) -> np.uint8:
    try:
        m, n = KS.shape
        if type(r) != int or r < 0 or r > 12:
            raise TypeError("The second input must be an integer between 0 and 12.")
        elif m != 4 or n != 4 or KS.max() > 1 or KS.min() < 0:
            raise ValueError("The first input must be a binary 4x4 matrix.")
        else:
            RC = np.array([
                [0, 0, 0, 1],
                [0, 0, 1, 0],
                [0, 1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 1, 1],
                [0, 1, 1, 0],
                [1, 1, 0, 0],
                [1, 0, 1, 1],
                [0, 1, 0, 1],
                [1, 0, 1, 0],
                [0, 1, 1, 1],
                [1, 1, 1, 0],
                [1, 1, 1, 1]
                ], dtype = np.uint8)
            RK = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range (0, 4):
                    RK[i][j] = KS[(i + 1) % 4][j]
                if i == 3:
                    RK[i][i] = np.uint8(RK[i][i] ^ np.uint8(KS[3][i] ^ 1))
                else:
                    RK[i][i] = np.uint8(RK[i][i] ^ np.uint8(KS[0][i] ^ 1))
                RK[i][i] = np.uint8(RK[i][i] ^ RC[r][i])
            return RK.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)



