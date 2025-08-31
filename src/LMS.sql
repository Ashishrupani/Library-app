CREATE TABLE publisher(
    pubName VARCHAR(20),
    pubPhone INT,
    pubAddress VARCHAR(50),

    PRIMARY KEY (pubName) 
);

CREATE TABLE libraryBranch(
    branchID INT,
    branchName VARCHAR(20),
    branchAddress VARCHAR(50),

    PRIMARY KEY (branchID)
);

CREATE TABLE borrower(
    cardNo INT,
    borrName VARCHAR(20),
    borrAddress VARCHAR(50),
    borrPhone INT,

    PRIMARY KEY (cardNo)
);

CREATE TABLE book(
    bookID INT PRIMARY KEY,
    bookTitle VARCHAR(30),
    bookPub VARCHAR(20),

    FOREIGN KEY (bookPub) REFERENCES publisher(pubName)
);

CREATE TABLE bookLoans(
    bookID INT,
    branchID INT,
    cardNo INT,
    dateOut DATE,
    dueDate DATE,
    returnedDate DATE,

    FOREIGN KEY (bookID) REFERENCES book(bookID) ON UPDATE CASCADE,
    FOREIGN KEY (branchID) REFERENCES libraryBranch(branchID) ON UPDATE CASCADE,
    FOREIGN KEY (cardNo) REFERENCES borrower(cardNo) ON UPDATE CASCADE
);

CREATE TABLE book_copies (
    book_id INT,
    branch_id INT,
    no_of_copies INT,

    FOREIGN KEY (book_id) REFERENCES book(bookID) ON UPDATE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES libraryBranch(branchID) ON UPDATE CASCADE
);

CREATE TABLE book_authors (
    book_id INT,
    author_name VARCHAR(100),

    FOREIGN KEY (book_id) REFERENCES book(bookID) ON UPDATE CASCADE
);

-- publisher
INSERT INTO publisher(pubName, pubPhone, pubAddress)
VALUES
    ('HarperCollins', '212-207-7000', '195 Broadway, New York, NY 10007'),
    ('Penguin Books', '212-366-3000', '475 Hudson St, New York, NY 10014'),
    ('Penguin Classics', '212-366-2000', '123 Main St, California, CA 01383'),
    ('Scribner', '212-207-7474', '19 Broadway, New York, NY 10007'),
    ('Harper & Row', '212-207-7000', '1195 Border street, Montana, MT 59007'),
    ('Little, Brown and Company', '212-764-2000', '111 Huddle St, New Jersey, NJ 32014'),
    ('Faber and Faber', '201-797-3800', '463 south centre street, Arizona, AR 71653'),
    ('Chatto & Windus', '442-727-3800', 'Bloomsbury House, 7477 Great Russell St, Arizona, AR 72965'),
    ('Ward, Lock and Co.', '647-242-3434', '456 Maple Ave, Texas, TX 76013'),
    ('Random House India', '291-225-6634', '423 baywatch centre street, Alabama, AL 30513'),
    ('Thomas Cautley Newby', '243-353-2352', '890 Elmwood Dr, Floride, FL 98238'),
    ('Allen & Unwin', '212-782-9001', '22 New Wharf Rd, Arizona, AR 70654'),
    ('Pan Books', '313-243-5353', '567 Pine Tree Rd, Colorado, CO 87348'),
    ('Bantam Books', '313-243-5354', '1745 Broadway, New York, NY 10019'),
    ('Doubleday', '212-782-9000', '789 Division St, Minnesota, MN 55344'),
    ('American Publishing Company', '682-243-3524', '7652 Northgate way lane, Georgia, GA 30054'),
    ('Chapman and Hall', '833-342-2343', '789 Oak St, Texas, TX 76010');


--Liabrary Branch
INSERT INTO libraryBranch(branchId, branchName, branchAddress)
VALUES
    (1, 'Main Branch', '123 Main St, New York, NY 10003'),
    (2, 'West Branch', '456 West St, Arizona, AR 70622'),
    (3, 'East Branch', '789 East St, New Jersey, NY 32032');

