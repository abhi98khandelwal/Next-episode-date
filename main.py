from get_message import GetMessage
from send_email import SendEmail
from database import Database

if __name__ == '__main__':
    # Define variables to connect to MySQL database
    user = 'root' # Set username of MySQL server
    password = '' # Set password of MySQL server
    d = Database(user, password)

    n = int(input("Number of queries"))
    for query in range(n):
        email=input("Email address")
        series = input("TV Series").split(',')
        message = "\n"
        #Create an object for Database class
        #Connect to database and insert the data in the table.
        d.write(email,series)
        for i in series:
            #Create an object for GetMessage class which can determine the next episode date of the TV Series.
            m = GetMessage(i)
            #print(a.get_imdb_url())
            message+="Tv series name: "+i+"\n"
            message+="Status: "+m.get_episode_date()+"\n"
            #print(message)
            message+="\n"

        #Send the result to user's email
        e = SendEmail(email,message)
        e.send()