import psycopg2

def create_db_connection():
    connection,cursor=None,None
    try:
        connection = psycopg2.connect(user = "lithint",
                                      password = "postgres",
                                      host = "127.0.0.1",
                                      port = "5433",
                                      database = "demo_db")
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        # cursor.execute("SELECT version();")
        # record = cursor.fetchone()
        print("You are connected to - \n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    return connection,cursor


def close_db_connection(connection=None,cursor=None):
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
