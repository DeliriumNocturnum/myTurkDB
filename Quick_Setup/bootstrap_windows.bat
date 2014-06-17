@echo Downloading Dependencies (Pip for Windows)

.\wget\wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py

@echo Downloading Python (2.7.6)

.\wget\wget --no-check-certificate https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi

@echo Downloading MySQL (5.6)

.\wget\wget http://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-community-5.6.19.0.msi

@echo Setting up MySQL Installer

START /wait msiexec /i mysql-installer-community-5.6.19.0.msi /quiet

@echo Installing MySQL 5.6

START /wait "" "C:\Program Files (x86)\MySQL\MySQL Installer\MySQLInstallerConsole.exe" --config=mysql-server-5.6-win32:passwd=root --product=* --catalog=mysql-5.6-win32 --action=install --type=full

SET PATH=%PATH%;"C:\Program Files (x86)\MySQL\MySQL Server 5.6\bin";"C:\Program Files\MySQL\MySQL Server 5.6\bin"

@echo Finished installing MySQL!

@echo Installing Python 2.7.6

START /wait msiexec /i python-2.7.6.msi /passive

SET PATH=%PATH%;C:\Python27\

@echo Finished installing Python!

@echo Installing PIP

python get-pip.py

@echo Finished installing PIP

SET PATH=%PATH%;C:\Python27\scripts\

@echo Installing Beautiful Soup Module

pip install beautifulsoup4

@echo Installing Mechanize Module

pip install mechanize

@echo Installing MySQL-Python Module

REM START /wait MySQL-python-1.2.5.win32-py2.7.exe

easy_install mysql-python

@echo Setting up MySQL

mysql -uroot -proot < setup.sql

mysql -u mturk -p"mturk" mturk < tables.sql