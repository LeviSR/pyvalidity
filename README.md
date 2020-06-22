# pyvalidity 
This program checks validity of an l-group inequation e <= t by
  - Transforming an t into a meet of joins of products of literals
  - Checking whether the joinands of all of the meetands extend to a right order on the free group, which yields a counterexample to validity of e <= t

# Usage
  1. Fork the repository to your own GitHub account.
  2. Open a terminal.
  3. Clone your repository into the active folder by executing `git clone <link to your fork>` in the terminal (without the <>).
  4. Execute `cd pyvalidity` in the terminal.
  5. Execute `python -m pyvalidity` in the terminal. Make sure you have Python installed and have added to
  your PATH variable.
  6. Follow the prompts.
  
# Troubleshooting on Windows
If typing `python` into the terminal opens the Microsoft Store, search for **App execution aliases** in the Start menu and disable the App installers for Python. If your PATH variable contains `...\Python\Python38` you should be able to use the program now.
