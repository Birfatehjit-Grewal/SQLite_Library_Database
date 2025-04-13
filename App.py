import sqlite3
from datetime import date
from random import choice

def findItemsByName(cursor, name):

    query = 'SELECT Title, ItemID, Type, Availablity, OnOrder FROM Item WHERE Title LIKE :name;'
    cursor.execute(query, {"name": '%'+name+'%'})
    return cursor.fetchall()

def borrowItemByID(cursor, ItemID, UserID):

	# Check if available

	query = 'SELECT I.Availablity FROM Item I WHERE I.ItemID = :ItemID;'
	cursor.execute(query, {"ItemID": ItemID})
	avail = cursor.fetchone()

	# Throw error if wrong ID

	if(avail == 0):
                print("Item not found")
                raise Exception("ItemID not found")

	# Throw error if unavailable

	if(int(avail[0]) == 0):
                print("Item unavailable")
                raise Exception("Item unavailable") 

	# If user is allowed to borrow, add to borrowings table 

	if(getUserOwes(cursor, UserID) > 0):
                print("Please pay the outstanding late fees before borrowing")
                raise Exception("Outstanding late fees")

	query = "INSERT INTO Borrowing(UserID, ItemID, BorrowDate, DueDate) VALUES(:UserID, :ItemID, DATE(), DATE(DATE(), '+14 days'));"

	cursor.execute(query, {"UserID": UserID, "ItemID": ItemID})

	# Change availability

	query = 'UPDATE Item SET Availablity = FALSE WHERE ItemID =  :ItemID;'

	cursor.execute(query, {"ItemID": ItemID})

def returnItemByID(cursor, ItemID):

	updateCharges(cursor)

	# Check availablity

	query = 'SELECT I.Availablity FROM Item I WHERE I.ItemID = :ItemID;'
	cursor.execute(query, {"ItemID": ItemID})
	avail = cursor.fetchone()

	# Throw error if wrong ID

	if(len(avail) == 0):
                print("Item not found")
                raise Exception("ItemID not found")

	# Throw error if ItemID never borrowed

	if(int(avail[0]) == 1):
                print("This Item was not borrowed")
                raise Exception("Item still available")

	# Add return date to relevant borrowing

	query = """UPDATE Borrowing
				SET ReturnDate = DATE() 
				WHERE BorrowDate IN (
					SELECT MAX(BorrowDate) 
					FROM Borrowing 
					WHERE ItemID = :ItemID 
					GROUP BY ItemID) 
				AND ItemID = :ItemID;
				"""

	cursor.execute(query, {"ItemID": ItemID})	

def payBalance(cursor, UserID):

	# Pay off balance on all Borrowing charges of User
	cursor.execute('UPDATE Borrowing SET Charge = 0 WHERE UserID = :UserID AND ReturnDate <> '0000-00-00';', {"UserID": UserID})

def getUserOwes(cursor, UserID):

	updateCharges(cursor)

	# Sum all charges of given user, return
	query = 'SELECT SUM(B.Charge) FROM Borrowing B WHERE B.UserID = :UserID GROUP BY UserID;'
	res = cursor.execute(query, {"UserID": UserID}).fetchone()

	# Return if > 0, else return 0
	if(res): 
		return res[0]
	else: 
		return 0

def donateItem(cursor):
	print("What is your item's type?\nSelect one:")
	print("[1] Book")
	print("[2] Magazine")
	print("[3] Journal")
	print("[4] CD")
	print("[5] Record")
	print("[6] Audio Book")
	print("[7] Go back")

	typeChoice = int(input("Input number [1-7]: "))

	while(True):
		try:
			match typeChoice:
				case 1:
					return donateBook(cursor)
				case 2:
					return donateMagazine(cursor)
				case 3:
					return donateJournal(cursor)
				case 4:
					return donateCD(cursor)
				case 5:
					return donateRecord(cursor)
				case 6:
					return donateAudioBook(cursor)
				case 7:
					return
				case _:
					print("Invalid choice. Try again")
					continue
		except:
			print("Invalid entry, try again")
			continue

