# To create a virtual environment for the project

  # Using Linux?
  python3 -m venv env

  # Using Windows?
  python -m venv env

# To activate the virtual environment recently created
  
  # Using Linux?
  Run command `source ./env/bin/activate` in the project root folder
  
  # Using Windows?
  1. Run Windows Powershell as Administrator
  2. Set-ExecutionPolicy Bypass
  3. Choose option "Y"
  4. Close Windows Powershell
  5. Run command `.env\Source\activate` in the project root folder

# To install the project dependencies
pip install numpy
pip install pandas
pip install openpyxl
pip install pyinstaller

# To run the project

  # Using Linux?
  python3 vale_mro.py

  # Using Windows?
  python vale_mro.py

# To build the project
pyinstaller vale_mro.py --onefile
