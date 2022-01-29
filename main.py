import stdiomask
import os
import random
import ad_account_creation
import google_account_creation
import redmine_account_creation
import tpm_account_creation
import inquirer
import logging


# Color printing functions
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m".format(skk))
def prYellow(skk): print("\033[93m {}\033[00m".format(skk))


if __name__ == '__main__':

    print('\nHi, this script will help you to create basic accounts\n')
    # This is the menu part
    # It prompts user to choose which account he wants to create
    questions = [inquirer.Checkbox(
        'interests',
        message="What account(s) you'd like to create? ('Space' to check an option(s), 'Enter' to proceed)",
        choices=['Active Directory', 'Google Workspace', 'Redmine', 'Team Password Manager']
    )]
    answers = inquirer.prompt(questions)  # returns a dict

    ad_check = False
    gw_check = False
    rm_check = False
    tpm_check = False
    # This part check the booleans. Depends on choices you've made above
    if 'Active Directory' in tuple(answers['interests']):
        ad_check = True
    if 'Google Workspace' in tuple(answers['interests']):
        gw_check = True
    if 'Redmine' in tuple(answers['interests']):
        rm_check = True
    if 'Team Password Manager' in tuple(answers['interests']):
        tpm_check = True
    crd_checks = [ad_check, rm_check, tpm_check]
# Data collection
    for x in crd_checks:
        if x:
            print('Please fill in your credentials')
            break
# Gathers (non-domain admin) account's credentials
# The script expects that Redmine and TPM administrators are the same account
    if rm_check or tpm_check:
        print('\nAccount with an admin privileges at Redmine and TPM: ')
        it_account = input("Enter your account(e.g.: firstname.lastname): ")
        it_password = stdiomask.getpass("Password: ")
# Domain admin credentials for Active Directory
    if ad_check:
        print('\nDomain Admin: ')
        domain_admin_account = input("Enter a Domain Admin's account: ")
        domain_admin_password = stdiomask.getpass("Password: ")

    print("\nPlease fill in a newcomer's info")
# New user's data. You can customize it as you wish
    new_user_firstname = input("Enter new user's firstname: ").capitalize()
    new_user_lastname = input("Enter new user's lastname: ").capitalize()
    new_user_name = new_user_firstname + ' ' + new_user_lastname
    new_user_account = new_user_firstname.lower() + '.' + new_user_lastname.lower()
    new_user_email = f'{new_user_account}@{your_domain}'
    # Here the script generates a password, you can use my generator or any other, or type the password in manually
    new_user_password = f'SomeText' + ''.join(random.sample('0123456789', 7))
    if ad_check:
        ad_account_creation.ad_user_creation(domain_admin_account,
                                             domain_admin_password,
                                             new_user_account,
                                             new_user_password,
                                             new_user_email,
                                             new_user_firstname,
                                             new_user_lastname,
                                             new_user_name)
    if gw_check:
        google_account_creation.google_user_creation(new_user_firstname,
                                                     new_user_lastname,
                                                     new_user_name,
                                                     new_user_email,
                                                     new_user_password)
    if rm_check:
        redmine_account_creation.redmine_prompt(it_account,
                                                it_password,
                                                new_user_firstname,
                                                new_user_lastname,
                                                new_user_account,
                                                new_user_email)
    if tpm_check:
        tpm_account_creation.tpm_user_creation(it_account,
                                               it_password,
                                               new_user_account,
                                               new_user_email,
                                               new_user_name)

    prGreen('\nFinished')
# This part prints out the result for a User which used the Script
    prYellow("User's data (generates despite results of the script):")
    if ad_check or rm_check or tpm_check:
        prYellow(f"full name = {new_user_name}")
        prYellow(f"account = {new_user_account}")
    if gw_check:
        prYellow(f"email = {new_user_email}")
    if ad_check or gw_check:
        prYellow(f"password = {new_user_password}")
    os.system("pause")
