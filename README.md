# Account creation script

Will help you to create basic accounts for your organization (Active Directory, Google, Redmine, Team password manager)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Install Python

I've used Python3.9 (Windows 10) for this project.
You can find it by the [link](https://www.microsoft.com/store/productId/9P7QFQMJRFP7)

### Clone using Git

Run in terminal:
```
cd /path/to/project/folder
git clone https://github.com/tymofiismyrnov/account_creation_script.git
```

### Installing required modules

Update pip by running the folowing:

```
pip install --upgrade pip
```

Install all needed modules with the following command:

```
pip install -r /path/to/project/requirements.txt
```

## How to use

* You will need network access to all the services.
So you should be in the same network as they all are
* Unless they are exposed to the world (which I think they aren't)
* Being in the project's directory run: 
```
py main.py 
```
* Python version could differ, change the command in that case, e.g Python3, python3.9, python3.10, etc.
* Follow the instructions on the screen

### How to hardcode your credentials (NOT RECOMMENDED!)

* open main.py file with any text editor or IDE
* Almost at the top of the file you can find four variables which look like this:
```
    it_account = input("Enter your account: ")
    it_password = stdiomask.getpass("Password: ")
    domain_admin_account = input("Enter a Domain Admin's account: ")
    domain_admin_password = stdiomask.getpass("Password: ")
```
* Replace value after equality sign for each variable with your credentials
* Values should be wrapped in parentheses and look like this: 
```
    it_account = 'my_login'
    it_password = 'MyPa33w0rd'
    domain_admin_account = 'my_domainadmin_login'
    domain_admin_password = 'MySup@S3qrePa33w0rd'
```