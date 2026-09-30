import numpy as np
import Basic as Bsc
import Encryption as Enc

"""
Instruction:
- ODTM.py - prepares ciphertext collections from plaintexts produced by ADTM, writes/reads them to disk,
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
                        print(f"ODTM: {round(y)}% of the writing has been completed.")
                        flag = False
                    elif abs(y - round(y)) >= 0.05:
                        flag = True
                    else:
                        continue
            f.close()

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                         Reading the plaintexts preapared by ADTM                          ####
###################################################################################################
def ReadDoc(Address: str) -> None:
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
                    print(f"ODTM: {round(y)}% of the reading has been completed.")
                    flag = False
                elif abs(y - round(y)) >= 0.05:
                    flag = True
                else:
                    continue
            return ptxList

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                            Preparing and wrinting output data                             ####
###################################################################################################
def ODTM_Generate(Address: str) -> list:
    ptxList = ReadDoc(Address)
    N = len(ptxList)
    ctxList = []
    MK = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ], dtype = np.uint8)
    Address1 = Address + "\\MasterKey.txt"
    with open(Address1, "r") as f:
        Data = f.read()
        f.close()
    Len = len(Data)
    if Len != 6 or (Len == 7 and Len[6] != "\n"):
        raise ValueError("Master key has not been eneterd properly in the MasterKe.txt file. Please renter it properly.")
    else:
        for i in range(2, 6):
            y = Data[i]
            if ord(y) > 57:
                t = np.uint8(ord(y) - 87)
            else:
                t = np.uint8(ord(y) - 48)
            B = Bsc.Int2Nib(t)
            MK[i - 2][0] = B[0]
            MK[i - 2][1] = B[1]
            MK[i - 2][2] = B[2]
            MK[i - 2][3] = B[3]
        flag = True
        for i in range(0, N):
            X = Enc.Enc(ptxList[i], MK, 7)
            ctxList.append(X.copy())
            y = round(100 * i / N, 2)
            if abs(y - round(y, 1)) < 0.005 and flag == True:
                print(f"ODTM: {round(y, 1)}% of the generating data has been completed.")
                flag = False
            elif abs(y - round(y, 1)) >= 0.005:
                flag = True
            else:
                continue
        WriteDoc(ctxList, Address)
        return ctxList