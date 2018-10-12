import pymysql

class Database:
    """
    A class to write data to the SQL table.

    Table Name : 'Entries'
    Table Structure :
        +-------+------- +
        | email | series |
        +-------+--------+

    Args:
        user (str): Username of MySQL server.
        password (str): Password of MySQL server.
        db (str): Database name.

    """
    def __init__(self,user,password,db):
        self.user = user
        self.password = password
        self.db = db
        self.connection = None

    def connect(self):
        #Method to connect to Database.
        self.connection = pymysql.connect(host='localhost',
                                 user=self.user,
                                 password=self.password,
                                 db=self.db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    def write(self,email,series):
        """
        Method to write the data to MySQL database connected.

        Args:
            email (str): email address of user.
            series (list): list of tv series queried by user.
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `Entries` (`email`, `series`) VALUES (%s, %s)"
                for tv_series in series:
                    cursor.execute(sql, (email, tv_series.strip()))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()

    def read(self,email):
        """
        Method to read the data from the table in MySQL database.

        Args:
            email (str): email id of the user
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                # Read all the records of an email address.
                sql = "SELECT `email`, `series` FROM `Entries` WHERE `email`=%s"
                cursor.execute(sql, ('abhi98khandelwal@gmail.com',))
                result = cursor.fetchall()
                print(result)
        finally:
            self.connection.close()