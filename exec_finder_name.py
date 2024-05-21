import os
import sys
import argparse

def list_executable_files_by_name(directory):
    executable_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.basename(file)
            if len(filename) >= 12 and filename[-4:] == '.txt':
                permissions_str = filename[-12:-4]
                if 'x' in permissions_str[1::3]:  # Check the 'x' bits in the permission string
                    executable_files.append(os.path.join(root, file))
    return executable_files

def count_file_permissions(files):
    permissions_count = {}
    for file in files:
        permission = file.split('/')[-1][-12:-4]
        permissions_count[permission] = permissions_count.get(permission, 0) + 1
    return permissions_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List executable files.")
    parser.add_argument('directory', type=str, help="The directory to search for executable files.")
    args = parser.parse_args()

    executable_files = list_executable_files_by_name(args.directory)
    print("Executable files:")
    for file in executable_files:
        print(file)

    permissions_count = count_file_permissions(executable_files)
    print("\nFile permissions count:")
    for permission, count in permissions_count.items():
        print("Permission: {} - Count: {}".format(permission, count))

    max_permission = max(permissions_count, key=permissions_count.get)
    min_permission = min(permissions_count, key=permissions_count.get)
    print("\nPermission with maximum files: {}".format(max_permission))
    print("Permission with minimum files: {}".format(min_permission))
