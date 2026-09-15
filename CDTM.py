import numpy as np
import Basic as Bsc
import Encryption as Enc

"""
Instruction:
- CDTM.py - prepares ciphertext collections from plaintexts produced by DDTM, writes/reads them to disk,
  and provides a simple verification helper.
"""

###################################################################################################
####                       Writing the prepared blocks into a text file                        ####
###################################################################################################
def WriteDoc(ctxList: list, Address: str) -> None:
    try:
        if type(ctxList) != list:
            raise TypeError("The first input must be a list of plaintexts.")
        else:
            flag = True
            Address = Address + "\\Ciphertexts.txt"
            Len = len(ctxList)
            with open(Address, "w") as f:
                for i in range(0, Len):
                    f.write("0x")
                    for j in range(0, 4):
                        num = 8 * ctxList[i][j][0] + 4 * ctxList[i][j][1] + 2 * ctxList[i][j][2] + ctxList[i][j][3]
                        f.write(Bsc.Int2Hex(num))
                    f.write("\n")
                    y = round((i + 1) / Len * 100, 2)
                    if abs(y - round(y)) < 0.05 and flag == True:
                        print(f"CDTM: {round(y)}% of the writing has been completed.")
                        flag = False
                    elif abs(y - round(y)) >= 0.05:
                        flag = True
                    else:
                        continue
            f.close()

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                         Reading the plaintexts preapared by DDTM                          ####
###################################################################################################
def ReadDoc(Address: str) -> list:
    try:
        if type(Address) != str:
            raise TypeError("Input must be the address of the target file.")
        else:
            ptxList = []
            Address = Address + "\\Plaintexts.txt"
            with open(Address, "r") as f:
                Data = f.read()
                f.close()
            Len = len(Data)
            ctr = 0
            ctr2 = 0
            flag = True
            while(ctr < Len):
                if Data[ctr] == "0" and Data[ctr + 1] == "x":
                    ctr += 2
                elif Data[ctr - 2] == "0" and Data[ctr - 1] == "x":
                    ctr3 = 0
                    X = np.array([
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                        ], dtype = np.uint8)
                    for i in range(0, 4):
                        num = Bsc.Hex2Int(Data[ctr + ctr3])
                        B = Bsc.Int2Nib(num)
                        X[i, :] = B.copy()
                        ctr3 += 1
                    ctr += 4
                    ptxList.append(X.copy())
                elif Data[ctr] == "\n":
                    ctr += 1
                    ctr2 += 1
                else:
                    ctr += 1
                y = round(100 * ctr / Len, 2)
                if abs(y - round(y)) < 0.05 and flag == True:
                    print(f"CDTM: {round(y)}% of the reading has been completed.")
                    flag = False
                elif abs(y - round(y)) >= 0.05:
                    flag = True
                else:
                    continue
            return ptxList

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                                  Random Oracle Generator                                  ####
###################################################################################################
def RndOracle(N: int) -> list:
    try:
        if type(N) != int or N < 1:
            raise TypeError("Input must be a positive integer.")
        elif N % 120 != 0:
            raise ValueError("Input must be a multiple of 120.")
        else:
            M =N // 120
            dataList =[]
            flag = True
            for i in range(0, M):
                tempList = []
                for j in range(0, 16):
                    X = np.array([
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                        ], dtype = np.uint8)
                    for l in range(0, 4):
                        num = np.uint8(Bsc.RandInt(0, 15, True))
                        X[l, :] = Bsc.Int2Nib(num).copy()
                    tempList.append(X.copy())
                for j in range(0, 15):
                    for l in range(j + 1, 16):
                        dataList.append(tempList[j].copy())
                        dataList.append(tempList[l].copy())
                y = round(100 * i / M, 2)
                if abs(y - round(y, 1)) < 0.005 and flag == True:
                    print(f"CDTM: {round(y, 1)}% of the generating data has been completed.")
                    flag = False
                elif abs(y - round(y, 1)) >= 0.005:
                    flag = True
                else:
                    continue
            return dataList

    except TypeError as e1:
            print("Error: Invalid input.", e1)

    except ValueError as e2:
            print("Error: Invalid input.", e2)

###################################################################################################
####                            Preparing and wrinting output data                             ####
###################################################################################################
def CDTM_Generate(Address: str) -> bool:
    ptxList = ReadDoc(Address)
    N = len(ptxList)
    ctxList = []
    MK = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ], dtype = np.uint8)
    b = Bsc.RandInt(0, 1, True)
    b = 1
    flag = True
    if b == 0:
        for i in range (0, 4):
            for j in range(0, 4):
                MK[i][j] = np.uint8(Bsc.RandInt(0, 65535, True) % 2)
        for i in range(0, N):
            X = Enc.Enc(ptxList[i], MK, 4)
            ctxList.append(X.copy())
            y = round(100 * i / N, 2)
            if abs(y - round(y, 1)) < 0.005 and flag == True:
                print(f"CDTM: {round(y, 1)}% of the generating data has been completed.")
                flag = False
            elif abs(y - round(y, 1)) >= 0.005:
                flag = True
            else:
                continue
        WriteDoc(ctxList, Address)
    else:
        rndList = RndOracle(N)
        WriteDoc(rndList, Address)
    
    b = bool(b)
    return b

###################################################################################################
####                                 Verifying DDTM's response                                 ####
###################################################################################################
def CDTM_Verify(b, bHat) -> None:
    try:
        if type(b) != bool or type(bHat) != bool:
            raise TypeError("Inputs must be boolean values.")
        else:
            if b == bHat:
                print("The decision is correct.")
            else:
                print("The decision is wrong.")

    except TypeError as e:
        print("Error: Invalid input.", e)
