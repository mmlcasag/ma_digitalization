def open_file(file_name):
    return open(file_name, 'w', newline='', encoding='utf-8')

def create_file(file_name):
    return open(file_name, 'w', newline='', encoding='utf-8')

def write(csv_file, csv_content):
    csv_file.write(csv_content)

def close_file(csv_file):
    csv_file.close()