--Borrower
INSERT INTO borrower(cardNo, borrName, borrAddress, borrPhone)
VALUES
    (123456, 'John Smith', '456 Oak St, Arizona, AR 70010', '205-555-5555'),
    (789012, 'Jane Doe', '789 Maple Ave, New Jersey, NJ 32542', '555-235-5556'),
    (345678, 'Bob Johnson', '12 Elm St, Arizona, AR 70345', '545-234-5557'),
    (901234, 'Sarah Kim', '345 Pine St, New York, NY 10065', '515-325-2158'),
    (567890, 'Tom Lee', '678 S Oak St, New York, NY 10045', '209-525-5559'),
    (234567, 'Emily Lee', '389 Oaklay St, Arizona, AR 70986', '231-678-5560'),
    (890123, 'Michael Park', '123 Pinewood St, New Jersey, NJ 32954', '655-890-2161'),
    (456789, 'Laura Chen', '345 Mapman Ave, Arizona, AR 70776', '565-985-9962'),
    (111111, 'Alex Kim', '983 Sine St, Arizona, AR 70451', '678-784-5563'),
    (222222, 'Rachel Lee', '999 Apple Ave, Arizona, AR 70671', '231-875-5564'),
    (333333, 'William Johnson', '705 Paster St, New Jersey 32002', '235-525-5567'),
    (444444, 'Ethan Martinez', '466 Deeplm St, New York, NY 10321', '555-555-5569'),
    (555555, 'Grace Hernandez', '315 Babes St, Arizona, AR 70862', '455-567-5587'),
    (565656, 'Sophia Park', '678 Dolphin St, New York, NY 10062', '675-455-5568'),
    (676767, 'Olivia Lee', '345 Spine St, New York, NY 10092', '435-878-5569'),
    (787878, 'Noah Thompson', '189 GreenOak Ave, New Jersey, NJ 32453', '245-555-5571'),
    (989898, 'Olivia Smith', '178 Elm St, New Jersey, NJ 32124', '325-500-5579'),
    (121212, 'Chloe Park', '345 Shark St, Arizona, AR 72213', '755-905-5572'),
    (232323, 'William Chen', '890 Sting St, New York, NY 10459', '406-755-5580'),
    (343434, 'Olivia Johnson', '345 Pine St, New Jersey, NJ 32095', '662-554-5575'),
    (454545, 'Dylan Kim', '567 Cowboy way St, New Jersey, NJ 32984', '435-254-5578');

--BOOK
INSERT INTO book(bookID, bookTitle, bookPub)
VALUES
    (1, 'To Kill a Mockingbird', 'HarperCollins'),
    (2, '1984', 'Penguin Books'),
    (3, 'Pride and Prejudice', 'Penguin Classics'),
    (4, 'The Great Gatsby', 'Scribner'),
    (5, 'One Hundred Years of Solitude', 'Harper & Row'),
    (6, 'Animal Farm', 'Penguin Books'),
    (7, 'The Catcher in the Rye', 'Little, Brown and Company'),
    (8, 'Lord of the Flies', 'Faber and Faber'),
    (9, 'Brave New World', 'Chatto & Windus'),
    (10, 'The Picture of Dorian Gray', 'Ward, Lock and Co.'),
    (11, 'The Alchemist', 'HarperCollins'),
    (12, 'The God of Small Things', 'Random House India'),
    (13, 'Wuthering Heights', 'Thomas Cautley Newby'),
    (14, 'The Hobbit', 'Allen & Unwin'),
    (15, 'The Lord of the Rings', 'Allen & Unwin'),
    (16, 'The Hitchhikers Guide to the Galaxy', 'Pan Books'),
    (17, 'The Diary of a Young Girl', 'Bantam Books'),
    (18, 'The Da Vinci Code', 'Doubleday'),
    (19, 'The Adventures of Huckleberry Finn', 'Penguin Classics'),
    (20, 'The Adventures of Tom Sawyer', 'American Publishing Company'),
    (21, 'A Tale of Two Cities', 'Chapman and Hall');


