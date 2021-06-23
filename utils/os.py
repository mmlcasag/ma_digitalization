import os


# from a file name like "foobar.txt"
# returns "foobar"
def get_file_name(file_name):
    return os.path.splitext(file_name)[0]


# from a file name like "foobar.txt"
# returns "txt"
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].replace(".", "")


def create_folder(folder_name, subfolder_name=""):
    if not subfolder_name:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    else:
        if not os.path.exists(os.path.join(folder_name, subfolder_name)):
            print(os.path.join(folder_name, subfolder_name))
            os.makedirs(os.path.join(folder_name, subfolder_name))


def get_files_list(folder_name, file_extension_list=[]):
    files_list = []

    if len(file_extension_list) == 0:
        files_list = os.listdir(folder_name)
    else:
        for file_name in os.listdir(folder_name):
            for file_extension in file_extension_list:
                if file_name.endswith(file_extension):
                    files_list.append(file_name)

    return files_list
