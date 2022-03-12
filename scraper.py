#!python3
# free_game.py
# finds this weeks free game on the Epic game store and prints it to a .txt file along with the valid date


import time
import os
import datetime
import argparse
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client


def send_email(message, email_address, email_password, recipients_emails):
    # Send weekly emails to personal account from a dummy account (freeGameAutomated@outlook.com)
    try:
        import smtplib
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(email_address, email_password)
        for user_email_address in recipients_emails:
            smtpObj.sendmail('freeGameAutomated@outlook.com', user_email_address,
                             "Subject: This weeks free epic game \n" + message)
        smtpObj.quit()
    except:
        # if the email fails to send add a note to the log file
        text_file = open('free_epic_game.txt', 'a')
        text_file.write('**Email for log above failed to send (Date: {})**'.format(today.strftime('%d/%m/%Y')))


def send_text(message, user_phone_number):  # function needs fixing
    try:
        accountSID = 'AC06167f5101f43014f24c33686efb2f84'
        authToken = '390e192cb8b9fe03e0b4717fbffaa231'
        twilioCli = Client(accountSID, authToken)
        myTwilioNumber = '+18312923438'
        twilioCli.messages.create(body=message, from_=myTwilioNumber, to=user_phone_number)
    except:
        text_file = open('free_epic_game.txt', 'a')
        text_file.write('**Txt message for log above failed to send (Date: {})**'.format(today.strftime('%d/%m/%Y')))


def update_log():
    # checks if the free game log file has been created (if it has it appends this weeks log to the existing file)
    if (today.year == 2020 and today.month == 5) and today.day == 23:
        text_file = open('free_epic_game.txt', 'w')

    else:
        text_file = open('free_epic_game.txt', 'a')

    # write the log info to free_epic_game.txt
    text_file.write(today.strftime('%d/%m/%Y') + '-' + (today + next_wk).strftime('%d/%m/%Y') + '\n')
    text_file.write('This weeks free game is: ' + free_game.text + '\n')
    text_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--email-address', type=str, required=True)
    parser.add_argument('--email-password', type=str, required=True)
    parser.add_argument('--email-list', nargs='+', required=True)
    args = parser.parse_args()

    # set CWD
    os.chdir(os.path.join(os.getcwd(), 'chrome-drivers'))

    # user details
    USER_EMAILS = args.email_list
    # USER_PHONE_NUMBER = None

    # create web driver object
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome()

    # open chrome and epic store free games page and wait 10 secs for web page animations to finish
    driver.get("https://www.epicgames.com/store/en-US/free-games")
    time.sleep(10)

    # create a datetime object with today's date
    today = datetime.datetime.now()
    # create a 7day time delta object
    next_wk = datetime.timedelta(days=7)

    # create an object from the HTML element containing the free games name
    xpath = '/html/body/div[1]/div/div[4]/main/div[3]/div/div/div/div/div[2]/span/div/div/section/div/div[1]/div/div/a/div/div/div[3]/span[1]'
    free_game = driver.find_element(by=By.XPATH, value=xpath)
    message = '\n' + today.strftime('%d/%m/%Y') + '-' + (today + next_wk).strftime(
        '%d/%m/%Y') + '\n' + 'This weeks free game is: ' + free_game.text

    # update log and send user messages
    update_log()
    send_email(message, USER_EMAILS)
    # send_text(message, USER_PHONE_NUMBER)

    # close driver object
    driver.quit()