def donateBook(cursor):
	
	# Get new item ID

	query1 = """SELECT MAX(ItemID)
				FROM Item
				"""

	newID = cursor.execute(query1).fetchone()[0] + 1

	Title = input("Book Title:")
	Author = input("Book Author:")
	PubDate = input("Publication date (YYYY-MM-DD):")
	Length = input("Length in pages:")
	ISBN = input("ISBN (serial number):")
	Publisher = input("Publisher:")
	Genre = input("Genre (10 Chars):")

	# Add book to item table

	query2 = """INSERT INTO Book 
				VALUES(:newID, :Title, :Author, :PubDate, :Length, :ISBN, :Publisher, NULL, :Genre);
				"""

	cursor.execute(query2, {
		"newID": newID, 
		"Title": Title, 
		"Author": Author, 
		"PubDate": PubDate, 
		"Length": Length, 
		"ISBN": ISBN, 
		"Publisher": Publisher, 
		"Genre": Genre
	})

	return newID

def donateOnlineBook(cursor):

    # Get new item ID

    query1 = """SELECT MAX(ItemID)
                FROM Item
                """

    newID = cursor.execute(query1).fetchone()[0] + 1

    Title = input("Book Title:")
    Author = input("Book Author:")
    Link = input("Book Link (URL starting with 'https://'):")
    PubDate = input("Publication date (YYYY-MM-DD):")
    Publisher = input("Publisher:")
    ISBN = input("ISBN (serial number):")
    Format = input("Format (e.g., PDF):")
    Length = input("Length in pages:")
    Genre = input("Genre (10 Chars):")

    # Add online book to item table

    query2 = """INSERT INTO OnlineBooks
                VALUES(:newID, :Title, :Author, :Link, :PubDate, :Publisher, :ISBN, :Format, :Length, :Genre);
                """

    cursor.execute(query2, {
        "newID": newID,
        "Title": Title,
        "Author": Author,
        "Link": Link,
        "PubDate": PubDate,
        "Publisher": Publisher,
        "ISBN": ISBN,
        "Format": Format,
        "Length": Length,
        "Genre": Genre
    })

    return newID

def donateMagazine(cursor):

    # Get new item ID

    query1 = """SELECT MAX(ItemID)
                FROM Item
                """

    newID = cursor.execute(query1).fetchone()[0] + 1

    Title = input("Magazine Title:")
    Publisher = input("Publisher:")
    PubDate = input("Publication date (YYYY-MM-DD):")
    IssueNum = input("Issue Number:")
    ISBN = input("ISBN (serial number):")
    Length = input("Length in pages:")

    # Add magazine to item table

    query2 = """INSERT INTO Magazine
                VALUES(:newID, :Title, :Publisher, :PubDate, :IssueNum, :ISBN, :Length, NULL);
                """

    cursor.execute(query2, {
        "newID": newID,
        "Title": Title,
        "Publisher": Publisher,
        "PubDate": PubDate,
        "IssueNum": IssueNum,
        "ISBN": ISBN,
        "Length": Length
    })

    return newID

def donateJournal(cursor):

    # Get new item ID

    query1 = """SELECT MAX(ItemID)
                FROM Item
                """

    newID = cursor.execute(query1).fetchone()[0] + 1

    Title = input("Journal Title:")
    Volume = input("Volume:")
    Issue = input("Issue:")
    Publisher = input("Publisher:")
    PubDate = input("Publication date (YYYY-MM-DD):")
    Field = input("Field of publication:")

    # Add journal to item table

    query2 = """INSERT INTO Journal
                VALUES(:newID, :Title, :Volume, :Issue, :Publisher, :PubDate, :Field, NULL);
                """

    cursor.execute(query2, {
        "newID": newID,
        "Title": Title,
        "Volume": Volume,
        "Issue": Issue,
        "Publisher": Publisher,
        "PubDate": PubDate,
        "Field": Field
    })

    return newID

