After git cloning the project into a local folder, please follow these steps:

## 1. Install python and pip locally.
<br>

Use the most recent version available <a href="https://www.python.org/downloads/">here</a>.

The project currently uses Python version 3.9.2.

### pip ###

*Using Linux?*

Use the following command to check whether pip is installed:

```
python -m pip --version
```

*Using Windows?*

```
C:\> py -m pip --version
```

If not installed, use the following commands to install:


*Linux*

```
sudo apt update
sudo apt install python3-pip
```


*Windows*

```
C:\> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
C:\> python get-pip.py

```
<br><br>

## 2. Install pipenv
<br>

Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world.

```
pip install pipenv
```

To check if pipenv was installed correctly, run:

```
pipenv check
```

After this, install git hooks running: 
```
pipenv run pre-commit install
```

For Linux, it is important to check if the current bash has a path to `~/.local/bin`.


<br><br>

## 3. Run project using virtual environment (venv)
<br>
Inside the project's folder, run the following command:
```
pipenv shell
```
This command spawns a shell within the virtualenv.
All `python` and `pip` commands will be executed using the binaries created by the virtual enviroment.
Type 'exit' or 'Ctrl+D' to return.
<br>
<br>
## 4. Install the project dependencies
<br>
This command should be executed within virtualenv.
Execute the `pipenv shell` before install the packages:
Inside the project's folder, run the following command:
```
pipenv install
```
All packages inside `Pipfile` will be installed.
<br>
<br>
## 5. Build the project
<br>
Run command:
```
pyinstaller .\services\extract_files\extract_files.py --onefile
pyinstaller .\services\petrobras\petrobras.py --onefile
pyinstaller .\services\vale\vale.py --onefile
```
<br>
<br>
## 6. Run the project
<br>
Run command:
```
cd .\services\extract_files
python extract_files.py
cd .\services\petrobras
python petrobras.py
cd .\services\vale
python .\services\vale\vale.py
```
<br>
<br>
## 7. Exit from the recently created virtual environment:
<br>
Run command:
```
exit
```
