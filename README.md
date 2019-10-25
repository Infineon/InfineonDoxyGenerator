
# Infineon Doxygen Generator (DRAFT)

Python Command Line Tool for Infineon Arduino Library Doxygen Documentation 

Features:
* HTML Doxygen generation (with Graphviz)
* PDF Doxygen generation (with Graphviz) (planned)
* Cross platform (Windows, Linux) 
* Doxygen toolchain installation support (only Linux) (planned)
* Github pages realease (beta)
* Travis CI automation (planned)

# Developing doxygen documentation (How to...)

1. Download the repository or release in the project/library root folder.
2. Your library must follow the Arduino Library Specfication (link!)
3. Install the required doxygen toolchain --> Cross platform installation steps (check with CLI, install with CLI (Linux))
4. Generate html 
5. Release it manually
6. Automate deployment in Travis CI

# Other options (Customizations)
- Custom doxyfile vs. automatically generated configuration
    -  Add additional .dox files 
    -  Custom project logo

# Add automation to your repository (Travis CI integration)

- travis script
- only for new tags

# Supported OS (Not yet check)
    Executed in the following platforms:
    - windows
    - cygwin 
    - unix...

# Troubleshooting 
 - git credentials popups ?
 - error handling ? 

 # TODOS
 - handle issues with paths
 - Refactor source files in modules: arduino libs doxyfile, generic doxyfile, release features
 - Add PDF 
 - Improve html template for Arduino library 