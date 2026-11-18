from database import connect_db
from datetime import date, timedelta


class Book:
    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies


class Member:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class LibraryManager:

    def add_book(self, title, author, copies):
        connection = connect_db()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO books
                (title, author, total_copies, available_copies)
                VALUES (?, ?, ?, ?)
            """, (title, author, copies, copies))

            connection.commit()
            print("\nBook added successfully!")

        except Exception as error:
            print("\nError:", error)

        finally:
            connection.close()

    def view_books(self):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        if not books:
            print("\nNo books found.")
        else:
            print("\n===== BOOK INVENTORY =====")

            for book in books:
                print(f"""
ID: {book[0]}
Title: {book[1]}
Author: {book[2]}
Total Copies: {book[3]}
Available Copies: {book[4]}
-------------------------
""")

        connection.close()

    def register_member(self, name, email):
        connection = connect_db()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO members (name, email)
                VALUES (?, ?)
            """, (name, email))

            connection.commit()
            print("\nMember registered successfully!")

        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                print("\nThis email is already registered!")
            else:
                print("\nError:", error)

        finally:
            connection.close()

    def view_members(self):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()

        if not members:
            print("\nNo members registered.")
        else:
            print("\n===== LIBRARY MEMBERS =====")

            for member in members:
                print(f"""
ID: {member[0]}
Name: {member[1]}
Email: {member[2]}
-------------------------
""")

        connection.close()

    def borrow_book(self, book_id, member_id):
        connection = connect_db()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT available_copies
                FROM books
                WHERE id = ?
            """, (book_id,))

            book = cursor.fetchone()

            if book is None:
                print("\nBook ID not found.")
                return

            if book[0] <= 0:
                print("\nNo copies available.")
                return

            cursor.execute("""
                SELECT id FROM members WHERE id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if member is None:
                print("\nMember ID not found.")
                return

            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=14)

            cursor.execute("""
                INSERT INTO loans
                (book_id, member_id, borrow_date, due_date)
                VALUES (?, ?, ?, ?)
            """, (
                book_id,
                member_id,
                borrow_date.isoformat(),
                due_date.isoformat()
            ))

            cursor.execute("""
                UPDATE books
                SET available_copies = available_copies - 1
                WHERE id = ?
            """, (book_id,))

            connection.commit()

            print("\nBook borrowed successfully!")
            print("Borrow Date:", borrow_date)
            print("Due Date:", due_date)

        except Exception as error:
            connection.rollback()
            print("\nError:", error)

        finally:
            connection.close()

    def return_book(self, loan_id):
        connection = connect_db()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT book_id, return_date
                FROM loans
                WHERE id = ?
            """, (loan_id,))

            loan = cursor.fetchone()

            if loan is None:
                print("\nLoan ID not found.")
                return

            if loan[1] is not None:
                print("\nThis book has already been returned.")
                return

            return_date = date.today().isoformat()

            cursor.execute("""
                UPDATE loans
                SET return_date = ?
                WHERE id = ?
            """, (return_date, loan_id))

            cursor.execute("""
                UPDATE books
                SET available_copies = available_copies + 1
                WHERE id = ?
            """, (loan[0],))

            connection.commit()

            print("\nBook returned successfully!")

        except Exception as error:
            connection.rollback()
            print("\nError:", error)

        finally:
            connection.close()

    def view_borrowed_books(self):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                loans.id,
                books.title,
                members.name,
                loans.borrow_date,
                loans.due_date
            FROM loans
            JOIN books ON loans.book_id = books.id
            JOIN members ON loans.member_id = members.id
            WHERE loans.return_date IS NULL
        """)

        loans = cursor.fetchall()

        if not loans:
            print("\nNo books are currently borrowed.")
        else:
            print("\n===== BORROWED BOOKS =====")

            for loan in loans:
                print(f"""
Loan ID: {loan[0]}
Book: {loan[1]}
Member: {loan[2]}
Borrow Date: {loan[3]}
Due Date: {loan[4]}
-------------------------
""")

        connection.close()

    def view_overdue_books(self):
        connection = connect_db()
        cursor = connection.cursor()

        today = date.today().isoformat()

        cursor.execute("""
            SELECT
                loans.id,
                books.title,
                members.name,
                loans.due_date
            FROM loans
            JOIN books ON loans.book_id = books.id
            JOIN members ON loans.member_id = members.id
            WHERE loans.return_date IS NULL
            AND loans.due_date < ?
        """, (today,))

        overdue = cursor.fetchall()

        if not overdue:
            print("\nNo overdue books!")
        else:
            print("\n===== OVERDUE BOOKS =====")

            for loan in overdue:
                print(f"""
Loan ID: {loan[0]}
Book: {loan[1]}
Member: {loan[2]}
Due Date: {loan[3]}
-------------------------
""")

        connection.close()