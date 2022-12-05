from configparser import ConfigParser
import mysql.connector


# ======= Functions =======
def ProgramQuit():
    input("Press enter to quit")
    quit()

def GetDBLoginFromConfig():

    # ===== Declaring Variables
    configparser = ConfigParser(interpolation=None)
    FileName = "DBConfig.ini"
    KeyName = "database"
    FileSetup = "; Login for the database\n[database]\n\nhost =\nuser =\npassword =\ndatabase =\n"
    login_data = []
    # ==== Start Function ====
    try:
        configparser.read(FileName)
        login_data.append(configparser.get("database", "host"))
        login_data.append(configparser.get("database", "user"))
        login_data.append(configparser.get("database", "password"))
        login_data.append(configparser.get("database", "database"))
        return login_data
    except Exception as e:
        print(f"Exception configparser: {e}")
        if str(e) == f"No section: '{KeyName}'":
            print("Error: Config file not found, creating new file...")
            with open(FileName, "w") as f:
                f.write(FileSetup)
            print("Done! Please fill in the config file and restart the program.")
            ProgramQuit()

# ============== Declaring Variables ================
    conn = None
    # ============== Start Function ================
    # Connect to the database
    try:
        conn = mysql.connector.connect(host=login_data[0], user=login_data[1], password=login_data[2],
                                       database=login_data[3])
        print("Verbinding met de database is gelukt!")
    # except if access denied
    except mysql.connector.Error as err:
        print(err.errno)
        if err.errno == 1045:
            print(
                "De inloggegevens zijn niet correct!\n\nVerander het bestand 'database-config.ini' en vul de juiste gegevens in.")
            ProgramQuit()
        elif err.errno == 1044:
            print("De database bestaat niet!")
            ProgramQuit()
        elif err.errno == 2003:
            print("De host is niet gevonden!")
            ProgramQuit()
        elif str(err) == "Character set 'utf8' unsupported":
            print("Please change the database to utf8mb4 or use mysql-connector-python 8.0.29")
            ProgramQuit()
        else:
            print(err)
            ProgramQuit()
    return conn

def ConnectingToDB(login_data):
    # ============== Declaring Variables ================
    conn = None
    # ============== Start Function ================
    # Connect to the database
    try:
        conn = mysql.connector.connect(host=login_data[0], user=login_data[1], password=login_data[2],
                                       database=login_data[3])
        print("Verbinding met de database is gelukt!")
    # except if access denied
    except mysql.connector.Error as err:
        print(err.errno)
        if err.errno == 1045:
            print(
                "De inloggegevens zijn niet correct!\n\nVerander het bestand 'database-config.ini' en vul de juiste gegevens in.")
            ProgramQuit()
        elif err.errno == 1044:
            print("De database bestaat niet!")
            ProgramQuit()
        elif err.errno == 2003:
            print("De host is niet gevonden!")
            ProgramQuit()
        elif str(err) == "Character set 'utf8' unsupported":
            print("Please change the database to utf8mb4 or use mysql-connector-python 8.0.29")
            ProgramQuit()
        else:
            print(err)
            ProgramQuit()
    # Return the connection
    return conn

def CreatingTable(mycursor):
    # ============== Declaring Variables ================
    TableName = "studentengegevens"
    # ============== Start Function ================
    try:
        mycursor.execute(
            f"CREATE TABLE {TableName} (StudentID INT(5) AUTO_INCREMENT PRIMARY KEY, Naam VARCHAR(70), Achternaam VARCHAR(70), Presentie TINYINT(1))")
    except mysql.connector.Error as err:
        if err.errno == 1050:
            print("De database bestaat al! voor de rest niks aan de hand!")