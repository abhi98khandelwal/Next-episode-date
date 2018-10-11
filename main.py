from get_message import GetMessage
from send_email import SendEmail
from database import Database
if __name__ == '__main__':
    user = 'root'
    password = ''
    db = 'innovacer'

    n = int(input("Number of queries"))
    for query in range(n):
        email=input("Email address")
        series = input("TV Series").split(',')
        message = "\n"
        d = Database(user,password,db)
        d.write(email,series)
        for i in series:
            a = GetMessage(i)
            print(a.get_imdb_url())
            message+="Tv series name: "+i+"\n"
            message+="Status: "+a.get_episode_date()+"\n"
            print(message)
            message+="\n"

        a = SendEmail(email,message)
        a.send()