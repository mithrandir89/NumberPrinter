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

## Compatibility
Tested on:
* **Windows 10 64bit**
