import numpy as np
import RF_Operators as RF_Opr
import KS_Operators as KS_Opr

"""
Instruction:
- Encryption.py implements the picoCrypton block cipher encryption routine, Enc(P, MK, r).

- Inputs:
  - P: numpy.ndarray, binary, shape (4, 4), dtype=np.uint8 - plaintext matrix.
  - MK: numpy.ndarray, binary, shape (4, 4), dtype=np.uint8 - master key matrix.
  - r: int - number of rounds (1..12).

- Output:
  - Returns numpy.ndarray, binary, shape (4, 4), dtype=np.uint8 - ciphertext matrix.

- Conventions and expectations:
  - All nibble values must be numpy uint8 (use np.uint8(...) or np.array(..., dtype=np.uint8)).
  - Many helper functions (in Basic.py, RF_Operators.py, KS_Operators.py) check .dtype and .shape;
    passing plain Python ints or nested lists will raise TypeError from those checks.
  - Convert inputs before calling Enc to avoid silent dtype/shape issues:
      P = np.array(P, dtype=np.uint8).reshape(4,4)
      MK = np.array(MK, dtype=np.uint8).reshape(4,4)

- Error handling:
  - Enc validates inputs and prints error messages on invalid input; it may return None after printing.
  - For robust code, validate and convert inputs in callers or modify helpers to raise exceptions instead of printing.

- Example:
    P = np.array([[1,0,0,1],
                  [0,1,0,1],
                  [1,1,0,1],
                  [1,0,0,0]], dtype=np.uint8)
    MK = np.array([[0,0,0,0],
                   [1,0,0,0],
                   [0,1,1,1],
                   [1,0,1,0]], dtype=np.uint8)
    C = Enc(P, MK, 12)  # returns np.ndarray (4,4) dtype=np.uint8

- Notes:
  - If you need reproducible keys or deterministic behavior, construct KS externally and pass prepared numpy arrays.
  - Convert returned numpy scalars to native Python ints with int(...) when needed.
"""

###################################################################################################
####                             picoCrypton encryption algorithm                              ####
###################################################################################################
def Enc(P: np.uint8, MK: np.uint8, r: int) -> np.uint8:
    try:
        m, n = MK.shape
        p, q = P.shape
        if type(r) != int or r < 1 or r > 12:
            raise TypeError("The third input must be an integer between 1 and 12.")
        elif m != 4 or n != 4 or p != 4 or q != 4 or P.max() < 0 or P.min() > 1 or MK.max() < 0 or MK.min() > 1:
            raise ValueError("The first and second inputs must be a 4x4 matrices of nibbles.")
        else:
            RK = KS_Opr.Ext(MK, 0)
            X = RF_Opr.Sigma(P, RK)
            KS = KS_Opr.Updt(MK, r)
            for i in range(1, r):
                K = np.uint8(KS[i].copy())
                RK = KS_Opr.Ext(K, i)
                Temp = X.copy()
                X = RF_Opr.RF(Temp, RK)
            K = np.uint8(KS[r].copy())
            RK = KS_Opr.Ext(K, r)
            C = RF_Opr.LastRF(X, RK)
            return C.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

