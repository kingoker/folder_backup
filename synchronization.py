# -*- coding: utf-8 -*-
import os
import shutil
import time


def are_files_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()


def synchronize(source_folder_path, replica_folder_path, indent=''):
    try:
        source_items = set(os.listdir(source_folder_path))
        replica_items = set(os.listdir(replica_folder_path))

        added_items, deleted_items, changed_items = set(), set(), set()

        for item in source_items - replica_items:  # added_items
            source_path, replica_path = os.path.join(source_folder_path, item), os.path.join(replica_folder_path, item)

            try:
                added_items.add(item)
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, replica_path)
                else:
                    shutil.copy(source_path, replica_path)
            except Exception as e:
                print(f"{indent}Error copying {os.path.basename(item)}: {e}")

        for item in replica_items - source_items:  # deleted_items
            item_path = os.path.join(replica_folder_path, item)

            try:
                deleted_items.add(item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            except Exception as e:
                print(f"{indent}Error deleting {os.path.basename(item)}: {e}")

        for item in source_items.intersection(replica_items):  # common_items
            source_path, replica_path = os.path.join(source_folder_path, item), os.path.join(replica_folder_path, item)

            try:
                if os.path.isdir(source_path):
                    deleted, added, changed = synchronize(source_path, replica_path, indent + '  ')
                    deleted_items.update(deleted)
                    added_items.update(added)
                    changed_items.update(changed)
                elif not are_files_equal(source_path, replica_path):
                    changed_items.add(item)
                    shutil.copy(source_path, replica_path)
            except Exception as e:
                print(f"{indent}Error processing {os.path.basename(item)}: {e}")

        return deleted_items, added_items, changed_items

    except Exception as e:
        print(f"{indent}Error during synchronization: {e}")
        return set(), set(), set()


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


def changes_info(formatted_time, deleted_items, added_items, changed_items, source_folder_path, replica_folder_path, log_file_path, indent=''):
    with open(log_file_path, 'a') as log_file:
        log_content = (
            f'{indent}##################\n\n'
            f'{indent}All data successfully synchronized\n{indent}Synchronization time: {formatted_time}\n'
            f'{indent}Source folder: {source_folder_path}\n{indent}Replica folder: {replica_folder_path}\n\n'
            f'{indent}Deleted: {", ".join(deleted_items) if deleted_items else "None"}\n'
            f'{indent}Added: {", ".join(added_items) if added_items else "None"}\n'
            f'{indent}Changed: {", ".join(changed_items) if changed_items else "None"}\n'
            f'\n{indent}##################\n\n\n'
        )
        log_file.write(log_content)
        print(log_content)



if __name__ == "__main__":
    source_folder_path = get_valid_input('\nPlease enter the full path to the SOURCE folder: ', input_type='folder')
    replica_folder_path = get_valid_input('\nPlease enter the full path to the REPLICA folder: ', input_type='folder')
    log_file_path = get_valid_input('\nPlease enter the full path to LOG file: ', input_type='file')
    time_interval_minute = get_valid_input('\nPlease enter the synchronization interval in minutes: ', input_type='number')
    
    while True:
        deleted_items, added_items, changed_items = synchronize(source_folder_path, replica_folder_path)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        changes_info(formatted_time, deleted_items, added_items, changed_items, source_folder_path, replica_folder_path, log_file_path, indent='')
        time.sleep(time_interval_minute * 60)