--bookloans
INSERT INTO bookLoans(bookID, branchID, cardNo, dateOut, dueDate, returnedDate)
VALUES
    (1, 1, 123456, '2022-01-01', '2022-02-01', '2022-02-01'),
    (2, 1, 789012, '2022-01-02', '2022-02-02', NULL),
    (3, 2, 345678, '2022-01-03', '2022-02-03', NULL),
    (4, 3, 901234, '2022-01-04', '2022-02-04', '2022-02-04'),
    (5, 1, 567890, '2022-01-05', '2022-02-05', '2022-02-09'),
    (6, 2, 234567, '2022-01-06', '2022-02-06', '2022-02-10'),
    (7, 2, 890123, '2022-01-07', '2022-02-07', '2022-03-08'),
    (8, 3, 456789, '2022-01-08', '2022-02-08', '2022-03-10'),
    (9, 1, 111111, '2022-01-09', '2022-02-09', '2022-02-06'),
    (10, 2, 222222, '2022-01-10', '2022-02-10', '2022-02-07'),
    (11, 1, 333333, '2022-03-01', '2022-03-08', '2022-03-08'),
    (12, 3, 444444, '2022-03-03', '2022-03-10', '2022-03-10'),
    (13, 3, 555555, '2022-02-03', '2022-03-03', '2022-02-18'),
    (14, 1, 565656, '2022-01-14', '2022-02-14', '2022-03-31'),
    (15, 3, 676767, '2022-01-15', '2022-02-15', '2022-02-21'),
    (16, 2, 787878, '2022-03-05', '2022-03-12', '2022-03-24'),
    (17, 3, 989898, '2022-03-23', '2022-03-30', '2022-03-30'),
    (18, 3, 121212, '2022-01-18', '2022-02-18', '2022-02-18'),
    (19, 1, 232323, '2022-03-24', '2022-03-31', '2022-03-31'),
    (20, 3, 343434, '2022-01-21', '2022-02-21', '2022-02-21'),
    (21, 3, 454545, '2022-01-24', '2022-02-24', '2022-02-24');


--book copies
INSERT INTO book_copies(book_id, branch_id, no_of_copies)
VALUES
    (1, 1, 3),
    (2, 1, 2),
    (3, 2, 1),
    (4, 3, 4),
    (5, 1, 5),
    (6, 2, 3),
    (7, 2, 2),
    (8, 3, 1),
    (9, 1, 4),
    (10, 2, 2),
    (11, 1, 3),
    (12, 3, 2),
    (13, 3, 1),
    (14, 1, 5),
    (15, 3, 1),
    (16, 2, 3),
    (17, 3, 2),
    (18, 3, 2),
    (19, 1, 5),
    (20, 3, 1),
    (21, 3, 1);


--book authors
INSERT INTO book_authors(book_id, author_name) 
VALUES
    (1, 'Harper Lee'),
    (2, 'George Orwell'),
    (3, 'Jane Austen'),
    (4, 'F. Scott Fitzgerald'),
    (5, 'Gabriel Garcia Marquez'),
    (6, 'George Orwell'),
    (7, 'J.D. Salinger'),
    (8, 'William Golding'),
    (9, 'Aldous Huxley'),
    (10, 'Oscar Wilde'),
    (11, 'Paulo Coelho'),
    (12, 'Arundhati Roy'),
    (13, 'Emily Bronte'),
    (14, 'J.R.R. Tolkien'),
    (15, 'J.R.R. Tolkien'),
    (16, 'Douglas Adams'),
    (17, 'Anne Frank'),
    (18, 'Dan Brown'),
    (19, 'Mark Twain'),
    (20, 'Mark Twain'),
    (21, 'Charles Dickens');


CREATE TRIGGER bookCopies
AFTER INSERT ON bookLoans
FOR EACH ROW
BEGIN
   UPDATE book_copies
    SET no_of_copies = 
        CASE 
            WHEN no_of_copies > 0 THEN no_of_copies - 1 
            ELSE 0 
        END
    WHERE book_id = NEW.bookID AND branch_id = NEW.branchID;
END;

.mode table
.header on

--First Query
INSERT INTO borrower (borrName, borrAddress, borrPhone)
VALUES ('Group5 member', '911 Copper St, Arlington, TX 99099', '682-702-4792');

--Second Query
UPDATE borrower
SET borrPhone = '837-721-8965'
WHERE borrName = 'Group5 member';

--Third Query
UPDATE book_copies
SET no_of_copies = no_of_copies + 1
WHERE branch_id = (
    SELECT branchID
    FROM libraryBranch
    WHERE branchName = 'East Branch'
);

--Fourth Query (a)
INSERT INTO book (bookID, bookTitle, bookPub)
VALUES (22, 'Harry Potter and the Sorcerers Stone', 'Oxford Publishing');

INSERT INTO book_authors(book_id, author_name)
VALUES (22, 'J.K. Rowling');

--Fourth Query (b)
INSERT INTO libraryBranch (branchName, branchAddress)
VALUES ('North Branch', '456 NW, Irving, TX 76100'), 
       ('UTA Branch', '123 Cooper St, Arlington, TX 76101');

--Fifth Query
SELECT book.bookTitle, libraryBranch.branchName, (julianday(bookLoans.dueDate) - julianday(bookLoans.dateOut)) AS days_borrowed
FROM bookLoans
JOIN book ON bookLoans.bookID = book.bookID
JOIN libraryBranch  ON bookLoans.branchID = libraryBranch.branchID
WHERE bookLoans.dateOut BETWEEN '2022-03-05' AND '2022-03-23'; 

