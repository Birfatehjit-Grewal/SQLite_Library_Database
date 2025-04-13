import sqlite3
from datetime import date
from App import * 
conn = sqlite3.connect('Library.db')
cursor = conn.cursor()
Loop1 = True
while(Loop1):
        print("Welcome, Please Chose One of the Following:")
        print("[1] Login Using UserID")
        print("[2] Register")
        print("[3] Admin")
        print("[4] Exit")
        typeChoice = int(input("Input number [1-4]: "))
        match typeChoice:
                case 1:
                        Loop2 = True
                        while(Loop2):
                                UserID = int(input("Enter UserID: "))
                                rows = searchUserID(cursor,UserID)
                                if(rows):
                                        Loop3 = True
                                        while(Loop3):
                                                print("What would you like to do:")
                                                print("[1] Find an item")
                                                print("[2] Borrow an item")
                                                print("[3] Check Borrowed Items")
                                                print("[4] Return an item")
                                                print("[5] Pay Charges")
                                                print("[6] Donate an item")
                                                print("[7] Find an event")
                                                print("[8] Event Reccomendations")
                                                print("[9] Register for an event")
                                                print("[10] Volunteer")
                                                print("[11] Ask For Help")
                                                print("[12] Exit")
                                                typeChoice = int(input("Input number [1-12]: "))
                                                match typeChoice:
                                                        case 1:
                                                                Loop4 = True
                                                                while(Loop4):
                                                                        Title = input("Enter Title: ")
                                                                        rows = findItemsByName(cursor,Title)
                                                                        if(rows):
                                                                                for row in rows:
                                                                                        print("Title: "+row[0]+", ItemID: "+str(row[1])+", Type: "+row[2]+", Availability: "+str(row[3])+", Ordered: "+str(row[4]))
                                                                                Loop4 = False
                                                                        else:
                                                                                print("No Item found with the Title: "+ Title)
                                                                                Loop4 = False
                                                        case 2:
                                                                ItemID = int(input("Enter ItemID: "))
                                                                try:
                                                                        borrowItemByID(cursor,ItemID,UserID)
                                                                        print("Borrowed Item with ItemID: "+str(ItemID))
                                                                except:
                                                                        print("")        
                                                                        
                                                        case 4:
                                                                ItemID = int(input("Enter ItemID: "))
                                                                try:
                                                                        returnItemByID(cursor,ItemID)
                                                                        print("Returned Item with ItemID: "+str(ItemID))
                                                                except:
                                                                        print("")
                                                                

                                                        case 5:
                                                                Loop4 = True
                                                                while(Loop4):
                                                                        charges = getUserOwes(cursor,UserID)
                                                                        print("Current Charges = "+str(charges))
                                                                        print("Would You Like to pay the charge right now: ")
                                                                        print("[1] Yes")
                                                                        print("[2] No")
                                                                        Pay = int(input("Input number [1-2]: "))
                                                                        match Pay:
                                                                                case 1:
                                                                                        payBalance(cursor,UserID)
                                                                                        Loop4 = False
                                                                                case 2:
                                                                                        Loop4 = False
                                                                                case _:
                                                                                        print("Invalid Entry")
                                                        case 6:
                                                                donateItem(cursor)
                                                        case 7:
                                                                findevent(cursor)
                                                        case 9:
                                                                eventRegister(cursor,UserID)
                                                        case 10:
                                                                Loop3 = True
                                                                while(Loop3):
                                                                        First = input("First Name: ")
                                                                        Last = input("Last Name: ")
                                                                        Address = input("Address: ")
                                                                        Email = input("Email: ")
                                                                        PNumber = input("Phone Number: ")
                                                                        print("Select Position:")
                                                                        print("[1] LIBRARIAN")
                                                                        print("[2] EVENT STAFF")
                                                                        print("[3] CAFE")
                                                                        print("[4] YOUTH WORKER")
                                                                        print("[5] CUSTODIAL")
                                                                        Loop4 = True
                                                                        while(Loop4):
                                                                                typechoice1 = int(input("Input number [1-5]: "))
                                                                                match typechoice1:
                                                                                        case 1:
                                                                                                Position = 'LIBRARIAN'
                                                                                                Loop4 = False
                                                                                        case 2:
                                                                                                Position = 'EVENT STAFF'
                                                                                                Loop4 = False
                                                                                        case 3:
                                                                                                Position = 'CAFE'
                                                                                                Loop4 = False
                                                                                        case 4:
                                                                                                Position = 'YOUTH WORKER'
                                                                                                Loop4 = False
                                                                                        case 5:
                                                                                                Position = 'CUSTODIAL'
                                                                                                Loop4 = False
                                                                                        case _:
                                                                                                print("Invalid choice. Try again\n")
                                                                        StaffID = addStaff(cursor,First,Last,Address,Email,PNumber,Position,UserID,'TRUE')
                                                                        if(StaffID != 0):
                                                                                print("Registered New StaffID = "+ str(UserID))
                                                                        else:
                                                                                print("Failed to Register User")
                                                                        Loop3 = False
                                                                
                                                                        
                                                        case 11:
                                                                askForHelp(cursor,UserID)
                                                        case 12:
                                                                Loop3 = False
                                                                Loop2 = False
                                                        case 3:
                                                                rows = checkBorrowings(cursor,UserID)
                                                                if(rows):
                                                                        for row in rows:
                                                                                print("ItemID: "+str(row[1])+", Borrow Date: "+str(row[2]+ ", Due Date: "+ str(row[3])))
                                                                else:
                                                                        print("No Item is currently Borrowed")
                                                        case 8:
                                                                rows = getReccomendedEvents(cursor,UserID)
                                                                if(rows):
                                                                        for row in rows:
                                                                                print("EventName: " + row[0] + ", Event Date: " + row[1])
                                                                else:
                                                                        print("No Item is currently Borrowed")
                                                        case _:
                                                                print("Invalid choice. Try again\n")
                                else:
                                        print("Incorrect UserID")
                                        Loop2 = False
                                
                case 2:
                        Loop3 = True
                        while(Loop3):
                                First = input("First Name: ")
                                Last = input("Last Name: ")
                                Address = input("Address (Optional press Enter to continue): ")
                                if(Address.strip() == ""):
                                        Address = "NULL"
                                Email = input("Email (Optional press Enter to continue): ")
                                if(Email.strip() == ""):
                                        Address = "NULL"
                                print("Select Event Type:")
                                print("[1] BOOK EVENT")
                                print("[2] BOOK CLUB")
                                print("[3] CLUB")
                                print("[4] ART SHOW")
                                print("[5] FILM SCREENING")
                                print("[6] READING")
                                print("[7] LECTURE")
                                print("[8] MEET AND GREET")
                                Loop4 = True
                                while(Loop4):
                                        typechoice1 = int(input("Input number [1-8]: "))
                                        match typechoice1:
                                                case 1:
                                                        PrefType = 'BOOK EVENT'
                                                        Loop4 = False
                                                case 2:
                                                        PrefType = 'BOOK CLUB'
                                                        Loop4 = False
                                                case 3:
                                                        PrefType = 'CLUB'
                                                        Loop4 = False
                                                case 4:
                                                        PrefType = 'ART SHOW'
                                                        Loop4 = False
                                                case 5:
                                                        PrefType = 'FILM SCREENING'
                                                        Loop4 = False
                                                case 6:
                                                        PrefType = 'READING'
                                                        Loop4 = False
                                                case 7:
                                                        PrefType = 'LECTURE'
                                                        Loop4 = False
                                                case 8:
                                                        PrefType = 'MEET AND GREET'
                                                        Loop4 = False
                                                case _:
                                                        print("Invalid choice. Try again\n")
                                UserID = addUser(cursor,First,Last,Address,Email,PrefType)
                                if(UserID != 0):
                                        print("Registered New UserID = "+ str(UserID))
                                else:
                                        print("Failed to Register User")
                                Loop3 = False
                case 3:
                        Loop2 = True
                        while(Loop2):
                                print("Please Chose One of the Following:")
                                print("[1] Put Item on order")
                                print("[2] Add Staff")
                                print("[3] Change ShelfID")
                                print("[4] Exit")
                                typeChoice = int(input("Input number [1-4]: "))
                                match typeChoice:
                                        case 1:
                                                putOnOrder(cursor)
                                        case 2:
                                                Loop3 = True
                                                while(Loop3):
                                                        First = input("First Name: ")
                                                        Last = input("Last Name: ")
                                                        Address = input("Address: ")
                                                        Email = input("Email: ")
                                                        PNumber = input("Phone Number: ")
                                                        print("Select Position:")
                                                        print("[1] LIBRARIAN")
                                                        print("[2] EVENT STAFF")
                                                        print("[3] CAFE")
                                                        print("[4] YOUTH WORKER")
                                                        print("[5] CUSTODIAL")
                                                        print("[6] MANAGER")
                                                        Loop4 = True
                                                        while(Loop4):
                                                                typechoice1 = int(input("Input number [1-6]: "))
                                                                match typechoice1:
                                                                        case 1:
                                                                                Position = 'LIBRARIAN'
                                                                                Loop4 = False
                                                                        case 2:
                                                                                Position = 'EVENT STAFF'
                                                                                Loop4 = False
                                                                        case 3:
                                                                                Position = 'CAFE'
                                                                                Loop4 = False
                                                                        case 4:
                                                                                Position = 'YOUTH WORKER'
                                                                                Loop4 = False
                                                                        case 5:
                                                                                Position = 'CUSTODIAL'
                                                                                Loop4 = False
                                                                        case 6:
                                                                                Position = 'MANAGER'
                                                                                Loop4 = False
                                                                        case _:
                                                                                print("Invalid choice. Try again\n")
                                                        StaffID = addStaff(cursor,First,Last,Address,Email,PNumber,Position,None,'FALSE')
                                                        if(StaffID != 0):
                                                                print("Registered New StaffID = "+ str(StaffID))
                                                        else:
                                                                print("Failed to Register User")
                                                        Loop3 = False

                                        case 3:
                                                ItemID = input("Enter ItemID: ")
                                                ShelfID = input("Enter ShelfID: ")
                                                shelfItem(cursor, ItemID, ShelfID)
                                        case 4:
                                                Loop2 = False
                                        case _:
                                                print("Invalid choice. Try again\n")
                case 4:
                        print("Exiting Interface")
                        if conn:
                                conn.commit()
                                print("Committed Changes!\n")
                                conn.close()
                                print("Closed database successfully")
                        Loop1 = False
                case _:
                        print("Invalid Entry")
