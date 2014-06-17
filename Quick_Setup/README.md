Quick Setup Scripts for myTurkDB
========

These  are platform-specific scripts to help setup an user's environment for myTurkDB

### Quick Setup on Windows 7

##### Requisites

+ An OS running Windows 7 or later
+ Python 2.7.6 -- https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi 
+ MySQL 5.6 -- http://dev.mysql.com/downloads/file.php?id=452278

##### Installation

The quick setup script for Windows can be run from the same directory that you have downloaded the Requisites into from elevated cmd: quick_install.bat

The script will automatically install MySQL Server 5.6.

The script will automatically install Python 2.7.6.

The script will automatically install the needed python modules.

The script will set up the tables.


##### Tested Versions and known issues

Quick Setup for Windows has been tested on

+ Windows 7 Professional x64 - Python 2.7.6
+ Windows 8.1 Pro x64 (Build 9600) - Python 2.7.6

### Quick Setup on Mac OS X

##### Requisites

+ A Mac running OS X 10.8.5 or later
+ Python 2.7.2 or later (already ships with OS X 10.8.5+)
+ Xcode 5.1.1 or later
+ The Xcode Command Line tools (can be installed from Xcode Preferences)

##### Installation

The quick setup script for Mac OS X can be ran in a Terminal with `sh bootstrap_osx.sh`

The script will automatically download all the necessary Python dependencies if needed.
MySQL will also be automatically downloaded and installed for OS X, as well as the myTurkBD tables.

##### Tested Versions and known issues

Quick Setup for OS X has been tested on 

+ Mac OS X Yosemite - 10.10 (Build 14A238x) - Python 2.7.6
  + The script may fail at installing the MySQL Startup Item. This will not impact myTurkDB, but you will have to manually start up MySQL every time you reboot.

### Quick Setup on Ubuntu

##### Requisites

+ A PC running Ubuntu 12.04 or later
+ Python 2.7.2 or later (the script will automatically install it if it's not there)
+ 500MB of disk space or more

##### Installation

The quick setup script (Bootstrap) for Ubuntu can be ran in a Terminal with `sh bootstrap_ubuntu.sh`

Due to the nature of the MySQL installer, if you install it for the first time, you MUST put a root password. The script will ask you for the root user's password to set up the myTurkDB tables (at the end of the setup).

The script will automatically download all the necessary Python dependencies if needed.
MySQL will also be automatically downloaded and installed if it's not there, as well as the myTurkBD tables.

##### Tested Versions and known issues

Bootstrap for Ubuntu has been tested on 

+ Ubuntu 12.04 - Linux 3.5.0-51-generic x86_64 x86_64 - Python 2.7.6
  + A root password is required to be set during setup, it will not be done automatically.