--Sixth Query
SELECT borrName
FROM borrower
JOIN bookLoans ON bookLoans.cardNo = borrower.cardNo
WHERE bookLoans.returnedDate IS NULL;

--Seventh Query 
SELECT branchName, COUNT(bookLoans.bookID) AS numBooksBorr, COUNT (julianday(returnedDate) <= julianday(dueDate)) AS booksReturned, SUM (julianday(returnedDate) IS NULL AND julianday(CURRENT_DATE)) AS stillBorrowed, COUNT (julianday(returnedDate) > julianday(dueDate)) AS lateReturn
FROM libraryBranch
JOIN bookLoans ON bookLoans.branchID = libraryBranch.branchID
JOIN book ON book.bookID = bookLoans.bookID
--JOIN book_copies ON book_copies.book_id = book.bookID
GROUP BY bookLoans.branchID, libraryBranch.branchName;

--Eighth Query 
SELECT bookTitle, MAX (julianday(dueDate) - julianday(dateOut)) AS numDaysBorr
FROM book
JOIN bookLoans ON bookLoans.bookID = book.bookID
GROUP BY book.bookTitle;

--Ninth Query
SELECT borrName, bookTitle, author_name, (julianday(dueDate) - julianday(dateOut)) AS numDaysBorr, (julianday(returnedDate) > julianday(dueDate)) AS lateReturn
FROM borrower
JOIN bookLoans ON bookLoans.cardNo = borrower.cardNo
JOIN book ON book.bookID = bookLoans.bookID
JOIN book_authors On book_authors.book_id = book.bookID
WHERE borrName = 'Ethan Martinez'
GROUP BY book.bookID;

--Tenth Query
SELECT borrName, borrAddress
FROM borrower
JOIN bookLoans ON bookLoans.cardNo = borrower.cardNo
JOIN libraryBranch ON libraryBranch.branchID = bookLoans.branchID
WHERE branchName = 'West Branch';

--UPDATE ID
UPDATE libraryBranch
SET branchID = 4 
WHERE branchName = 'North Branch';

UPDATE libraryBranch
SET branchID = 5 
WHERE branchName = 'UTA Branch';

--First Query
ALTER TABLE bookLoans
ADD Late INT;

UPDATE bookLoans
SET Late = 
CASE WHEN julianday(returnedDate) <= julianday(dueDate) THEN 0
WHEN julianday(returnedDate) > julianday(dueDate) OR returnedDate IS NULL THEN 1 
END;

SELECT * FROM bookLoans;

--Second Query
ALTER TABLE libraryBranch
ADD LateFee INT;

UPDATE libraryBranch
SET LateFee = 
CASE WHEN branchId = 1 THEN 4.00
WHEN branchId = 2 THEN 5.00
WHEN branchId = 3 THEN 6.00
END; 

SELECT * FROM libraryBranch;

--Third Query
CREATE VIEW vBookLoanInfo (
    Card_No,
    Borrower_Name,
    Date_Out,
    Due_Date,
    Returned_date,
    TotalDays,
    Book_Title,
    No_of_days_returned_late, 
    Branch_ID,
    LateFeeBalance
) AS 
    SELECT bl.cardNo, 
    b.borrName, 
    bl.dateOut, 
    bl.dueDate, 
    bl.returnedDate, 
    CASE WHEN julianday(returnedDate) - julianday(dateOut) <= 0 THEN 0 
         WHEN julianday(returnedDate) - julianday(dateOut) IS NULL THEN 0 
         ELSE julianday(returnedDate) - julianday(dateOut) END, 
    bk.bookTitle, 
    CASE WHEN julianday(returnedDate) - julianday(dueDate) <= 0 THEN 0 
         WHEN julianday(returnedDate) - julianday(dueDate) IS NULL THEN 0 
         ELSE julianday(returnedDate) - julianday(dueDate) END AS returnedLate, 
    lb.branchId, 
    ((CASE WHEN julianday(returnedDate) - julianday(dueDate) <= 0 THEN 0.00 
           WHEN julianday(returnedDate) - julianday(dueDate) IS NULL THEN 0.00 
           ELSE julianday(returnedDate) - julianday(dueDate) END) * lb.LateFee) AS LateFeeBalance
    FROM bookLoans bl
    JOIN borrower b ON b.cardNo = bl.cardNo
    JOIN libraryBranch lb ON lb.branchId = bl.branchId
    JOIN book bk ON bk.bookId = bl.bookId;

SELECT * FROM vBookLoanInfo;
