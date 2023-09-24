# main.py
"""
title: Final Project Book Collection
author: Judy Zhu
date-created: 12/9/2022
"""
import csv
from flask import Flask, render_template, request, redirect

# --- GLOBAL VARIABLES --- #
FILENAME = "booklist.csv"

# --- FLASK --- #
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    home page, user adds book
    :return:
    """
    ALERT = ""
    HEADER, BOOKS = readFile(FILENAME) #get the header and the books
    if request.form: #user inputs in book; html: if name == value
        TITLE = request.form.get("title")
        AUTHOR = request.form.get("author")
        DESCRIPTION = request.form.get("description")
        TYPE = request.form.get("type")
        RATING = request.form.get("rating")
        COMMENTS = request.form.get("comments")
        DATE_ADDED = request.form.get("date_added")

        if checkContent(TITLE): #check if the book exists already
            createEntry(TITLE, AUTHOR, DESCRIPTION, TYPE, RATING, COMMENTS, DATE_ADDED)
            ALERT = "Successfully added this book!"
            return redirect('/')
        else:
            ALERT = "This book already exists"
    return render_template("index.html", alert=ALERT, books=BOOKS)


@app.route('/editbook/<id>', methods=['GET', 'POST'])
def editBook(id):
    """
    user edits book
    :param id: str
    :return:
    """
    EDITBOOK = [] #array for data of the book to be autofilled in the form
    with open(FILENAME, newline="") as FILE:
        READER = csv.reader(FILE)
        for ROW in READER:
            if ROW[0] == id:  # if the title of book matches
                EDITBOOK.append(ROW)

    if request.method == 'POST': #user presses submit
        ID = request.form.get("oldtitle") #gets the old title to replace
        NEWTITLE = request.form.get("newtitle") #gets data
        NEWAUTHOR = request.form.get("newauthor")
        NEWDESCRIPTION = request.form.get("newdescription")
        NEWTYPE = request.form.get("newtype")
        NEWRATING = request.form.get("newrating")
        NEWCOMMENTS = request.form.get("newcomments")
        NEWDATE_ADDED = request.form.get("newdate_added")
        NEWDATA = [] #will write back to the csv file
        with open(FILENAME, newline="") as FILE:
            READER = csv.reader(FILE)
            for ROW in READER:
                if ROW[0] != ID:  # if the title of book doesnt match
                    NEWDATA.append(ROW)  # append it to the array
                else:
                    ROW[0] = NEWTITLE #replace with new data
                    ROW[1] = NEWAUTHOR
                    ROW[2] = NEWDESCRIPTION
                    ROW[3] = NEWTYPE
                    ROW[4] = NEWRATING
                    ROW[5] = NEWCOMMENTS
                    ROW[6] = NEWDATE_ADDED
                    NEWDATA.append(ROW)

        with open(FILENAME, "w", newline="") as FILE:
            WRITER = csv.writer(FILE)  # write the data back
            for row in NEWDATA:
                WRITER.writerow(row) #write back to file
        return redirect('/')
    else:
        print(EDITBOOK)
        return render_template('editbook.html', editbook=EDITBOOK)





@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    function for user to search up books
    :return: ??i dont know what to put here ?? rnder_template
    """
    ALERTT = "" #if the search is not not valid
    global RESULTS
    if request.method == 'POST':
        QUERY = request.form['query']  # get what the user searched... HTML NEEDS TO BE name="query"
        if checkSearch(QUERY): #check if the searched book exists
            RESULTS = []  # 2d array fo the results
            with open(FILENAME, newline="") as FILE:
                READER = csv.reader(FILE)
                for ROW in READER:
                    if QUERY == ROW[0]:
                        RESULTS.append(ROW)  # if the seach entry matches
            ALERTT = ""
            return render_template('index.html', alert="", alertsearch=ALERTT, results=RESULTS)
        else:
            RESULTS = []
            ALERTT = "No book title match"

    return render_template('index.html', alertsearch=ALERTT, results=RESULTS)

@app.route('/delete/<id>')
def deleteBookEntry(id):
    """
    deletes the book that the user chooses
    :param id: str
    :return: redirect (?)
    """
    deleteBook(id)
    return redirect('/')





