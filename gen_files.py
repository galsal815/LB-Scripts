import os
import sys

def generate_permission_strings():
    permissions = []
    for i in range(512):
        binary_str = '{:09b}'.format(i)
        perm_str = ''.join(['r' if binary_str[j] == '1' else '-' for j in range(0, 9, 3)] + 
                           ['w' if binary_str[j] == '1' else '-' for j in range(1, 9, 3)] + 
                           ['x' if binary_str[j] == '1' else '-' for j in range(2, 9, 3)])
        permissions.append(perm_str)
    return permissions

def permissions_to_octal(perm):
    octal_str = ''
    for i in range(0, 9, 3):
        perm_triplet = perm[i:i+3]
        octal_value = (4 if perm_triplet[0] == 'r' else 0) + \
                      (2 if perm_triplet[1] == 'w' else 0) + \
                      (1 if perm_triplet[2] == 'x' else 0)
        octal_str += str(octal_value)
    return octal_str

def create_files(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    permissions = generate_permission_strings()
    for perm in permissions:
        octal_perm = permissions_to_octal(perm)
        filename = "{}.txt".format(perm)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            f.write("Permissions: {} ({})".format(perm, octal_perm))
        os.chmod(filepath, int(octal_perm, 8))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gen_files.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    create_files(directory)

