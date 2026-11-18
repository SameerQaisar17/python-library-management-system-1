from database import create_tables
from library import LibraryManager


def main():
    create_tables()
    library = LibraryManager()

    while True:
        print("""
========== LIBRARY MANAGEMENT SYSTEM ==========

1. Add Book
2. View All Books
3. Register Member
4. View Members
5. Borrow Book
6. Return Book
7. View Borrowed Books
8. View Overdue Books
9. Exit

================================================
""")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            print("\n===== ADD BOOK =====")

            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()

            try:
                copies = int(input("Enter number of copies: "))

                if not title or not author or copies <= 0:
                    print("\nEnter valid book details.")
                else:
                    library.add_book(title, author, copies)

            except ValueError:
                print("\nPlease enter a valid number.")

        elif choice == "2":
            library.view_books()

        elif choice == "3":
            print("\n===== REGISTER MEMBER =====")

            name = input("Enter member name: ").strip()
            email = input("Enter email address: ").strip()

            if not name or not email:
                print("\nName and email are required.")
            else:
                library.register_member(name, email)

        elif choice == "4":
            library.view_members()

        elif choice == "5":
            print("\n===== BORROW BOOK =====")

            try:
                book_id = int(input("Enter book ID: "))
                member_id = int(input("Enter member ID: "))

                library.borrow_book(book_id, member_id)

            except ValueError:
                print("\nPlease enter valid IDs.")

        elif choice == "6":
            print("\n===== RETURN BOOK =====")

            try:
                loan_id = int(input("Enter loan ID: "))
                library.return_book(loan_id)

            except ValueError:
                print("\nPlease enter a valid loan ID.")

        elif choice == "7":
            library.view_borrowed_books()

        elif choice == "8":
            library.view_overdue_books()

        elif choice == "9":
            print("\nThank you for using the Library Management System!")
            break

        else:
            print("\nInvalid option! Choose between 1 and 9.")


if __name__ == "__main__":
    main()