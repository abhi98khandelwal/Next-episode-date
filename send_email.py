import smtplib
class SendEmail:
    """
    A class to send email given the email and message.


    Args:
        email (str): email id of recipient.
        message (str): message that needs to be sent.
    """


    #username : senders gmail username
    username = 'abhi98khandelwal'
    #password : senders gmail password
    password = 'mniak19!!!998'
    def __init__(self,email,message):
        self.email = email
        self.message = 'Subject: {}\n\n{}'.format("Tv Series next episode dates", message)

    def send(self):
        #Method sends the mail via smtp lib
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login(self.username,self.password)
        server.sendmail(
            "abhi98khandelwal@gmail.com",
            self.email,
            self.message
        )
        server.quit()
if __name__=='__main__':
    email = input("Email Id: ")
    message = input("Message: ")
    a = SendEmail(email,message)
    a.send()