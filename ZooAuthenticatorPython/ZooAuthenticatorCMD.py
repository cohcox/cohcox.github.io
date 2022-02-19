"""
    Enhancements to IT-145 Zoo Authenticator for CS-499
    Cody Cox
    02/19/2022
    CS-499
    Southern New Hampshire University
"""

"""
    This application is to be used by a zoo in order to maintain security to sensitive data that should only be available to the necessary job description.
    The end goal will be to wrap this in a nice GUI that shows well, though currently the focus is on functionality. 
    It uses a database to secure access to the CSV files for each job, in the coming days the ability to create and delete entries into each file will be made.

    NOTE = Passwords for users are as follows: admin1 - 123, admin2 - 321, keeper1 - 456, keeper2 - 654, vet1 - 789, vet2 - 987
"""

# Initial imports to project
import csv, time
from pprint import pprint
from getpass import getpass
from pymongo import MongoClient, client_options, cursor

# Set up database through MonogDB where records are stored
client = MongoClient('localhost', 27017)
db = client.zoodatabase

# Main function to initialize program 
def main():
    
    # Open users.csv in order to read from usernames and passwords, so that access may be restricted to information
    with open("users.csv", "r") as file:
        file_reader = csv.reader(file)
        user_find(file_reader)
        file.close()

        # After sign in actions are done and data recorded, as if another account would like to sign in
        access = input("Would you like to sign into another account? (y/n)")
        if access == "y":
            main()
        else:
            print("Goodbye!!")

# Function to check for user name in file
def user_find(file):
    
    # Recieve user input for username
    user = input("Enter username: ")
    
    # Set up variables for checking which user is logging on
    keeper = "keeper"
    admin = "admin"
    vet = "vet"
    
    for row in file:

        # Checks if username matches up with existing users file
        if row[0] == user:
            user_found = [row[0],row[1]]
            
            # Checks if password lines up with username entered
            password_check(user_found)

            # If all true, prints data from mongodb pertaining to each job from collections and csv files in zoodatabase
            # Grants access to veterinarian data
            if vet in user:
                cursor = db['veterinarian'].find({},{'_id':0}).sort('name')
                print("Confirmed 'Veterinarian', would you like to display all data, sort data by category, search by animal name, or insert/delete records of an animal? (all/sort/search/insert/delete)")
                answer = input(": ")

                # Displays all data, sorted by name
                if answer == "all":
                    for document in cursor:
                        pprint(document)

                # Displays all data, sorted by users choosing
                if answer == "sort":
                    print("How would you like your data sorted? (name, gender, age, medication)")
                    searchInput = input(": ")

                    if searchInput == 'name':
                        cursor = db['veterinarian'].find({},{'_id':0}).sort('name')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'gender':
                        cursor = db['veterinarian'].find({},{'_id':0}).sort('gender')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'age':
                        cursor = db['veterinarian'].find({},{'_id':0}).sort('age')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'medication':
                        cursor = db['veterinarian'].find({},{'_id':0}).sort('medication')
                        for document in cursor:
                            pprint(document)

                # Search by animal name
                if answer == "search":
                    searchByNameVet()

                # Invokes exterior functions for insertion and deletion of records
                if answer == "insert":
                    veterinarianCreate()
                    time.sleep(0.1)
                    for document in cursor:
                        pprint(document)
                if answer == "delete":
                    veterinarianDelete()
                    time.sleep(0.1)
                    for document in cursor:
                        pprint(document)

            # Grants access to zookeeper data
            if keeper in user:
                myDB = db['zookeeper']
                cursor = myDB.find({},{'_id':0}).sort('name')
                
                print("Confirmed 'Zoo Keeper', would you like to display all data, sort data by category, search by animal name or insert/delete records of an animal? (all/sort/search/insert/delete)")
                answer = input(": ")

                # Displays list for records of all animals by name(this is by default)
                if answer == "all":
                    for document in cursor:
                        pprint(document)

                # Displays animal records by category of users choosing
                if answer == "sort":
                    print("How would you like your data sorted? (species, name, habitat, gender)")
                    searchInput = input(": ")

                    if searchInput == 'species':
                        cursor = myDB.find({},{'_id':0}).sort('species')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'name':
                        cursor = myDB.find({},{'_id':0}).sort('name')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'habitat':
                        cursor = myDB.find({},{'_id':0}).sort('habitat')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'gender':
                        cursor = myDB.find({},{'_id':0}).sort('gender')
                        for document in cursor:
                            pprint(document)

                # Search by animal name
                if answer == "search":
                    searchByNameKeeper

                # Invokes exterior functions for insertion and deletion of records
                if answer == "insert":
                    zookeeperCreate()
                    time.sleep(0.1)
                    for document in cursor:
                        pprint(document)
                if answer == "delete":
                    zookeeperDelete()
                    time.sleep(0.1)
                    for document in cursor:
                        pprint(document)

            # Grants access to veterinarin data
            if admin in user:
                myCollection = "administrative"
                cursor = db['administrative'].find({},{'_id':0}).sort('name')
                print("Confirmed 'Administrator', would you like to display all data, sort data by category, search by name, or insert/delete records of an employee? (all/sort/search/insert/delete)")
                answer = input(": ")
                
                # Displays list for records of all employees by name(this is by default)
                if answer == "all":
                    for document in cursor:
                        pprint(document)

                # Displays employee records by category of users choosing
                if answer == "sort":
                    print("How would you like your data sorted? (username, name, PTO days, gender)")
                    searchInput = input(": ")

                    if searchInput == 'username':
                        cursor = db['administrative'].find({},{'_id':0}).sort('username')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'name':
                        cursor = db['administrative'].find({},{'_id':0}).sort('name')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'PTO days':
                        cursor = db['administrative'].find({},{'_id':0}).sort('PTO days')
                        for document in cursor:
                            pprint(document)
                    if searchInput == 'gender':
                        cursor = db['administrative'].find({},{'_id':0}).sort('gender')
                        for document in cursor:
                            pprint(document)

                # Searches by name
                if answer == "search":
                    searchByNameAdmin()
                
                # Invokes exterior functions for insertion and deletion of records
                if answer == "insert":
                    adminCreate()
                    time.sleep(0.1)
                    for document in cursor:
                        pprint(document)

                if answer == "delete":
                    adminDelete()
                    time.sleep(0.1)
                    for document in cursor:
                        pprint(document)
            break
           
