After git cloning the project into a local folder, please follow these steps:

1. Install Python locally.
   Use the most recent version available <a href="https://www.python.org/downloads/">here</a>.
   The project currently uses Python version 3.9.2.

2. Navigate into the project root folder.

3. Create a virtual environment for the project:
   
  3.1. If you are using Linux:
    - Run command `python3 -m venv env`
  3.2. If you are using Windows:
    - Run command `python -m venv env`
  
4. Activate the recently created virtual environment:
  
  4.1. If you are using Linux:
    - Run command `source ./env/bin/activate`
  4.2. If you are using Windows:
    - Run Windows Powershell as Administrator
    - Run command `Set-ExecutionPolicy Bypass`
    - Choose the option "Y"
    - Close Windows Powershell
    - Run command `.env\Source\activate`

5. Install the project dependencies
  - pip install numpy
  - pip install pandas
  - pip install openpyxl
  - pip install pyinstaller

6. Build the project
  - Run command `pyinstaller vale_mro.py --onefile`
  
7. Run the project

  7.1. If you are using Linux:
  - Run command `python3 vale_mro.py`
  7.2. If you are using Windows:
  - Run command `python vale_mro.py`
