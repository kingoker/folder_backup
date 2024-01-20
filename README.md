📁 This project focuses on developing a folder synchronization program in Python to ensure an identical copy of the source folder is maintained in the replica folder.


#
### Getting Started:

To prepare your working derictory clone this derictory

```
git clone https://github.com/kingoker/folder_backup.git .
```
Launch the program

```
python3 synchronization.py
```

#
### Features:
📍 One-Way Synchronization: The program ensures one-way synchronization, modifying the content of the replica folder to precisely match the content of the source folder.

📍 Periodic Synchronization: Automation is achieved through periodic synchronization, allowing for timely updates.

📍 Logging: Comprehensive logging records file creation, copying, and removal operations to both a file and the console output, enhancing transparency and traceability.

📍 Command Line Configuration: Configure folder paths, synchronization interval, and log file path easily using command line arguments for enhanced flexibility and ease of use.

#
### Additional:
A comprehensive test case has been implemented to verify the synchronization function. Additionally, folders have been added to facilitate convenient testing of the program.