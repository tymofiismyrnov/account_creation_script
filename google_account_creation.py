from __future__ import print_function
import os.path
import inquirer
import googleapiclient.errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import time

# If modifying these scopes, delete the file token.json.
import main
# These are the scopes need to work with the script
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user',
          'https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/admin.directory.user.security']


def google_user_creation(new_user_firstname,
                         new_user_lastname,
                         new_user_name,
                         new_user_email,
                         new_user_password):
    # This is an oAuth key taken from Google Developer Console
    account_secret = 'credentials.json'
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                account_secret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("Google Workspace:")

    # This part prompts user to choose a single org unit.
    # Depending on the answer it will take the value from a dictionary below
    # So you can write a short names in "Choices" for better readability and fill in values in the ou_list dictionary.
    ou_choice = [inquirer.List(
        'OrgUnits',
        message="What OrgUnit user should be added to? (Press 'Enter' to choose)",
        choices=['My corp', 'Developers', 'QualityAssurance', 'Managers']
    )]
    answers = inquirer.prompt(ou_choice)  # returns a dict
    unit = answers['OrgUnits']
    ou_list = {'My corp': '/My Company',
               'Developers': '/My Company/Developers',
               'QualityAssurance': '/My Company/QA',
               'Managers': '/My Company/Managers'}
    service = build('admin', 'directory_v1', credentials=creds)

    print("Enter Workspace Groups that user should be added to")
    print("Use full names split by space for multiple groups")
    groups = input("*** (enter group email) ***?: ").lower().split()
    userinfo = {
        "password": new_user_password,
        "primaryEmail": new_user_email,
        "name": {
            "familyName": new_user_lastname,
            "givenName": new_user_firstname,
            "fullName": new_user_name
        },
        'orgUnitPath': ou_list[unit],
        "changePasswordAtNextLogin": "false"
    }

    group_info = {
        "email": new_user_email,
        "role": "MEMBER"
    }

    # Create User
    print('Google Workspace: Creating account...')
    try:
        service.users().insert(body=userinfo).execute()
        main.prGreen("\nGoogle Workspace: Account has been created")
    except googleapiclient.errors.Error as err:
        main.prRed(f'Google Workspace: {err}')

    # Add a User to a group(s)
    add_group = []

    main.prGreen("Google Workspace: Working with groups")
    for x in groups:
        try:
            service.members().insert(groupKey=x, body=group_info).execute()
            # This part should check if user is added to the {x} group
            # But Google needs some time to add user to a group(s), so this part show false errors from time to time
            # time.sleep(3)
            # service.members().get(groupKey=x, memberKey=new_user_email).execute()
        except Exception as e:
            main.prRed(f'Google Workspace: {e}')
            continue
        else:
            add_group.append(x)
    if add_group:
        main.prGreen(f"Google Workspace: New user has been added to the {add_group} groups")
    if not add_group:
        main.prGreen(f"Google Workspace: User hasn't been added to any group")

    time.sleep(1)
    return
