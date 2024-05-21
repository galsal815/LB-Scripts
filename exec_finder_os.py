import os
import stat
import argparse
from glob import glob

def is_executable_by_anyone(permissions):
    return bool(permissions & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

def list_executable_files(directory):
    exec_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if is_executable_by_anyone(os.stat(filepath).st_mode):
                exec_files.append(filepath)
    return exec_files

def count_permissions(directory):
    permission_counts = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            permissions = oct(os.stat(filepath).st_mode)[-3:]
            if permissions in permission_counts:
                permission_counts[permissions] += 1
            else:
                permission_counts[permissions] = 1
    return permission_counts

def find_min_max_permissions(permission_counts):
    min_perm = min(permission_counts, key=permission_counts.get)
    max_perm = max(permission_counts, key=permission_counts.get)
    return min_perm, max_perm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List executable files and count file permissions')
    parser.add_argument('directory', type=str, help='Directory to search in')
    args = parser.parse_args()
    
    directory = args.directory
    
    exec_files = list_executable_files(directory)
    for file in exec_files:
        print(file)
    
    permission_counts = count_permissions(directory)
    min_perm, max_perm = find_min_max_permissions(permission_counts)
    print("Permission with max files: {} ({} files)".format(max_perm, permission_counts[max_perm]))
    print("Permission with min files: {} ({} files)".format(min_perm, permission_counts[min_perm]))
