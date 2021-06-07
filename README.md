After git cloning the project into a local folder, please follow these steps:

### 1. Install Python locally.
   
   Use the most recent version available <a href="https://www.python.org/downloads/">here</a>.
   The project currently uses Python version 3.9.2.

### 2. Navigate into the project root folder.

### 3. Create a virtual environment for the project:
   
  #### If you are using Linux:
  - Run command `python3 -m venv env`
  #### If you are using Windows:
  - Run command `python -m venv env`
  
### 4. Activate the recently created virtual environment:
  
  #### If you are using Linux:
  - Run command `source ./env/bin/activate`
  #### If you are using Windows:
  - Run Windows Powershell as Administrator
  - Run command `Set-ExecutionPolicy Bypass`
  - Choose the option "Y"
  - Close Windows Powershell
  - Run command `.env\Source\activate`

### 5. Install the project dependencies
  - pip install numpy
  - pip install pandas
  - pip install openpyxl
  - pip install pyinstaller

### 6. Build the project
  - Run command `pyinstaller vale_mro.py --onefile`
  
### 7. Run the project

  #### If you are using Linux:
  - Run command `python3 vale_mro.py`
  #### If you are using Windows:
  - Run command `python vale_mro.py`
