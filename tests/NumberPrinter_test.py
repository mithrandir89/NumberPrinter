import sys
import os
import subprocess
import ctypes

# Define a tuple (immutable object) containing all our test cases with: Input | Expected Return code | Expected stdout
INPUT_INDEX      = 0
EXP_RET_INDEX    = 1
EXP_STDOUT_INDEX = 2
TestCases = ( #Input         Expected Ret    Expected stdout
             ("32000000",    0,              "Big Endian: 01 E8 48 00\nLittle Endian: 00 48 E8 01\n"),  # Random number within range (1)
             ("2000000000",  0,              "Big Endian: 77 35 94 00\nLittle Endian: 00 94 35 77\n"),  # Random number within range (2)
             ("4000000000",  0,              "Big Endian: EE 6B 28 00\nLittle Endian: 00 28 6B EE\n"),  # Random number within range (3)     
             ("4294967295",  0,              "Big Endian: FF FF FF FF\nLittle Endian: FF FF FF FF\n"),  # Max boundary
             ("0",           0,              "Big Endian: 00 00 00 00\nLittle Endian: 00 00 00 00\n"),  # Min boundary
             ("2147483648",  0,              "Big Endian: 80 00 00 00\nLittle Endian: 00 00 00 80\n"),  # Exactly half range   
             ("StringTest", -1,              ""                                                     ),  # ASCII characters
             ("-1",         -1,              ""                                                     ),  # Out of range (negative)
             ("4294967296", -1,              ""                                                     ),  # Out of range (bigger than max)
             ("åçêë",       -1,              ""                                                     ),  # Random characters from extended ASCII table
             ("4294967294",  0,              "Big Endian: FF FF FF FE\nLittle Endian: FE FF FF FF\n"),  # First valid below max boundary
             ("1",           0,              "Big Endian: 00 00 00 01\nLittle Endian: 01 00 00 00\n"),  # First valid above min boundary
             ("+1",         -1,              ""                                                     ),  # Positive number with '+' sign in front
             ("/*-+",       -1,              ""                                                     ),  # Random math symbols
             ("1.0",        -1,              ""                                                     ),  # Floating point with dot
             ("1,0",        -1,              ""                                                     )   # Floating point with comma
            )

TESTRES_RETCODE_INDEX = 0
TESTRES_STDOUT_INDEX  = 1            
TESTRES_SUCCESS_INDEX = 2

def RunTest(ProgramPath):
    
    print(os.path.basename(__file__) + " is going to run a total of " + str(len(TestCases)) + " TestCases...", end="", flush=True)

    # Collect all the results in here for statistics and log purpose.
    TestsResult = []
    
    # Run the program, providing all the inputs needed to cover the test cases required
    for i in range(len(TestCases)):
        Success = False
        
        CompletedProcess = subprocess.run([ProgramPath, TestCases[i][INPUT_INDEX]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='ascii')
        
        # Capture output into string
        StrStdOut = CompletedProcess.stdout
        
        # Interpret return code as signed (Windows by default is providing an unsigned number)
        ReturnCode = ctypes.c_int32(CompletedProcess.returncode).value
                
        # First test if the program returned with expected code
        if ReturnCode == TestCases[i][EXP_RET_INDEX]:
            # Then compare expected printed output
            if StrStdOut == TestCases[i][EXP_STDOUT_INDEX]:
                Success = True
                
        # Append a new tuple to the list
        TestsResult.append((ReturnCode, StrStdOut, Success))
                        
    print("done")
    
    # Use TestsResult to gather statistics and failure details
        
    # Filter success
    NSuccess = len([Success for Result in TestsResult if True == Result[TESTRES_SUCCESS_INDEX]])
  
    print("Stats:\nTests Passed: " + str(NSuccess) +
          "\nTests Failed: " + str(len(TestCases) - NSuccess) +
          "\nPassed Tests Percentage " + str('%.3f'%(100 * float(NSuccess)/float(len(TestCases)))) + "%")
          
    for i in range(len(TestsResult)):
        if False == TestsResult[i][TESTRES_SUCCESS_INDEX]:
            print("\nTestCase #" + str(i) + " failed:" + 
                  "\nRet Code - Expected: " + str(TestCases[i][EXP_RET_INDEX]) +                    ", Received: " +  str(TestsResult[i][TESTRES_RETCODE_INDEX]) +
                  "\nStdout - Expected: "   + str(str.encode(TestCases[i][EXP_STDOUT_INDEX])) +     ", Received: " +  str(str.encode(TestsResult[i][TESTRES_STDOUT_INDEX])))


if __name__ == "__main__":
    # Accept only one single parameter, which must be the program path (NB argv[0] is the name of the script)
    if len(sys.argv) == 2:
        ProgramPath = sys.argv[1];
        RunTest(ProgramPath)
    else:
        sys.stderr.write("Error: Expected single argument containig path of the program under test")
