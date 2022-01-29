from pyad import *
import time


# Prompting user if he wants to create an AD account or not.
# Creating account if answer is 'y' or 'yes'
# Adding user to 'other' and 'PWD_policy_contractor' groups
import main


def ad_user_creation(domain_admin_account,
                     domain_admin_password,
                     new_user_account,
                     new_user_password,
                     new_user_email,
                     new_user_firstname,
                     new_user_lastname,
                     new_user_name):

    try:
        print('\nActive Directory:')
        print('Active Directory: Creating an account. Please wait...')
        # Auth to an AD Server
        pyad.set_defaults(ldap_server="YOURDOMAINCONTROLLER.COM",
                          username=domain_admin_account,
                          password=domain_admin_password)
        ou = pyad.adcontainer.ADContainer.from_dn("cn=, dc=, dc=")
        # Creating a user object
        new_domain_user = pyad.aduser.ADUser.create(new_user_account,
                                                    ou,
                                                    new_user_password,
                                                    optional_attributes={"mail": [new_user_email],
                                                                         "givenName": [new_user_firstname],
                                                                         "sn": [new_user_lastname],
                                                                         "displayName": [new_user_name]}
                                                    )
        print('Active Directory: Adding user to groups...')
        time.sleep(1)
        # Adding user to groups is pretty straightforward
        group_1 = adgroup.ADGroup.from_cn("Workers")
        group_2 = adgroup.ADGroup.from_cn("Managers")
        group_1.add_members(new_domain_user)
        group_2.add_members(new_domain_user)
        main.prGreen('\nActive Directory: Account has been created\n')
        return
    except Exception as e:
        main.prRed(f'Active Directory: error.{e}')
        pass
