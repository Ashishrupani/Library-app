from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import date, timedelta
import random

# Get today's date
today = date.today()


# Create tkinter window
root = Tk()
root.title('LIBRARY DB')
root.geometry("800x500")  # Adjust the window size as needed

# Connect to the database
name = 'library.db'
conn = sqlite3.connect(name)
conn.close()  # Close the connection as it's not used immediately
print("Connected to DB Successfully")


main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

first_canvas = Canvas(main_frame)
first_canvas.pack(side=LEFT, fill=BOTH, expand=1)

scroll_ = ttk.Scrollbar(main_frame, orient=VERTICAL, command=first_canvas.yview)
scroll_.pack(side=RIGHT, fill=Y)

first_canvas.configure(yscrollcommand=scroll_.set)
#first_canvas.bind('<Configure>', lambda e: first_canvas.configure(scrollregion= first_canvas.bbox("all")))

#Created a container within the main frame to hold buttons and stuff
second_frame = Frame(first_canvas)
first_canvas.create_window((0,0), window=second_frame, anchor="nw")
#second_frame.bind('<MouseWheel>', lambda e: first_canvas.yview_scroll(e.delta / 60, "units"))

scroll_horizontal = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=first_canvas.xview)
scroll_horizontal.pack(side=BOTTOM, fill=X)

##functions that will help in showing and deleting output
def clean():
    print_label.grid_remove()

def print_out(output):
    global print_label
    print_label = Label(second_frame, text = output, justify=LEFT)
    print_label.grid(row = 15, column = 0, columnspan = 2 )
print_out("") 

def showBooks():
    showBooks_conn = sqlite3.connect(name)
    showBooks_cur = showBooks_conn.cursor()
    showBooks_cur.execute("""SELECT bookID, bookTitle FROM book""")
    records = showBooks_cur.fetchall()
    lines = "ID\t" + "Book Title\t" +"\n"
    for i in records:
        lines += str(i[0]) + "\t" + str(i[1]) + "\n"
    clean()
    print_out(lines)
    
def checkOut():
    checkOut_conn = sqlite3.connect(name)  # Connect to the database
    checkOut_cur = checkOut_conn.cursor()
    checkOut_cur.execute("SELECT bookID FROM book WHERE bookTitle = ?", (checkOut_box.get(),))
    book_id = checkOut_cur.fetchone()
    if not book_id:
        clean()
        print_out("Error: Book not found. Ensure the title is correct.")
        checkOut_conn.close()
        return 
    else:
        book_id = book_id[0]
    
    # Insert into bookLoans table
    checkOut_cur.execute("SELECT no_of_copies FROM book_copies WHERE book_id = ? AND branch_id = ?", (book_id, branchIDOut_box.get()))
    book_copy = checkOut_cur.fetchone()
    if not book_copy:
        clean()
        print_out("Error: Both entires need to be correct(book and branch (ID))")
        checkOut_conn.close()
        return
    else:
        book_copy = book_copy[0]
        
    
    if book_copy > 0:
        if 'number' not in globals():
            clean()
            print_out("You need to make a borrower card first! (Add your information and click \"Add Borrower\")")
            return
        checkOut_cur.execute(
            "INSERT INTO bookLoans (bookID, branchID, cardNo, dateOut, dueDate, returnedDate) "
            "VALUES (?, ?, ?, ?, ?, ?)", (book_id, branchIDOut_box.get(), number ,today,today + timedelta(days=30),None))
        checkOut_cur.execute("""SELECT * FROM book_copies""")
        records = checkOut_cur.fetchall()
        lines = "Book successfully checked out!\n"
        lines += "bookID\t branchID\t No_of_copies\n"
        for i in records:
            lines += str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t\n" 
        clean()
        print_out(lines)
    else:
        clean()
        print_out("Sorry, no copies left. Out of Stock\n")
        
    # Commit and close the connection
    checkOut_conn.commit()
    checkOut_conn.close()

