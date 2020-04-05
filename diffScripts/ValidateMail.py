#pip3 :   https://pypi.org/project/py3-validate-email/

from validate_email import validate_email

for mail in mails :
    print(mail[0])
    if mail[0] == 'None' :
        continue
    tmpMail = mail[0]
    f1.write(tmpMail.ljust(57))
    isValid = validate_email(email_address=mail[0], check_regex=True, check_mx=True, from_address='amir@elementor.com', helo_host='my.host.name', smtp_timeout=10, dns_timeout=10, use_blacklist=True)
    #print(str(isValid.ljust(57)) + "\n")
    if isValid == True :
        print("good")
        f1.write("Valid_mail".ljust(57) + "\n")
    else :
        print("bad_Mail")
        f1.write("bad_mail".ljust(57) + "\n")