# --- CSV --- #
def readFile(FILENAME):
    '''
    opens out csv vile and reads the contents to an array. IF the file has not been created yet, create it
    :param FILENAME: csv file
    :return: HEADER, DATA: Our CSV header and the data
    '''

    try:
        with open(FILENAME, newline="") as FILE:
            READER = csv.reader(FILE)
            HEADER = next(READER)
            DATA = []
            for row in READER:
                DATA.append(row)
        return HEADER, DATA
    except:
        with open(FILENAME, "w", newline="") as FILE: #create new file
            WRITER = csv.writer(FILE)
            HEADER = ["Title", "Author", "Description", "Type", "Rating", "Comments", "Date Added"]
            WRITER.writerow(HEADER)
        return readFile(FILENAME)

def createEntry(TITLE, AUTHOR, DESCRIPTION, TYPE, RATING, COMMENTS, DATE_ADDED):
    """
    creates a book entry and adds it to our csv file using the data received from our flask application
    :param TITLE: str
    :param AUTHOR: str
    :param DESCRIPTION: str
    :param TYPE: str
    :param RATING: str
    :param COMMENTS: str
    :param DATE_ADDED:str
    :return: none
    """
    BOOK = [TITLE, AUTHOR, DESCRIPTION, TYPE, RATING, COMMENTS, DATE_ADDED]
    with open(FILENAME, "a", newline="") as FILE:
        WRITER = csv.writer(FILE)
        WRITER.writerow(BOOK)

def checkContent(BOOK):
    '''
    checks to see if the book exists in the CSV already
    :param BOOK: str
    :return: bool
    '''
    with open(FILENAME, newline="") as FILE:
        READER = csv.reader(FILE)
        for ROW in READER:
            if ROW[0] == BOOK:
                return False
        return True

def checkSearch(QUERY):
    '''
    checks to see if the query exists in the CSV
    :param QUERY: str
    :return: bool
    '''
    with open(FILENAME, newline="") as FILE:
        READER = csv.reader(FILE)
        for ROW in READER:
            if QUERY == ROW[0]:
                return True
        return False



def deleteBook(BOOK):
    """
    deletes a contact
    :param BOOK: str
    :return: none
    """
    NEW_DATA = []
    with open(FILENAME, newline="") as FILE:
        READER = csv.reader(FILE)
        for ROW in READER:
            if ROW[0] != BOOK:
                NEW_DATA.append(ROW)
    with open(FILENAME, "w", newline="") as FILE:
        WRITER = csv.writer(FILE)
        WRITER.writerows(NEW_DATA)

"""def editBook(ID, TITLE, AUTHOR, DESCRIPTION, TYPE, RATING, COMMENTS, DATE_ADDED):
    
    allows the user to edit their book entry
    :param ID: old title, id
    :param TITLE: str
    :param AUTHOR: str
    :param DESCRIPTION: str
    :param TYPE:
    :param RATING:
    :param COMMENTS:
    :param DATE_ADDED:
    :return:
    
    rows = []
    with open(FILENAME, newline="") as FILE:
        READER = csv.reader(FILE)
        for ROW in READER:
            if ROW[0] != ID: #if the title of book doesnt match
                rows.append(ROW) #replace it with new data
            else:
                ROW[0] = TITLE
                ROW[1] = AUTHOR
                ROW[2] = DESCRIPTION
                ROW[3] = TYPE
                ROW[4] = RATING
                ROW[5] = COMMENTS
                ROW[6] = DATE_ADDED
                print(ROW)
                rows.append(ROW)
    with open(FILENAME, "w", newline="") as FILE:
        WRITER = csv.writer(FILE) #write the data back
        for row in rows:
            WRITER.writerow(row)


def getData(TITLE):
    with open(FILENAME, newline="") as FILE:
        READER = csv.reader(FILE)
        for ROW in READER:
            if ROW[0] == TITLE:
                print(ROW)
                return ROW
            else:
                break
"""


# --- MAIN PROGRAM CODE --- #
if __name__ == "__main__":
    app.run(debug=True)