def borrower_button():
    borrBtn_conn = sqlite3.connect(name)  # Connect to the database
    borrBtn_cur = borrBtn_conn.cursor()
    
    bor_name = borr_name_box.get()
    bor_add = borr_address_box.get()
    bor_ph = borr_phone_number.get()
    
    if not bor_name or not bor_add or not bor_ph:
        clean()
        print_out("Error: ALL FIELDS REQUIRED TO MAKE A CARD!")
    else:
        global number
        number = random.randint(111111, 999999)
        borrBtn_cur.execute("INSERT INTO borrower (cardNo, borrName, borrAddress, borrPhone) "
            "VALUES (?, ?, ?, ?)", (number , borr_name_box.get(), borr_address_box.get(), borr_phone_number.get()))
        
        borrBtn_conn.commit()
        borrBtn_conn.close()
        
        borrBtn_conn = sqlite3.connect(name)  # Connect to the database
        borrBtn_cur = borrBtn_conn.cursor()
        borrBtn_cur.execute("SELECT * FROM borrower WHERE borrName = ? AND cardNo = ?", (borr_name_box.get(), number, ))
        records = borrBtn_cur.fetchall()
        lines = ""
        lines += "Your Borrower Card is Ready!\n"
        for i in records:
            lines += "Card NO: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Address: " +str(i[2]) + "\n" + "Phone No: " + str(i[3]) + "\n"
        clean()
        print_out(lines)
    borrBtn_conn.commit()
    borrBtn_conn.close()
    
def No_of_Copies():
    checkOut_conn = sqlite3.connect(name)  # Connect to the database
    checkOut_cur = checkOut_conn.cursor()
    
    checkOut_cur.execute("SELECT bookID FROM book WHERE bookTitle = ?", (checkOut_box.get(),))
    book_id = checkOut_cur.fetchone()

    if not book_id:
        clean()
        print_out("Error: Book not found. Ensure the title is correct.")
        checkOut_conn.close()
        return 
    else:
        book_id = book_id[0]

    checkOut_cur.execute("SELECT branch_id, no_of_copies FROM book_copies WHERE book_id = ?", (book_id,))
    records = checkOut_cur.fetchall()
    lines = ""
    lines += "Branch ID\tNo of Copies\n"
    for i in records:
        lines += str(i[0]) + "\t" + str(i[1]) + "\n"
    clean()
    print_out(lines)
    
    # Commit and close the connection
    checkOut_conn.commit()
    checkOut_conn.close()
    
def add_book():
    add_book_conn = sqlite3.connect(name)
    add_book_cur = add_book_conn.cursor()
    
    #make sure all entires are filled.
    bk_name = bk_box.get()
    id = id_box.get()
    auth = auth_box.get()
    #getting publisher name
    pb_name = publish.get()
    
    if not bk_name or not id or not auth:
        clean()
        print_out("Need to specify all entries to add a book to the collection!\n")
    else:
        clean()
        add_book_cur.execute("INSERT INTO book (bookID, bookTitle, bookPub) "
            "VALUES (?, ?, ?)", (id_box.get(), bk_box.get(), publish.get()))
        add_book_conn.commit()
        add_book_conn.close()
        
        add_book_conn = sqlite3.connect(name)
        add_book_cur = add_book_conn.cursor()
        add_book_cur.execute("INSERT INTO book_authors (book_id, author_name) "
            "VALUES (?, ?)", (id_box.get(), auth_box.get()))
        add_book_conn.commit()
        add_book_conn.close()
        
        add_book_conn = sqlite3.connect(name)
        add_book_cur = add_book_conn.cursor()
        for i in range(5):
            add_book_cur.execute("INSERT INTO book_copies (book_id, branch_id, no_of_copies) "
            "VALUES (?, ?, ?)", (id_box.get(), f"{i + 1}" , "5"))
        add_book_conn.commit()
        add_book_conn.close()
        
        
    
    
    add_book_conn.close()

