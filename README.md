# Folder Synchronization Script  

A Python script that keeps a **replica folder** as an exact copy of a **source folder**.  
It runs continuously at a set interval and logs all changes.

## Features
- **One-way sync**: Source to Replica  
- **Copies new or updated files**  
- **Deletes extra files/folders in the replica**  
- **Logs all actions**  

##  How to use
Run the script using:

```sh
python3 synctwofolders.py /path/to/source /path/to/replica 60 /path/to/logfile.log
