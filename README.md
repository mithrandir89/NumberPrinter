# NumberPrinter
A simple application accepting an unsigned 32-bit number from the user and displaying that number in big-endian and little-endian byte formats.

## Directories structure
* **src**: contains the C source implementing the program features
* **tests**: contains Python test script(s) to exercise and validate program behaviour in different conditions
* **support**: contains a Python script to be deployed (ideally to a build server) and launched autonomously. This will will clone the environment of this repository in the host system and launch the automated the test suite.

## Dependencies
In order to build the program, `make` and `gcc` (supporting -std=c99) are needed.

All the Python scripts are using modern features of Python, mostly leveraging builtin libraries. Recommended a version => **Python 3.7**.

The tests launcher Python script (included in **support** folder) is making use of external *GitPython* submodule to interact with local and remote repository.

## System Operation
### Tests
The Python script running the program embeds an array of test cases to exercise the application.
The application executable must be provided as the only argument to the script.
It will run all of tests defined, producing stats printed to stdout.
In case of failure, it will also produce a report with Returned vs Expected outputs.
![alt text](https://github.com/mithrandir89/NumberPrinter/raw/master/doc/images/execute_ok.PNG "Execution with no failures")
![alt text](https://github.com/mithrandir89/NumberPrinter/raw/master/doc/images/execute_nok.PNG "Execution with failure")

### Launcher script
The script assumes Git installed on the host system.
It will clone the repository (URL hardcoded) in the working directory, build the system and launch the tests found in the tests folder of the repo (which in our case is 1).
For each of the test found, a *.txt* report file is opened and written with the content of each run (reporting current time). The report file will be still created in the working directory.
![alt text](https://github.com/mithrandir89/NumberPrinter/raw/master/doc/images/launcher_output.PNG "Launcher script output")
![alt text](https://github.com/mithrandir89/NumberPrinter/raw/master/doc/images/launcher_log.PNG "Launcher script log")

## Compatibility
Tested on:
* **Windows 10 64bit**. Using GNU Make 3.82.90 under MINGW and Python 3.7.2.

It should work with minimal efforts/adjustments also on UNIX platforms.