def late_returns():
    late_returns_conn = sqlite3.connect(name)
    late_returns_cur = late_returns_conn.cursor()
    
    from_ = date_from.get()
    to_ = date_to.get()
    
    if not from_ or not to_:
        clean()
        print_out("ERROR: Need both entires for the date ranges.")
    else:
        clean()
        late_returns_cur.execute("""SELECT bookID, branchID, cardNo, dateOut, dueDate, returnedDate, CASE WHEN julianday(returnedDate) - julianday(dueDate) <= 0 THEN 0 
         WHEN julianday(returnedDate) - julianday(dueDate) IS NULL THEN 0 
         ELSE julianday(returnedDate) - julianday(dueDate) END 
         FROM bookLoans WHERE dueDate BETWEEN ? AND ?""", (date_from.get(), date_to.get()))
        records = late_returns_cur.fetchall()
        
        lines = "bookID\t branchID\t cardNo\t dateOut\t\t dueDate\t\t returnedDate\t days_returned_Late\t\n"
        for i in records:
            lines += str(i[0]) + "\t " + str(i[1]) + "\t " + str(i[2]) + "\t " + str(i[3]) + "\t " + str(i[4]) + "\t " + str(i[5]) + "\t\t " + str(i[6]) + "\t " + "\n"
        
        print_out(lines)
            
    late_returns_conn.commit()
    late_returns_conn.close()
    
def borrower_search():
    borrower_search_conn = sqlite3.connect(name)
    borrower_search_cur = borrower_search_conn.cursor()
    
    id = view_id_box.get()
    name_ = view_name_box.get()
    balance = view_balance_box.get()
    
    if not id and not name_ and not balance:
        borrower_search_cur.execute("SELECT Card_No, Borrower_Name, LateFeeBalance FROM vBookLoanInfo ORDER BY LateFeeBalance DESC")
    elif not name_:
        borrower_search_cur.execute("SELECT Card_No, Borrower_Name, LateFeeBalance FROM vBookLoanInfo WHERE Card_No = ? OR LateFeeBalance = ?", (id, view_balance_box.get()))
    elif id or name_ or balance:
        borrower_search_cur.execute("SELECT Card_No, Borrower_Name, LateFeeBalance FROM vBookLoanInfo WHERE Card_No = ? OR Borrower_Name LIKE ? OR LateFeeBalance = ?", (id, "%" + name_ +"%", view_balance_box.get()))
    
    records = borrower_search_cur.fetchall()
    lines = "BorrowerID\t BorrowerName\t LateFeeBalance\n"
    for i in records:
            lines += str(i[0]) + "\t\t" + str(i[1]) + "\t\t" + "$"+str(i[2]) + "\n"
    
    clean()
    print_out(lines)
    
    borrower_search_conn.commit()
    borrower_search_conn.close()

def book_search():
    book_search_conn = sqlite3.connect(name)
    book_search_cur = book_search_conn.cursor()
    
    id = view_id_b_box.get()
    book_id = view_bid_b_box.get()
    book_name = view_title_b_box.get()
    
    if not id and not book_id and not book_name:
        book_search_cur.execute("SELECT bookID, Book_Title, LateFeeBalance FROM book JOIN vBookLoanInfo ON book.bookTitle = vBookLoanInfo.Book_Title ORDER BY LateFeeBalance DESC")
    elif not book_name:
        book_search_cur.execute("SELECT bookID, Book_Title, LateFeeBalance FROM book JOIN vBookLoanInfo ON book.bookTitle = vBookLoanInfo.Book_Title WHERE  Card_No = ? OR  book.bookID= ?", (id, book_id))
    elif id or book_id or book_name:
        book_search_cur.execute("SELECT bookID, Book_Title, LateFeeBalance FROM book JOIN vBookLoanInfo ON book.bookTitle = vBookLoanInfo.Book_Title WHERE  Card_No = ? OR  book.bookID= ? OR Book_Title LIKE ?", (id, book_id, "%" + book_name + "%"))
    
    records = book_search_cur.fetchall()
    lines = "BookID\t\t BookTitle\t\t\t LateFeeBalance\n"
    for i in records:
            lines += str(i[0]) + "\t\t" + str(i[1]) + "\t\t\t" + "$"+str(i[2]) + "\n"
    
    clean()
    print_out(lines)
    
    book_search_conn.commit()
    book_search_conn.close()
    
    
    
