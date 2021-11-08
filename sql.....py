import sqlite3

conn = sqlite3.connect("birddex.db")

refresh = True
add = True
""" Here, conn is the database object and 'databasename.db' is the actual database we're trying to connect with. 
If there is no database available then the same command will trigger 
to create a new database of the same name in our current directory."""

curr = conn.cursor() #Here 'curr' is our new cursor object.

# SQL command that creates a table in the database

if refresh == True:
    createTableCommand = """ CREATE TABLE Markers (
    indexx VARCHAR(33),
    lat FLOAT(53),
    lon FLOAT(53),
    bird VARCHAR(50)
    );"""

    # Executing the SQL command
    curr.execute(createTableCommand)

    # Commit the changes
    conn.commit()

curr = conn.cursor()
if add == True:
    # The 2D array containing required data
    data = [[574097271543845914851462667672505, 57.40972715438459, 14.851462667672505, "penis 0"],
            [564097271543845915851462667672505, 56.40972715438459, 15.851462667672505, "penis 1"],
            ]

    # A for loop to iterate through the data and add them one by one.
    for i in data:
        addData = f"""INSERT INTO Markers VALUES('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}')"""
        print(addData)  # To see all the commands iterating
        curr.execute(addData)
    print("Data added successfully!")

    conn.commit()

# Our search query that extracts all data from the NSA_DATA table.
fetchData = "SELECT bird from Markers WHERE indexx=1"

# Notice that the next line of code doesn't output anything upon execution.
curr.execute(fetchData)

# We use fetchall() method to store all our data in the 'answer' variable
answer = curr.fetchall()

# We print the data
for data in answer:
    print(data)