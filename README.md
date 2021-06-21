After git cloning the project into a local folder, please follow these steps:

## 1. Install python and pip locally.
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

## 2. Install pipenv

Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world.

```
pip install pipenv
```

To check if pipenv was installed correctly, run:

```
pipenv check
```

For Linux, it is important to check if the current bash has a path to `~/.local/bin`.

## 3. Run project using virtual environment (venv)
First, set variable PIPENV_VENV_IN_PROJECT to pipenv install packages inside project folder (.venv)
```
export PIPENV_VENV_IN_PROJECT="enabled" 
```

Inside the project's folder, run the following command:
```
pipenv shell
```
This command spawns a shell within the virtualenv.
All `python` and `pip` commands will be executed using the binaries created by the virtual enviroment.
Type 'exit' or 'Ctrl+D' to return.

## 4. Install the project dependencies
This command should be executed within virtualenv.
Execute the `pipenv shell` before install the packages:
Inside the project's folder, run the following command:

```
pipenv install
```
All packages inside `Pipfile` will be installed.

After this, install git hooks running:
```
pipenv run pre-commit install
```

## 5. Build the project
Run command:

```
pyinstaller .\services\extract_files\extract_files.py --onefile
pyinstaller .\services\petrobras\petrobras.py --onefile
pyinstaller .\services\vale\vale.py --onefile
```
## 6. Run the project
Run command:

```
cd .\services\extract_files
python extract_files.py
cd .\services\petrobras
python petrobras.py
cd .\services\vale
python .\services\vale\vale.py

```
## 7. Exit from the recently created virtual environment:
Run command:

```
exit
```