#first requirement##########################################
#label
first_query = "To see the books available in the database: PRESS \"Show Book\"\n "
info_label = Label(second_frame, text = first_query, justify=LEFT)
info_label.grid(row=0, columnspan=6)

book_info = Label(second_frame, text ='Books available: ', justify=LEFT)
book_info.grid(row = 1, column = 0, columnspan = 1,)
bookTitle = Label(second_frame, text ='Book Title: ', justify=LEFT)
bookTitle.grid(row = 3, column = 0, columnspan = 1)

branchIdTitle = Label(second_frame, text ='Branch ID: ', justify=LEFT)
branchIdTitle.grid(row = 3, column = 2, columnspan = 1)

#buttons
show_button = Button(second_frame, text = "Show Books", command = showBooks)
show_button.grid(row = 1, column = 1, columnspan = 1, pady = 2, padx = 2, ipadx = 5)

clear_button = Button(second_frame, text = "Clear", command = clean)
clear_button.grid(row = 1, column = 2, columnspan = 1, pady = 2, padx = 2, ipadx = 5)


#textbox
checkOut_box = Entry(second_frame, width = 30)
checkOut_box.grid(row = 3, column = 1, padx = 20, columnspan = 1)

branchIDOut_box = Entry(second_frame, width = 30)
branchIDOut_box.grid(row = 3, column = 3, columnspan = 1, padx = 20)

check_out = Button(second_frame, text = "Check Out Book (book title and branch ID)", command = checkOut)
check_out.grid(row = 3, column = 5, columnspan = 1, pady = 5, padx = 5, ipadx = 5) #FOR THE CHECK OUT BUTTON


#SECOND REQUIREMENT##################################################
#LABELS
borr_name = Label(second_frame, text = 'Borrower Name: ')
borr_name.grid(row = 4, column = 0, columnspan = 1)

borrower_address = Label(second_frame, text ='Address: ')
borrower_address.grid(row = 4, column = 2, columnspan = 1)

borrower_phone = Label(second_frame, text ='Phone: ')
borrower_phone.grid(row = 4, column = 4, columnspan = 1)  

#TEXTBOXES
borr_name_box = Entry(second_frame, width = 30)
borr_name_box.grid(row = 4, column = 1, padx = 10, columnspan = 1)

borr_address_box = Entry(second_frame, width = 30)
borr_address_box.grid(row = 4, column = 3, padx = 10, columnspan = 1)

borr_phone_number = Entry(second_frame, width = 30)
borr_phone_number.grid(row = 4, column = 5, padx = 10, columnspan = 1) 

#BUTTON
AddBorrower = Button(second_frame, text = "Add Borrowers", command = borrower_button)
AddBorrower.grid(row = 4, column = 6, columnspan = 1, pady = 5, padx = 5, ipadx = 5)


#third requirement#############################################################
bk = Label(second_frame, text = 'Add Book: ')
bk.grid(row = 5, column = 0, columnspan = 1)

##DROP  MENU

publish = StringVar()
publish.set("Publisher Name")

publish_drop = OptionMenu(second_frame, publish, 'Harper Collins',
    'Penguin Books',
    'Penguin Classics',
    'Scribner',
    'Harper & Row',
    'Little, Brown and Company',
    'Faber and Faber',
    'Chatto & Windus',
    'Ward, Lock and Co.',
    'Random House India',
    'Thomas Cautley Newby',
    'Allen & Unwin',
    'Pan Books',
    'Bantam Books',
    'Doubleday',
    'American Publishing Company',
    'Chapman and Hall')

publish_drop.grid(row=5, column=2,columnspan=1)

bk_id = Label(second_frame, text = 'Book ID: ')
bk_id.grid(row = 5, column = 3, columnspan = 1)

auth_nm = Label(second_frame, text = 'Author name: ')
auth_nm.grid(row = 6, column = 0, columnspan = 1)