def donateCD(cursor):

    # Get new item ID

    query1 = """SELECT MAX(ItemID)
                FROM Item
                """

    newID = cursor.execute(query1).fetchone()[0] + 1

    Title = input("CD Title:")
    Artist = input("Artist:")
    RecordLabel = input("Record Label:")
    ReleaseDate = input("Release date (YYYY-MM-DD):")

    # Add CD to item table

    query2 = """INSERT INTO CD
                VALUES(:newID, :Title, :Artist, :RecordLabel, :ReleaseDate, NULL);
                """

    cursor.execute(query2, {
        "newID": newID,
        "Title": Title,
        "Artist": Artist,
        "RecordLabel": RecordLabel,
        "ReleaseDate": ReleaseDate
    })

    return newID

def donateRecord(cursor):

    # Get new item ID

    query1 = """SELECT MAX(ItemID)
                FROM Item
                """

    newID = cursor.execute(query1).fetchone()[0] + 1

    Title = input("Record Title:")
    Location = input("Location (e.g., LOCAL):")
    Date = input("Date (YYYY-MM-DD):")
    Category = input("Category (e.g., GENERAL):")
    ShelfID = input("Shelf ID:")

    # Add record to item table

    query2 = """INSERT INTO Record
                VALUES(:newID, :Title, :Location, :Date, :Category, NULL);
                """

    cursor.execute(query2, {
        "newID": newID,
        "Title": Title,
        "Location": Location,
        "Date": Date,
        "Category": Category
    })

    return newID

def donateAudioBook(cursor):

    # Get new item ID

    query1 = """SELECT MAX(ItemID)
                FROM Item
                """

    newID = cursor.execute(query1).fetchone()[0] + 1

    Title = input("AudioBook Title:")
    Author = input("AudioBook Author:")
    PubDate = input("Publication date (YYYY-MM-DD):")
    Publisher = input("Publisher:")
    ISBN = input("ISBN (serial number):")
    Length = input("Length in minutes:")

    # Add audiobook to item table

    query2 = """INSERT INTO AudioBook
                VALUES(:newID, :Title, :Author, :PubDate, :Publisher, :ISBN, :Length);
                """

    cursor.execute(query2, {
        "newID": newID,
        "Title": Title,
        "Author": Author,
        "PubDate": PubDate,
        "Publisher": Publisher,
        "ISBN": ISBN,
        "Length": Length
    })

    return newID

def shelfItem(cursor, ItemID, ShelfID):

	# Check that item is shelvable
	query1 = """SELECT Type
				FROM Item
				WHERE ItemID = :ItemID
				"""
	res = cursor.execute(query1, {"ItemID": ItemID}).fetchone()[0]

	if((res in ('BOOK', 'MAGAZINE', 'CD', 'RECORD', 'JOURNAL')) == False):
		raise Exception("Invalid Item type")

	match res:
		case "BOOK":
			setBookShelfID(cursor, ShelfID, ItemID)
		case "MAGAZINE":
			setMagazineShelfID(cursor, ShelfID, ItemID)
		case "CD":
			setCDShelfID(cursor, ShelfID, ItemID)
		case "RECORD":
			setRecordShelfID(cursor, ShelfID, ItemID)
		case "JOURNAL":
			setJournalShelfID(cursor, ShelfID, ItemID)

def setBookShelfID(cursor, newShelfID, ItemID):
    cursor.execute("UPDATE Book SET ShelfID = :newShelfID WHERE ItemID = :ItemID", {"newShelfID": newShelfID, "ItemID": ItemID})

def setMagazineShelfID(cursor, newShelfID, ItemID):
    cursor.execute("UPDATE Magazine SET ShelfID = :newShelfID WHERE ItemID = :ItemID", {"newShelfID": newShelfID, "ItemID": ItemID})

def setJournalShelfID(cursor, newShelfID, ItemID):
    cursor.execute("UPDATE Journal SET ShelfID = :newShelfID WHERE ItemID = :ItemID", {"newShelfID": newShelfID, "ItemID": ItemID})

def setCDShelfID(cursor, newShelfID, ItemID):
    cursor.execute("UPDATE CD SET ShelfID = :newShelfID WHERE ItemID = :ItemID", {"newShelfID": newShelfID, "ItemID": ItemID})

def setRecordShelfID(cursor, newShelfID, ItemID):
    cursor.execute("UPDATE Record SET ShelfID = :newShelfID WHERE ItemID = :ItemID", {"newShelfID": newShelfID, "ItemID": ItemID})

