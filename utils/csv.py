import csv

def open_file(file_name):
    return open(file_name, 'w', newline='', encoding='utf-8')

def create_file(file_name):
    return open(file_name, 'w', newline='', encoding='utf-8')

def close_file(csv_file):
    csv_file.close()