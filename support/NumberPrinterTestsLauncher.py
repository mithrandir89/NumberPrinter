from git import Repo # needed for Git interaction
from git.exc import GitCommandError
import os
import subprocess
import datetime

# Global variables
GIT_REPO_URL   = "https://github.com/mithrandir89/NumberPrinter.git"
GIT_REPO_LOCAL = "NumberPrinter" # this also serves as the name of the program under test
SRC_DIR        = "src"
TESTS_DIR      = "tests"

BUILDSYSTEM_APP = "mingw32-make"
PYTHON          = "py"

# Reference to Repo object
RepositoryRef = 0

def CloneRepo():
    global RepositoryRef
    try:
        print("Attempting to clone program repository in current working directory...", end="", flush=True)
        # Use util library to facilitate cloning operation.
        # Cloning will automatically checkout to master branch,
        # which is considered the mainline branch for the program to test
        RepositoryRef = Repo.clone_from(GIT_REPO_URL, GIT_REPO_LOCAL)
        
        print("...done")
        
    except GitCommandError:
        print("\nA folder with the same name of the repository is already present. Considering this step already done.");        
        RepositoryRef = Repo(GIT_REPO_LOCAL) # get reference to repo. If this aborts, it means that this is not a git repo...
        
    # all the other types of exception are not considered here and will make the system abort, as expected
   
def BuildProgram():
    # To build the program, I need to change current working directory
    os.chdir(os.path.join(os.getcwd(), GIT_REPO_LOCAL))
    
    # Checkout into master branch (discard local changes), in any case. Then pull to get last version
    RepositoryRef.git.checkout('master', force=True)
    RepositoryRef.git.pull()
    
    # Execute make. This will create an executable in the root of the Git repository
    # NB Not capturing the output as we would like to see it on the terminal
    subprocess.run([BUILDSYSTEM_APP, GIT_REPO_LOCAL])
      
def LaunchTests():
    # Look for all .py file in the test folder
    TestsList = []
    for file in os.listdir(os.path.join(os.getcwd(), TESTS_DIR)):
        if file.endswith(".py"):
            TestsList.append(file)
            
    print("Found #" + str(len(TestsList)) + " Test scripts. Launching them...")
    
    # Launch them using program executable created
    for i in range(len(TestsList)):
        CompletedProcess = subprocess.run([PYTHON, TESTS_DIR + "/" + TestsList[i], GIT_REPO_LOCAL], stdout=subprocess.PIPE, encoding='ascii')
        # Print std output
        print(CompletedProcess.stdout)
        # Extract test name without extension, to feed log file
        TestName, Extension = os.path.splitext(TestsList[i])
        AppendLogToFile(TestName, CompletedProcess.stdout)
        
def AppendLogToFile (filename, content):

    # Store logs in the working directory where this script has been launched
    os.chdir("..")

    # Open file and write header (append in case already exist)
    # Create new log every day
    f = open(filename + "_" + str(datetime.date.today().day).zfill(2) + str(datetime.date.today().month).zfill(2) + str(datetime.date.today().year) + ".txt", "a+")
    f.write("Test executed at " + str(datetime.datetime.now().hour).zfill(2) + ":" + str(datetime.datetime.now().minute).zfill(2) + "\n")
    
    # Test output content
    f.write(content)
    
    # End test delimiter
    f.write("--------------------------------------------------------------------------------\n")
    
    f.close()
  
if __name__ == "__main__":
    # Clone github repository, if not existing in current directory
    CloneRepo()

    # Invoke make file to build the program.
    BuildProgram()
    
    # LaunchTests found in the remote repo
    LaunchTests()
    
