import os
import shutil
import re


def get_absolute_path():
    return os.getcwd()


# from a file name like "foobar.txt"
# returns "foobar"
def get_file_name(file_name):
    return os.path.splitext(file_name)[0]


# from a file name like "foobar.txt"
# returns "txt"
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].replace(".", "").lower()


def get_file_size(file_name):
    return os.stat(file_name).st_size


def create_folder(folder_name, subfolder_name=""):
    if not subfolder_name:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    else:
        if not os.path.exists(os.path.join(folder_name, subfolder_name)):
            os.makedirs(os.path.join(folder_name, subfolder_name))


def delete_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)


def get_files_list(folder_name, file_extension_list=[]):
    files_list = []

    if not os.path.isdir(folder_name):
        return files_list

    if len(file_extension_list) == 0:
        files_list = os.listdir(folder_name)
    else:
        for file_name in os.listdir(folder_name):
            for file_extension in file_extension_list:
                if file_name.endswith(file_extension):
                    files_list.append(file_name)

    return files_list


# Apply a regex to file name and create a folder with string returned
# Move all files that match with regex to folder
def move_files_by_regex_name(input_folder, output_folder, regex):
    file_list = get_files_list(input_folder)

    if len(file_list) > 0:
        create_folder(output_folder)

    file_list.sort()
    for img_name in file_list:
        found = re.search(regex, img_name)
        if found:
            destination_folder = os.path.join(output_folder, found[0])
            create_folder(destination_folder)
            origin_file_src = os.path.join(input_folder, img_name)
            shutil.copy(origin_file_src, destination_folder)


def copy_file(full_source_path, full_destination_path):
    shutil.copyfile(full_source_path, full_destination_path)
