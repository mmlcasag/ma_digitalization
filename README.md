After git cloning the project into a local folder, please follow these steps:

## 1. Install python and pip locally.

### python ###

Use the most recent version available <a href="https://www.python.org/downloads/">here</a>.

The project currently uses Python version 3.11.3.

### pip ###

To check if pip is installed, run:

*Using Linux?*
```
python -m pip --version
```

*Using Windows?*
```
C:\> py -m pip --version
```

If not installed, run the following commands to install:

*Using Linux?*
```
sudo apt update
sudo apt install python3-pip
```

*Using Windows?*
```
C:\> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
C:\> python get-pip.py
```

To update pip to latest version:
```
python.exe -m pip install --upgrade pip
```

The project currently uses pip version 23.1.2.

## 2. Install pipenv

Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world.

To check if pipenv is installed, run:
```
pipenv check
```

If not installed, run the following command to install:
```
pip install pipenv
```

For Linux, it is important to check if the current bash has a path to `~/.local/bin`.

## 3. Run project using virtual environment (venv)

*Using Linux?*

First, set variable PIPENV_VENV_IN_PROJECT to pipenv install packages inside project folder (.venv)

```
export PIPENV_VENV_IN_PROJECT="enabled" 
```

*Using Windows?*

Inside the project's folder, run the following command:

```
mkdir .venv
```

Now, inside the project's folder, run the following command:

```
pipenv shell
```

This command spawns a shell within the virtualenv.

All `python` and `pip` commands will be executed using the binaries created by the virtual enviroment.

Type 'exit' or 'Ctrl+D' to return.

## 4. Install the project dependencies

This command should be executed within the virtual environment.
Execute the `pipenv shell` before install the packages:

Inside the project's folder, run the following command:
```
pipenv install
pipenv install --dev
```

It is also necessary to generate the packages that the project itself generates, so you need to run the following command:

```
pipenv install -d --editable .
```
These packages are configured in the file `setup.cfg`, if you need to add new packages, you need to run the above command again


All packages inside `Pipfile` will be installed.

After this, install git hooks running:
```
pipenv run pre-commit install
```

## 5. Build the project

Run command:
```
pyinstaller services/extract_files/extract_files.py --onefile
pyinstaller services/petrobras/petrobras.py --onefile
pyinstaller services/vale/vale.py --onefile
```

## 6. Run the project

Run command:

```
cd services/extract_files
python extract_files.py
```
```
cd services/petrobras
python petrobras.py
```
```
cd services/vale
python vale.py
```

## 7. Exit the virtual environment:

Run command:
```
exit
```
