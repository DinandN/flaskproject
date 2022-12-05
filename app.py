# ======= Imports =======
# Packages
import re
from flask import Flask, request, render_template, redirect
# Local
from py.functions import *

# ========= Declaring Variables =========
# Config and Logins
app = Flask(__name__)
DBlogin_data = GetDBLoginFromConfig()
conn = ConnectingToDB(DBlogin_data)
# Database cursor
mycursor = conn.cursor()

# ========= Start of Code =========
print("Starting Flask Server")
CreatingTable(mycursor)


# post function
@app.route('/', methods=["GET", "POST"])
def GetInfoFromPost():
    if request.method == "POST":
        # fail safe if no data is entered
        if (request.form.get("form_FirstName") != "") & (request.form.get("form_Surname") != ""):
            # getting the data from the post
            firstName = request.form.get("form_FirstName")
            lastName = request.form.get("form_Surname")
            Present = request.form.get("form_Present")
            # converting the "Present" data to a boolean
            if Present == "on":
                Present = True
            elif Present is None:
                Present = False

            # Inputting the data into the database
            sql = "INSERT INTO studentengegevens (Naam, Achternaam, Presentie) VALUES (%s, %s, %s)"
            val = (firstName, lastName, Present)
            mycursor.execute(sql, val)
            conn.commit()

    # Getting all data from database to make a table
    mycursor.execute("SELECT * FROM studentengegevens")
    data = mycursor.fetchall()
    return render_template("index.html", db_data=data)

# delete function


@app.route('/delete', methods=["GET"])
def DeleteStudent():
    # getting the ID from the URL
    ID = request.args.get("deletenumber")
    # Returning to the main page url
    # SQL statement to delete a student
    sql = f"DELETE FROM  studentengegevens WHERE StudentID = {ID}"
    mycursor.execute(sql)
    conn.commit()
    return redirect("/", code=302)

# update function


@app.route('/update', methods=["GET", "POST"])
def UpdateStudent():
    # get id from database
    ID = request.args.get("updatenumber")
    if request.method == "GET":
        # redirect to update page
        return render_template('/update.html')
    # get data from update page
    if request.method == "POST":
        firstName = request.form.get("form_FirstNameUpdate")
        lastName = request.form.get("form_SurnameUpdate")
        Present = request.form.get("form_PresentUpdate")
        # convert boolean
        if Present == "on":
            Present = True
        elif Present is None:
            Present = False
        # sql statement to update student
        sql = f"UPDATE studentengegevens SET Naam = %s, Achternaam = %s, Presentie = %s WHERE StudentID = %s"
        val = (firstName, lastName, Present, ID)
        mycursor.execute(sql, val)
        conn.commit()
        # return to home page
        return redirect('/', code=302)


# starting the python application
if __name__ == "__main__":
    app.run(debug=True)
