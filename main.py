from get_message import GetMessage
from send_email import SendEmail
if __name__ == '__main__':
    n = int(input("Number of queries"))
    for query in range(n):
        email=input("Email address")
        series = input("TV Series").split(',')
        message = "\n"
        for i in series:
            a = GetMessage(i)
            print(a.get_imdb_url())
            message+="Tv series name: "+i+"\n"
            message+="Status: "+a.get_episode_date()+"\n"
            print(message)
            message+="\n"

        a = SendEmail(email,message)
        a.send()