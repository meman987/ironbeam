# Pre-requisites

`python`, `hledger` and `just` are used. Only `python` is needed to create csv-files.
The `justfile` is developed for linux/macOS. It should work with cygwin or similar under
Windows.


# Usage

Save daily account statements from https://trading.certigo.com/ (Acount > Overview > Statements) 
in the `input` folder with the extension `.txt`. Select all text, copy and paste into a text-file.

<img width="798" alt="screen" src="https://github.com/user-attachments/assets/1b9293fd-ee84-4164-ad64-8fb57646de69">

Run `just iron` to show results or run the commands in `justfile` manually if you cannot use 
`just`.

