
photo_Directory = ''


def setupIGHelper():
    import os
    if "GameCounter.txt" not in os.listdir():
        with open('GameCounter.txt', 'w+') as file:
            file.write('1')
            file.close()

def getCurrentCounterTxtFile():
    with open('GameCounter.txt', 'r') as file:
        return int(file.read())


def increaseCounterTxtFile():
    with open('GameCounter.txt', 'r+') as file:
        number = int(file.read())
        file.truncate(0)
        file.seek(0)
        file.write(str(number + 1))

def chooseGame(game_Number):
    import os
    game_Choices = [game.replace('.JPG',"") for game in os.listdir('D:\PS3 Pictures\JPG') if "Open Case" not in game]
    game_Choices.sort()
    try:
        return game_Choices[game_Number-1]
    except IndexError:
        print("No new games. Closing application.")
        exit()

def getPhotoURL(user_Choice):
    return photo_Directory + user_Choice + '.JPG'
def getPhotoOpenCaseURL(user_Choice):
    return photo_Directory + user_Choice + ' Open Case.JPG'


def getGameWikipediaSummary(game):
    import wikipedia, re
    print("Getting wikipedia information for " + game_Of_The_Day)
    game = game.replace(".JPG"," (video game)")
    game_Article = wikipedia.page(game)
    result = re.sub(r"([\xe9\xef])", "", game_Article.summary[0:2000]) #Removes characters with accents over them.

    print("Article from wikipedia:")
    print(result)
    return result

def emailVideoAndDescription():



    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    sender_email = "collectionspreserved@gmail.com"
    receiver_email = "doncapodilupo@aim.com"
    msg = MIMEMultipart()
    msg['Subject'] = 'Game of the Day: ' + game_Of_The_Day
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msgText = MIMEText('<b>%s</b>' % game_Info, 'html')
    msg.attach(msgText)

    with open(getPhotoURL(game_Of_The_Day), 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename="gameOTD.jpg")
        msg.attach(img)
    with open(getPhotoOpenCaseURL(game_Of_The_Day), 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename="gameOTDOpenCase.jpg")
        msg.attach(img)



    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login('collectionspreserved@gmail.com',
                         input("Enter Password for CollectionsPreserved@gmail.com: "))
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)










if __name__ == '__main__':

    setupIGHelper()

    game_Of_The_Day = chooseGame(getCurrentCounterTxtFile())

    print(game_Of_The_Day)

    game_Info = getGameWikipediaSummary(game_Of_The_Day)

    emailVideoAndDescription()

    increaseCounterTxtFile()