bk_box = Entry(second_frame, width = 30)
bk_box.grid(row = 5, column = 1, padx = 20, columnspan = 1)

id_box = Entry(second_frame, width = 30)
id_box.grid(row = 5, column = 4, padx = 20, columnspan = 1)

auth_box = Entry(second_frame, width = 30)
auth_box.grid(row = 6, column = 1, padx = 20, columnspan = 1)


###BUTTON
book_button = Button(second_frame, text = "ADD BOOK", command = add_book)
book_button.grid(row = 6, column = 3, columnspan = 2, pady = 5, padx = 5, ipadx = 50)




#fourth requirement#############################################################

#BUTTON
number_of_copies = Button(second_frame, text = "No of Copies(book title)", command = No_of_Copies)
number_of_copies.grid(row = 3, column = 4, columnspan = 1, pady = 5, padx = 5, ipadx = 50) #FOR THE CHECK OUT BUTTON




#fifth requirement#################
#LABELS
date_range_l = Label(second_frame, text = 'FROM DATE(YYYY-MM-DD): ')
date_range_l.grid(row = 7, column = 0, columnspan = 1)

date_range_2 = Label(second_frame, text = 'TO DATE(YYYY-MM-DD): ')
date_range_2.grid(row = 7, column = 2, columnspan = 1)

#ENTRIES
date_from = Entry(second_frame, width = 30)
date_from.grid(row = 7, column = 1, padx = 20, columnspan = 1)

date_to = Entry(second_frame, width = 30)
date_to.grid(row = 7, column = 3, padx = 20, columnspan = 1)

#BUTTON
date_button = Button(second_frame, text = "Search Late Returns", command = late_returns)
date_button.grid(row = 7, column = 4, columnspan = 1, pady = 5, padx = 5, ipadx = 5)




#6a Requirement###########
#LABEL
view_id = Label(second_frame, text = 'Borrower ID: ')
view_id.grid(row = 9, column = 0, columnspan = 1)

view_name = Label(second_frame, text = 'Borrower Name: ')
view_name.grid(row = 9, column = 2, columnspan = 1)

view_balance = Label(second_frame, text = 'Late Fee Balance: ')
view_balance.grid(row = 9, column = 4, columnspan = 1)

#ENTRIES
view_id_box = Entry(second_frame, width = 30)
view_id_box.grid(row = 9, column = 1, padx = 20, columnspan = 1)

view_name_box = Entry(second_frame, width = 30)
view_name_box.grid(row = 9, column = 3, padx = 20, columnspan = 1)

view_balance_box = Entry(second_frame, width = 30)
view_balance_box.grid(row = 9, column = 5, padx = 20, columnspan = 1)

#BUTTON
borr_search = Button(second_frame, text = "FIND", command = borrower_search)
borr_search.grid(row = 10, column = 0, columnspan = 6, pady = 5, padx = 5, ipadx = 5)


#6b requirement ###
view_id_b = Label(second_frame, text = 'Borrower ID: ')
view_id_b.grid(row = 11, column = 0, columnspan = 1)

view_bid_b = Label(second_frame, text = 'Book ID: ')
view_bid_b.grid(row = 11, column = 2, columnspan = 1)

view_title_b = Label(second_frame, text = 'Book Title: ')
view_title_b.grid(row = 11, column = 4, columnspan = 1)

#ENTRIES
view_id_b_box = Entry(second_frame, width = 30)
view_id_b_box.grid(row = 11, column = 1, padx = 20, columnspan = 1)

view_bid_b_box = Entry(second_frame, width = 30)
view_bid_b_box.grid(row = 11, column = 3, padx = 20, columnspan = 1)

view_title_b_box = Entry(second_frame, width = 30)
view_title_b_box.grid(row = 11, column = 5, padx = 20, columnspan = 1)

#BUTTON
borr_search = Button(second_frame, text = "FIND", command = book_search)
borr_search.grid(row = 12, column = 0, columnspan = 6, pady = 5, padx = 5, ipadx = 5)


# Function definitions for database operations and updates
root.mainloop()