# Checks for password and if it matches up with username
def password_check(user_found):
    
    time.sleep(0.1)
    # Use getpass module to safely input password
    user = getpass("Enter Password: ")
    
    # Searches users.csv for password in index 1 and checks if match with index 0(username) in row, if so confirm password match
    if user_found[1] == user:
        print("Password correct!")
    
    # If password does not line up with username, ask to try again  
    if user_found[1] != user:
        answer = input("Password incorrect, try again?(y/n)")
        if answer == "y":
            main()
        if answer == "n":
            print("Goodbye")
            quit()


# This begins block of code containing methods for insertion, deletion, and searching by name for each job
# Method for zookeeper to add an animal through MongoDB
def veterinarianCreate():
    myDB = db['veterinarian']

    # Input variables
    species = input("What is the animal's species? : ")
    name = input("What is the animal's name? : ")
    age = input("What is the animal's age? : ")
    gender = input("What is the animal's gender? : ")
    medication = input("Is the animal on any medication? : ")

    # Uses input variables to create the dictionary for insertion into database records
    mydict = {"species" : species, "name" : name, "age" : age, "gender" : gender, "medication" : medication}
    myDB.insert_one(mydict)
    print("Successfuilly inserted " + species + "" + name + " into the zoo database.")

# Method for zookeeper to delete an animal through MongoDB
def veterinarianDelete():
    myDB = db['veterinarian']

    delete = input("What is the name of the animal who's data you would like to delete? : ")

    deleteQuery = { "name" : delete}
    myDB.delete_one(deleteQuery)
    print("Confirmed deltetion of " + delete + " from the database")

# Method for zookeeper to add an animal through MongoDB
def zookeeperCreate():
    myDB = db['zookeeper']

    # Input variables
    species = input("What is the animal's species? : ")
    name = input("What is the animal's name? : ")
    age = input("What is the animal's age? : ")
    gender = input("What is the animal's gender? : ")
    habitat = input("What habitat will the animal live in? : ")
    food = input("What type of food does this animal eat? : ")
    feedings = input("How many feedings per day is necessary? : ")

    # Uses input variables to create the dictionary for insertion into database records
    mydict = {"species" : species, "name" : name, "age" : age, "gender" : gender, "habitat" : habitat, "food type" : food, "feedings" : feedings}
    myDB.insert_one(mydict)
    print("Successfuilly inserted " + species + "" + name + " into the zoo database.")

# Method for zookeeper to delete an animal through MongoDB
def zookeeperDelete():
    myDB = db['zookeeper']

    delete = input("What is the name of the animal who's data you would like to delete? : ")

    deleteQuery = { "name" : delete}
    myDB.delete_one(deleteQuery)
    print("Confirmed deltetion of " + delete + " from the database")

# Method for administrator to create an employee through MongoDB
def adminCreate():
    myDB = db['adminastrative']

    # Input variables
    userName = input("What is the employee's desired username? : ")
    name = input("What is the employee's name? : ")
    gender = input("What is the employee's gender? : ")
    ptoDays = input("How many PTO days will the employee have? : ")
    insurance = input("What type of insurance will the employee have? (Family, Single, N/A) : ")

    # Uses input variables to create the dictionary for insertion into database records
    mydict = {"username" : userName, "name" : name, "gender" : gender, "PTO days" : ptoDays, "insurance" : insurance}
    myDB.insert_one(mydict)
    print("Successfuilly inserted " + name + " into the employee database.")


# Method for administrator to delete an employee through MongoDB
def adminDelete():
    myDB = db['adminastrative']

    delete = input("What is the name of the employee who's data you would like to delete? : ")

    deleteQuery = { "name" : delete}

    myDB.delete_one(deleteQuery)
    print("Confirmed deltetion of " + delete + " from the database")

# Searching algorithms for each job, by name
def searchByNameAdmin():
    myDB = db["administrative"]

    name = input("What is the name that you would like to display records for? : ")

    foundName = myDB.find_one({"name" : name})
    pprint(foundName)

def searchByNameKeeper():
    myDB = db["zookeeper"]

    name = input("What is the name that you would like to display records for? : ")

    foundName = myDB.find_one({"name" : name})
    pprint(foundName)

def searchByNameVet():
    myDB = db["veterinarian"]

    name = input("What is the name that you would like to display records for? : ")

    foundName = myDB.find_one({"name" : name})
    pprint(foundName)
    
            
# Runs the main function to start program
main()