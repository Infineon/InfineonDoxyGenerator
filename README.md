
# Infineon Doxygen Generator 

Python Command Line Tool for Infineon Arduino Library Doxygen Documentation 

Features:
* HTML and PDF Doxygen generation (with Graphviz)
* Doxygen toolchain installation support (only Linux)
* Github pages realease
* Travis CI automation
* Cross platform (Windows, Linux)

# Developing doxygen documentation

1. Download the repository or release in the project/library root folder.
2. Your library must follow the Arduino Library Specfication (link)
3. Install the required toolchain --> Cross platform installation steps
4. Generate html 
5. Release it manually
6. Automate deployment in Travis CI

# Other options 
- Custom doxyfile vs. automatically generated configuration
    -  Add additional .dox files 
    -  Custom project logo

# Add automation to your repository

- travis script
- only for new tags

# Supported OS
    Executed in the following platforms:
    - windows
    - cygwin 
    - unix...

# Troubleshooting 
 - git credentials popups
 - error handling