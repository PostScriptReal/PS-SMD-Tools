# PostScript's SMD Tools
PostScript's SMD Tools (PS's SMD Tools) is an open-source, MIT licensed modding tool for Half-Life and other games that run under the GoldSRC engine **(not Source or Source 2)**.

PS's SMD Tools allows for the editing of GoldSRC SMD files in advanced ways that would be tedious to do by hand, such as copying bone transformations, allowing for 5-fingered rigs to be made easily out of multiplayer playermodels (e.g. HL Deathmatch, Counter-Strike and Sven Co-op).

## Features
- Armature Bone Transformation Duping
- Material Pointer Fixing (Fixing pointers to texture files)
- Scripting for extra automation

## Getting Started
### Running from binaries
If you are a Windows/Linux user, you can download binaries for your respective OS and run them without needing to install python. The binaries support the following versions of Windows and Linux

- Windows 8 and above (x86 only)
- Linux distros using kernel version 5.15 and above (also x86 only)

If your device doesn't meet the above requirements, you must run the program from the source code.

### Running from source code
Alternatively, if you are running MacOS or ARM versions of the major operating systems (I personally do not recommend running on Windows versions earlier than 7 as that would require using outdated versions of python that have security vulnerabilities), you can still run the program manually from the source code! **Keep in mind that MacOS support may be a little iffy as I have no way to test the program on MacOS, you may experience issues with the program which may include display issues and program errors.**

The first thing you should do is download the source code, it is recommended that you go to the latest stable release and click on 'Source code (.zip or .tar.gz)', you can also clone the repository using git but that would give you a much more unstable version of the program.

After grabbing the source code, you should make sure that you have *Python* installed, if you are using Linux, I recommend trying to find *Python* in your distro's package manager, if you are using Windows or Mac, download your OS's respective version of *Python* on the [*Python* website](https://www.python.org/downloads/), and go through the setup (restart if/when necessary).

Once you have *Python* installed and the source code for SMD Tools is unzipped, open up a terminal in the directory SMD Tools is unzipped from and run this command:
```
python3 GUI.py
```
**If that doesn't work, try substituting python3 for python, otherwise there are either issues with the program itself or you have missing dependencies!**

Once everything is done, the program should launch on your system, if you are using Windows or Linux, you can execute smd_tools.bat (for Windows) or smd_tools.sh (for Linux) instead of typing in the command each time.

## Need help on how to use the program?
Check out the wiki page for tutorials so you can learn how to properly use the tool!