def findevent(cursor):
        print("Search for Event by:")
        print("[1] Name")
        print("[2] Date")
        print("[3] Type")
        print("[4] Go back")
        typeChoice = int(input("Input number [1-4]: "))
        Date = date.today()
        Loop1 = True
        while(Loop1):
                match typeChoice:
                        case 1:
                                Name = input("Enter Event Name: ")
                                Name = '%' + Name + '%'
                                query = 'SELECT * FROM EVENT WHERE EventName lIKE :Name AND EventDate > :Date'
                                cursor.execute(query,{"Name":Name,"Date":Date})
                                rows=cursor.fetchall()
                                print("After Fetch")
                                for row in rows:
                                        print("EventName: " + row[0] + ", Event Date: " + row[1] + " Type: "+row[2]+"\n")
                                Loop1 = False
                        case 2:
                                SearchDate = input("Enter Event Date (YYYY-MM-DD): ")
                                query = 'SELECT EventName, EventDate, Type FROM Event WHERE EventDate > :SearchDate AND EventDate > :Date ORDER BY EventDate;'
                                cursor.execute(query,{"SearchDate":SearchDate,"Date":Date})
                                rows=cursor.fetchall()
                                for row in rows:
                                        print("EventName: " + row[0] + ", Event Date: " + row[1] + " Type: "+row[2]+"\n")
                                Loop1 = False
                        case 3:
                                print("Select Event Type:")
                                print("[1] BOOK EVENT")
                                print("[2] BOOK CLUB")
                                print("[3] CLUB")
                                print("[4] ART SHOW")
                                print("[5] FILM SCREENING")
                                print("[6] READING")
                                print("[7] LECTURE")
                                print("[7] MEET AND GREET")
                                Loop2 = True
                                while(Loop2):
                                        typechoice1 = int(input("Input number [1-7]: "))
                                        match typechoice1:
                                                case 1:
                                                        eventType = 'BOOK EVENT'
                                                        Loop2 = False
                                                case 2:
                                                        eventType = 'BOOK CLUB'
                                                        Loop2 = False
                                                case 3:
                                                        eventType = 'CLUB'
                                                        Loop2 = False
                                                case 4:
                                                        eventType = 'ART SHOW'
                                                        Loop2 = False
                                                case 5:
                                                        eventType = 'FILM SCREENING'
                                                        Loop2 = False
                                                case 6:
                                                        eventType = 'READING'
                                                        Loop2 = False
                                                case 7:
                                                        eventType = 'LECTURE'
                                                        Loop2 = False
                                                case 8:
                                                        eventType = 'MEET AND GREET'
                                                        Loop2 = False
                                                case _:
                                                        print("Invalid choice. Try again\n")
                                query = 'SELECT EventName, EventDate FROM Event WHERE Type = :eventType;'
                                cursor.execute(query,{"eventType":eventType,"Date":Date})
                                rows=cursor.fetchall()
                                for row in rows:
                                        print("EventName: " + row[0] + ", Event Date: " + row[1] +"\n")
                                Loop1 = False
                        case _:
                                print("Invalid choice. Try again\n")

def eventRegister(cursor,UserID):
        Loop1 = True
        Date = date.today()
        while(Loop1):
                Name = input("Event Name: ")
                eventDate = input("Event Date (YYYY-MM-DD): ")
                query = 'SELECT COUNT(*) FROM Event WHERE EventName = :Name AND EventDate = :eventDate;'
                cursor.execute(query,{"Name":Name,"eventDate":eventDate,"Date":Date})
                count = cursor.fetchone()
                if(count[0] == 1):
                        query = 'INSERT INTO Registered VALUES(:UserID,:Date,:Name);'
                        cursor.execute(query,{"UserID":UserID,"Date":eventDate,"Name":Name})
                        Loop1 = False
                elif(count[0]> 1):
                        print("Input does not return an unique event Please try again")
                else:
                        print("No Such Event exists")
                        Loop1 = False
        
