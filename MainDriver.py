from Basic import AddressModifiy
from time import sleep
import DDTM
import CDTM

"""
Instruction:
- MainDriver.py — orchestrates two scenarios chosen by user: it generates plaintexts (DDTM),
  produces ciphertexts or random blocks (CDTM), runs the DDTM decision procedure,
  and compares/verifies the resultthat is the 4-round impossible-differential-based distinguisher game defined on picoCrypton.
  Moreover, it can also recover the key of the 7-round picoCrypton block cipher in chosen plaintext scenario.

Purpose and high-level flow:
A. In the scenario of the destinguisher game:
   1. Ask the user for a target folder path (Address).
   2. Prompt the user for the desired success probability pr (float, 0.5 <= pr < 1).
   3. Call DDTM.DDTM_Write(pr, Address) to generate and save plaintext pairs (writes Plaintexts.txt).
   4. Call CDTM.CDTM_Write(Address) to produce the corresponding ciphertext pairs (writes Ciphertexts.txt) and receive a bool
      indicating which generator was used.
   5. Call DDTM.DDTM_Decision(pr, Address) to read ciphertexts and produce a boolean decision (bHat).
   6. Call CDTM.CDTM_Verify(b, bHat) to print whether the decision is correct.

B. In the scenario of picoCrypton key-recovery:
   1. Ask the user for a target folder path (Address).
   2. Call ADTM.ADTM_Write(Address) to generate and save plaintext pairs for impossible differential cryptanalysis.
   3. Receive the corresponding ciphertext pairs from the ODTM and then start seiving the keys by using impossible-differential property.
   4. At the last step by applyng the exhaustive search on remaining-ke sets the master key of the algorithm will be recovered.

Types and input expectations:
- Address: plain Python string containing the target folder path. Current implementation concatenates
  a Windows backslash ("\\") internally when forming filenames. For cross-platform usage or to avoid
  double separators, pass an absolute folder path or modify modules to use os.path.join before calling.
- pr: Python float in the half-open interval [0.5, 1). The code enforces the bounds and will reprompt
  until a valid float is entered.

User interaction and validation:
- main(Address: str) validates Address is a str and uses input(...) to request pr.
- The pr prompt expects a valid float; the loop re-prompts on invalid values.
- The script prints progress messages for long-running operations (DDTM/CDTM), so expect lengthy runtime
  and high memory usage for large pr values (DDTM may create very large plaintext sets).

Side effects and files created/consumed:
- Plaintexts.txt (written by DDTM.WriteDoc) — file format: each line "0x" + 16 hex chars (row-major).
- Ciphertexts.txt (written by CDTM.WriteDoc) — same format as above.
- Both files are created under the provided Address folder (Address + "\\Plaintexts.txt" / "\\Ciphertexts.txt").

Error handling and robustness:
- main() catches TypeError for an invalid Address argument and prints an error message.
- The called modules (DDTM, CDTM, Encryption, Basic, RF_Operators, KS_Operators) perform their own
  type/dtype checks and typically print error messages on invalid input (often returning None).
  For robust automation, validate and pre-convert inputs (numpy dtypes) before calling or refactor
  helper functions to raise exceptions instead of printing.
- Because file I/O and generation can be expensive, consider:
    - Ensuring the target folder exists and is writable before starting.
    - Running the heavy generation steps in a background thread/process or with progress persistence.
    - Using streaming writes/reads to avoid building huge in-memory lists.

Recommendations and improvements:
- Use os.path.join(Address, "Plaintexts.txt") and os.path.join(Address, "Ciphertexts.txt") inside
  DDTM/CDTM to be cross-platform and avoid path concatenation bugs.
- Convert and validate inputs to numpy types where required by helper modules (e.g. np.uint8).
- Consider returning status codes from main (int) instead of only printing, to support automation.
- Add an optional non-interactive API (pass pr as parameter or via CLI arguments) for scripted runs.
- Add logging instead of prints for better control of verbosity and progress tracking.

Example usage (interactive):
    $ python MainDriver.py
    Please enter the address of the target folder: C:\data\picoCrypton
    For detiguisher game please enter the required success probability, a number between 0.5 and 1, with exclude 1: 0.9
    (program prints progress messages, writes files, and prints verification results)
    For key recovery scenario the only the address of chosen plaintexts and correspondig ciphertexts shall entered.

Behavior summary:
- main(Address) returns None; primary outputs are created files and console messages.
- The final verification result is printed by CDTM.CDTM_Verify; the boolean values used are produced by
  CDTM.CDTM_Write and DDTM.DDTM_Decision and are not returned by main.
- For picoCrypton key recovery the ADTM.ADTM_Write insert the chosen plaintexts and also sieves the possible keys, and ODTM encrypts the required plaintexts.
"""

###################################################################################################
####                                Destinguisher Game Scenario                                ####
###################################################################################################
def main(Address: str, scenario: int) -> None:
    try:
        if type(Address) != str:
            raise TypeError("The first input must be the address of the target folder.")
        else:
            if scenario == "0":
                pr = float(input("Enter the required success probability, a number between 0.5 and 1, with exclude 1: "))
                while type(pr) != float or pr < 0.5 or pr >= 1:
                    print("Invalid input. Please enter a number between 0.5 and 1, with exclude 1.")
                    pr = float(input("Enter the required success probability, a number between 0.5 and 1, with exclude 1: "))
                print("Destinguisher game has been started.")
                print("Generating the required plaintexts prepared by DDTM.")
                DDTM.DDTM_Generate(pr, Address)
                print("Preparing the random blocks by CDTM.")
                b = CDTM.CDTM_Generate(Address)
                print("Checking the generated data by DDTM.")
                print("Making deceision by DDTM.")
                bHat = DDTM.DDTM_Decision(pr, Address)
                print("Verifying the answer by CDTM.")
                CDTM.CDTM_Verify(b, bHat)
            else:
                print("Please wait. This part shall be completed.")

    except TypeError as e:
        print("Error: Game has been terminated because of an invalid input.", e)

if __name__ == "__main__":
    print("In this session we will execute two impossible-differential cryptanalaysis scenarios on picoCrypton block cipher.")
    scenario = input("Please eneter the scenario.\n [0]:Destinguisher game,\n [1]:Key recovery.\n")
    while scenario != "1" and scenario != "0":
        print("Input is not correct.")
        scenario = input("Please eneter the scenario.\n [0]:Destinguisher game,\n [1]:Key recovery.\n")
    Address = input("Please enter the address of the target folder: ")
    modAddress = AddressModifiy(Address)
    main(modAddress, scenario)
