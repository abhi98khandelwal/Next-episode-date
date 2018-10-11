import smtplib
class SendEmail:
    def __init__(self,email,message):
        self.email = email
        self.message = message
        pass

    def send(self):
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login("abhi98khandelwal","mniak19!!!998")
        server.sendmail(
            "abhi98khandelwal@gmail.com",
            self.email,
            self.message
        )
        server.quit()
if __name__=='__main__':
    a = SendEmail()
    a.send()