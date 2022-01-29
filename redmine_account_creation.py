from redminelib import Redmine
import redminelib.exceptions
import time

import main

redmine_url = 'https://yourredmineserver.com'
redmine_version = ''


# Authentication to Redmine
def redmine_auth(it_account, it_password):
    redmine = Redmine(redmine_url,
                      version=redmine_version,
                      username=it_account,
                      password=it_password)
    return redmine


# Prompting user if he wants to create a Redmine account or not
def redmine_prompt(it_account, it_password, new_user_firstname, new_user_lastname, new_user_account, new_user_email):
    redmine = redmine_auth(it_account, it_password)
    redmine_user_check(new_user_firstname=new_user_firstname,
                       new_user_lastname=new_user_lastname,
                       new_user_account=new_user_account,
                       new_user_email=new_user_email,
                       redmine=redmine)


# This function checks if user already exists in Redmine
def redmine_user_check(new_user_firstname, new_user_lastname, new_user_account, new_user_email, redmine):
    print('\nRedmine:')
    print('Redmine: Checking existing users. Please wait...')
    existence = False
    curr_user = None
    try:
        for user in redmine.user.all():
            curr_user = user
            if new_user_firstname.lower() == str.lower(user.firstname) and new_user_lastname.lower() == str.lower(
                    user.lastname):
                existence = True
                break

        # if existence is True and curr_user is not None:
        if existence and curr_user:
            main.prRed(f'Redmine: User {curr_user.firstname} {curr_user.lastname} or {curr_user.login} already exists')
        else:
            print('Redmine: No matches found')
            time.sleep(1)
            redmine_user_creation(new_user_account, new_user_firstname, new_user_lastname, new_user_email, redmine)
    except redminelib.exceptions.AuthError as err:
        main.prRed(f"Redmine: {err=}, {type(err)=}")
        pass


# # This function creating a new account in Redmine
def redmine_user_creation(new_user_account, new_user_firstname, new_user_lastname, new_user_email, redmine):
    print('Redmine: Creating an account. Please wait...')
    try:
        user = redmine.user.create(
            login=new_user_account,
            # password='password', #You can enter a variable here if you want to generate a password
            firstname=new_user_firstname,
            lastname=new_user_lastname,
            mail=new_user_email,
            auth_source_id=3,
            mail_notification='only_my_events',
            must_change_passwd=False
        )
        # Here you can select a project(s) which a user should be added to, as well as his role
        redmine.project_membership.create(project_id='project#1', user_id=user.id, role_ids=[0])
        redmine.project_membership.create(project_id='project#2', user_id=user.id, role_ids=[1])
    except redminelib.exceptions.ValidationError as err:
        main.prRed(f"Redmine: Unexpected {err=}, {type(err)=}")
        pass
    main.prGreen('\nRedmine: Account has been created')
