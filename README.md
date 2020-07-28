# pyvalidity 
This program checks validity of an l-group inequation e <= t by
  - Transforming an t into a meet of joins of products of literals
  - Checking whether the joinands of all of the meetands extend to a right order on the free group, which yields a counterexample to validity of e <= t

# Usage
  1. Open a terminal.
  2. Clone this repository into the active folder by executing `git clone <link to this repository>` in the terminal (without the <>).
  3. Execute `python pyvalidity` in the terminal.
  4. Follow the prompts.
  
# Troubleshooting on Windows
If typing `python` into the terminal opens the Microsoft Store, search for **App execution aliases** in the Start menu and disable the App installers for Python. If your PATH variable contains `...\Python\Python38` you should be able to use the program now.
