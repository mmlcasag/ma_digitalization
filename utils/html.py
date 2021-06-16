def open_file(file_name):
    return open(file_name, 'w', newline='', encoding='utf-8')

def create_file(file_name):
    return open(file_name, 'w', newline='', encoding='utf-8')

def write(html_file, html_content):
    html_file.write(html_content)

def close_file(html_file):
    html_file.close()

def get_header():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        * {
        font-family: Arial;
        font-size: x-small;
        }
        th {
        text-align: left;
        padding: 3px;
        }
        tr {
        text-align: left;
        padding: 3px;
        }
        td {
        text-align: left;
        padding: 3px;
        }
    </style>
    </head>
    <body>
    '''

def get_footer():
    return '''
    </body>
    </html>
    '''