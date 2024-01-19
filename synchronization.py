# -*- coding: utf-8 -*-
import os
import shutil
import time


# compare files
def are_files_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()


# synchronize function
def synchronize(source_folder_path, replica_folder_path):
    try:
        source_file_list = set(os.listdir(source_folder_path))
        replica_file_list = set(os.listdir(replica_folder_path))

        deleted_files = replica_file_list - source_file_list
        added_files = source_file_list - replica_file_list
        common_files = source_file_list.intersection(replica_file_list)

        # copy new files
        for file in added_files:
            try:
                shutil.copy(os.path.join(source_folder_path, file), replica_folder_path)
            except Exception as e:
                print(f"Error copying file {file}: {e}")

        # remove deleted files
        for file in deleted_files:
            try:
                os.remove(os.path.join(replica_folder_path, file))
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

        # update changed files
        changed_files = []
        for file in common_files:
            source_path = os.path.join(source_folder_path, file)
            target_path = os.path.join(replica_folder_path, file)

            if not are_files_equal(source_path, target_path):
                try:
                    shutil.copy(source_path, target_path)
                    changed_files.append(file)
                except Exception as e:
                    print(f"Error updating file {file}: {e}")
        return deleted_files, added_files, changed_files

    except Exception as e:
        print(f"Error during synchronization: {e}")
        return [], [], []


# file log function
def log_changes(formatted_time, deleted_files, added_files, changed_files, source_folder_path, replica_folder_path, log_file_path):
    with open(log_file_path, 'a') as log_file:
        log_file.write('##################\n')
        log_file.write(f'All data successfully synchronized\nSynchronization time: {formatted_time}\n'
                       f'Source folder: {source_folder_path}\nReplica folder: {replica_folder_path}\n\n'
                       f'Deleted files: {", ".join(deleted_files) if deleted_files else "None"}\n'
                       f'Added files: {", ".join(added_files) if added_files else "None"}\n'
                       f'Changed files: {", ".join(changed_files) if changed_files else "None"}\n'
                       f'##################\n\n\n')


# Inputs validator
def get_valid_input(prompt, input_type, test_value=None):
    while True:
        user_input = input(prompt) if test_value is None else test_value
        try:
            if input_type == 'folder' and (not os.path.isdir(user_input)):
                raise ValueError("The specified path is not a valid folder.")
            
            elif input_type == 'file' and (not os.path.isfile(user_input)):
                raise ValueError("The specified path is not a valid file.")
                
            elif input_type == 'number' and (not user_input.isdigit() or int(user_input) <= 0):
                raise ValueError("Please enter a valid numeric value.")
            elif input_type == 'number':
                return int(user_input)
            
            return user_input
        except ValueError as e:
            print(f"Error: {e}")


# Input parameters
if __name__ == "__main__":
    source_folder_path = get_valid_input('\nPlease enter the full path to the source folder: ', input_type='folder')
    replica_folder_path = get_valid_input('\nPlease enter the full path to the replica folder: ', input_type='folder')
    log_file_path = get_valid_input('\nPlease enter the full path to the file where entered changes will be recorded: ', input_type='file')
    time_interval_minute = get_valid_input('\nPlease enter the synchronization interval in minutes: ', input_type='number')

    try:
        while True:
            deleted_files, added_files, changed_files = synchronize(source_folder_path, replica_folder_path)
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            print('\n\n##################\n')
            print(f'All data successfully synchronized\n'
                    f'Synchronization time: {formatted_time}\n'
                    f'Source folder: {source_folder_path}\nReplica folder: {replica_folder_path}\n\n'
                    f'Deleted files: {", ".join(deleted_files) if deleted_files else "None"}\n'
                    f'Added files: {", ".join(added_files) if added_files else "None"}\n'
                    f'Changed files: {", ".join(changed_files) if changed_files else "None"}\n'
                    f'\n##################\n\n')

            log_changes(formatted_time, deleted_files, added_files, changed_files, source_folder_path, replica_folder_path, log_file_path)
            time.sleep(time_interval_minute * 60)

    except KeyboardInterrupt:
        print("\nThe program has been terminated.\n")