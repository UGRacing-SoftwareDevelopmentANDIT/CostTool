# Costing Web App

UGRacing's own tool for creating a BOM (Bill of Materials) and partial CBOM (Costed Bill of Materials) for the Formula Student UK static costing event. This tool aims to create a more streamlined experience for engineers, removing as much of the guess work and making the final product for competition more consistent; as such creating an overall better entry.

Data from the Costing Tool will be exported in a suitable format for easy and automated transfer to the official online FSUK tool.

## Prerequisites

Python 3.10+, Django 3.2.8

## Installation

Begin by cloning the repository to your local machine:

`git clone https://github.com/UGRacing-IT/recruit-onboarding`

Create a virtual environment for dependencies:

Linux:

`virtualenv <path-to-venv>`

Windows:

`python -m venv <path-to-venv>`

Activate the virtual environment using the commands for your OS and CLI of choice:

| Platform | Shell | Command to activate virtual environment |
| :-: | :-: | :-: |
| POSIX | bash/zsh | source \<venv-path>/bin/activate |
| | fish | source \<venv-path>/bin/activate.fish |
| | csh/tsch | source \<venv-path>/bin/activate.csh |
| | Powershell | \<venv-path>/bin/Activate.ps1 |
| Windows | cmd.exe | \<venv-path>\Scripts\activate.bat |
| | Powershell | \<venv-path>\Scripts\Activate.ps1 |

Dependencies are then installed using `pip`:

`pip install -r requirements.txt`

Dependencies are now installed.

To complete the initial Django setup, the following needs to be run:

`python manage.py makemigrations` and then,

`python manage.py migrate`

This "imports" the changes made to the models throughout development.

To run the Django web app, run the following:

`python manage.py runserver`

You're now all set to continue development.

### Installation Problems

If you have an issue saying that \<some table\> cannot be found. Try deleting all `__pycache__` files and the `db.sqlite3` file then run the following:

`python manage.py makemigrations` and then,

`manage.py migrate --run-syncdb`

This should hopefully fix any issues.

## Features

TBA

## Contributors

* Jolie Bonner
* Lewis Tse

## License

TBD
