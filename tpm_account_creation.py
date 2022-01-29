import tpm
import main


# TPM Authentication
def tpm_auth(it_account, it_password):
    tpm_url = "https://YOURSERVE.COM"
    tpm_conn = tpm.TpmApiv4(tpm_url,
                            username=it_account,
                            password=it_password)
    return tpm_conn


# Creating account and adding user to a group
def tpm_user_creation(it_account,
                      it_password,
                      new_user_account,
                      new_user_email,
                      new_user_name):
    tpm_conn = tpm_auth(it_account, it_password)
    new_tpm_user_data = {
        "username": new_user_account,
        "email_address": new_user_email,
        "name": new_user_name,
        "role": "normal user",
        'login_dn': f'{new_user_account}@'+'YOURDOMAIN'
    }

    try:
        print('\nTeam password manager:')
        print('Team password manager: Creating an account. Please wait...')
        userid = (tpm_conn.create_user(new_tpm_user_data))
        tpm_conn.add_user_to_group(GroupID='', UserID=userid)
        main.prGreen("\nTeam password Manager: Account has been created")
        return
    except Exception as e:
        main.prRed(f'Team password manager: {e}')
        return