def addUser(cursor, nameF, nameL, address=None, email=None, prefType=None):

	# Find largest userID, add 1 for new userID

	query1 = """SELECT MAX(UserID)
				FROM User;"""

	newID = cursor.execute(query1).fetchone()[0] + 1

	# Make query, attempt to insert. Return false if a check has failed

	query2 = """INSERT INTO User
				VALUES(:newID, :nameL, :nameF, :address, :email, :prefType);"""

	# Return false if failed

	try:
		cursor.execute(query2, {"newID": newID, "nameL": nameL, "nameF": nameF, "address": address, "email": email, "prefType": prefType})
		return newID
	except:
		return 0

def addStaff(cursor, nameF, nameL, address, email, phoneNum, position='LIBRARIAN',UserID=None, volunteer='FALSE'):

	# Find greatest/newest ID, add 1 for new ID

	query1 = """SELECT MAX(StaffID)
			FROM Staff;"""

	newID = cursor.execute(query1).fetchone()[0] + 1

	# Insert new ID into table

	query2 = """INSERT INTO Staff
				VALUES(:newID, :nameL, :nameF, :address, :email, :phoneNum, DATE(), :position, :volunteer, :UserID)"""
	
	# Return false if failed

	try:
		cursor.execute(query2, {"newID": newID, "nameL": nameL, "nameF": nameF, "address": address, "email": email, "phoneNum": phoneNum, "position": position, "volunteer": volunteer, "UserID": UserID})
		return newID
	except:
		return 0

def askForHelp(cursor, UserID):

	# Get all staff that are librarians

	query1 = """SELECT FirstName, LastName, StaffID
				FROM Staff
				WHERE Position = 'LIBRARIAN'
				"""
	librarian = choice(cursor.execute(query1).fetchall())

	query2 = """SELECT Email
				FROM User
				WHERE UserID = :UserID;
				"""

	userEmail = cursor.execute(query2,{"UserID":UserID}).fetchone()[0]

	if(userEmail == None):
                newEmail = input("Please add an Email: ")
                addEmail(cursor, UserID, newEmail)
		 

	# We would send them a message and notify them, which they would then respond to 
	# but we're not setting up a twillio or other messenging service

	print(librarian[0], librarian[1], "has been notified, and will send you an email to help you out!")

def updateCharges(cursor):

	# For all entries in borrowing where DATE > DUE DATE and RETURNDATE = 0, increment charge by one day

	query1 = """UPDATE Borrowing
				SET Charge = (JULIANDAY(DATE()) - JULIANDAY(DueDate)) * 0.50
				WHERE DATE() > DueDate
					AND ReturnDate = '0000-00-00';
				"""

	cursor.execute(query1)

def searchUserID(cursor, UserID):

	# Form query, execute, return result

	query1 = """SELECT UserID, FirstName, LastName, Address, Email, prefType
				FROM User
				WHERE UserID = :UserID
				"""

	return cursor.execute(query1, {"UserID": UserID}).fetchone()

def addEmail(cursor, UserID, newEmail):

	# Form query

	query1 = """UPDATE User
				SET Email = :newEmail
				WHERE UserID = :UserID
				"""
	try:
		cursor.execute(query1, {"newEmail":newEmail,"UserID": UserID})
	except:
		raise Exception("User not found")

def checkBorrowings(cursor, UserID):

	updateCharges(cursor)

	return cursor.execute("SELECT * FROM Borrowing WHERE UserID = :UserID AND ReturnDate = '0000-00-00'", {"UserID": UserID}).fetchall()

def isValidUser(cursor, UserID):

	query1 = """SELECT UserID
				FROM User
				WHERE UserID = :UserID"""

	return len(cursor.execute(query1, {"UserID": UserID}).fetchone()) > 0

def getReccomendedEvents(cursor, UserID):

	query1 = """SELECT prefType
				FROM User
				WHERE UserID = :UserID
				"""

	UserType = cursor.execute(query1, {"UserID": UserID}).fetchone()[0]

	# Form Query

	query2 = """SELECT *
				FROM Event
				WHERE Type = :UserType
				"""

	return cursor.execute(query2, {"UserType": UserType}).fetchall()

def putOnOrder(cursor):
	
	newID = donateItem(cursor)

	query1 = """UPDATE Item
				SET Availablity = FALSE, OnOrder = TRUE
				WHERE ItemID = :newID;
				"""

	cursor.execute(query1, {"newID": newID})