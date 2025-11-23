import json
import logging
from pathlib import Path

# -------------------- Logging Configuration -------------------- #
LOG_FILE = "library.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -------------------- Book Class -------------------- #
class Book:
    """
    Represents a single book in the library.
    """

    def _init_(self, title: str, author: str, isbn: str, status: str = "available"):
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        # normalize status
        if status.lower() not in ("available", "issued"):
            status = "available"
        self.status = status.lower()

    def _str_(self) -> str:
        return (
            f"Title : {self.title}\n"
            f"Author: {self.author}\n"
            f"ISBN  : {self.isbn}\n"
            f"Status: {self.status.capitalize()}"
        )

    def to_dict(self) -> dict:
        """
        Convert Book object to a dictionary for JSON serialization.
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """
        Create a Book object from a dictionary.
        """
        return cls(
            title=data.get("title", ""),
            author=data.get("author", ""),
            isbn=data.get("isbn", ""),
            status=data.get("status", "available"),
        )

    def issue(self) -> bool:
        """
        Mark the book as issued.
        Returns True if successful, False if already issued.
        """
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self) -> bool:
        """
        Mark the book as available.
        Returns True if successful, False if already available.
        """
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self) -> bool:
        """
        Check if the book is available.
        """
        return self.status == "available"


# -------------------- Library Inventory Class -------------------- #
class LibraryInventory:
    """
    Manages a collection of Book objects and handles file persistence.
    """

    def _init_(self, data_file: str = "catalog.json"):
        self.data_file = Path(data_file)
        self.books: list[Book] = []
        self.load_from_file()

    # ---------- File Handling ---------- #
    def load_from_file(self) -> None:
        """
        Load books from a JSON file.
        Handles missing or corrupted files using try-except.
        """
        if not self.data_file.exists():
            logging.info(f"Data file {self.data_file} not found. Starting with empty catalog.")
            self.books = []
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book.from_dict(item) for item in data]
            logging.info("Catalog loaded successfully from file.")
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error while loading catalog: {e}")
            print("Warning: Catalog file is corrupted. Starting with an empty catalog.")
            self.books = []
        except OSError as e:
            logging.error(f"OS error while loading catalog: {e}")
            print("Error reading catalog file. Starting with an empty catalog.")
            self.books = []

    def save_to_file(self) -> None:
        """
        Save current catalog to JSON file.
        """
        try:
            with self.data_file.open("w", encoding="utf-8") as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
            logging.info("Catalog saved successfully to file.")
        except OSError as e:
            logging.error(f"OS error while saving catalog: {e}")
            print("Error: Could not save catalog to file.")

    # ---------- Book Operations ---------- #
    def add_book(self, book: Book) -> None:
        """
        Add a new book to the catalog.
        """
        if self.search_by_isbn(book.isbn):
            print("A book with this ISBN already exists. Not adding duplicate.")
            logging.info(f"Attempted to add duplicate ISBN: {book.isbn}")
            return
        self.books.append(book)
        logging.info(f"Book added: {book.title} (ISBN: {book.isbn})")

    def search_by_title(self, title: str) -> list[Book]:
        """
        Return a list of books whose title contains the search string (case-insensitive).
        """
        title_lower = title.lower()
        return [book for book in self.books if title_lower in book.title.lower()]

    def search_by_isbn(self, isbn: str) -> Book | None:
        """
        Return the book with the exact ISBN, or None if not found.
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self) -> None:
        """
        Display all books in the catalog.
        """
        if not self.books:
            print("No books in the catalog.")
            return
        print("\n--- All Books in Catalog ---")
        for idx, book in enumerate(self.books, start=1):
            print(f"\nBook #{idx}")
            print(book)
        print("\n-----------------------------")

    def issue_book(self, isbn: str) -> None:
        """
        Issue a book by ISBN.
        """
        book = self.search_by_isbn(isbn)
        if not book:
            print("Book not found.")
            logging.info(f"Attempt to issue non-existent book ISBN: {isbn}")
            return

        if book.issue():
            print(f"Book '{book.title}' issued successfully.")
            logging.info(f"Book issued: {book.title} (ISBN: {book.isbn})")
        else:
            print("Book is already issued.")
            logging.info(f"Attempt to issue already issued book ISBN: {isbn}")

    def return_book(self, isbn: str) -> None:
        """
        Return a book by ISBN.
        """
        book = self.search_by_isbn(isbn)
        if not book:
            print("Book not found.")
            logging.info(f"Attempt to return non-existent book ISBN: {isbn}")
            return

        if book.return_book():
            print(f"Book '{book.title}' returned successfully.")
            logging.info(f"Book returned: {book.title} (ISBN: {book.isbn})")
        else:
            print("Book is already available.")
            logging.info(f"Attempt to return already available book ISBN: {isbn}")


# -------------------- CLI Helper Functions -------------------- #
def get_non_empty_input(prompt: str) -> str:
    """
    Repeatedly ask the user for input until a non-empty string is given.
    """
    while True:
        try:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty. Please try again.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Returning to menu.")
            return ""


def get_menu_choice() -> int:
    """
    Get a valid menu choice from the user.
    """
    while True:
        try:
            choice_str = input("Enter your choice: ").strip()
            choice = int(choice_str)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number (1-6).")
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Exiting.")
            return 6  # Treat as Exit


def handle_add_book(inventory: LibraryInventory) -> None:
    print("\n--- Add Book ---")
    title = get_non_empty_input("Enter title: ")
    if not title:
        return
    author = get_non_empty_input("Enter author: ")
    if not author:
        return
    isbn = get_non_empty_input("Enter ISBN: ")
    if not isbn:
        return

    new_book = Book(title=title, author=author, isbn=isbn)
    inventory.add_book(new_book)
    print("Book added to catalog.")


def handle_issue_book(inventory: LibraryInventory) -> None:
    print("\n--- Issue Book ---")
    isbn = get_non_empty_input("Enter ISBN of the book to issue: ")
    if not isbn:
        return
    inventory.issue_book(isbn)


def handle_return_book(inventory: LibraryInventory) -> None:
    print("\n--- Return Book ---")
    isbn = get_non_empty_input("Enter ISBN of the book to return: ")
    if not isbn:
        return
    inventory.return_book(isbn)


def handle_view_all(inventory: LibraryInventory) -> None:
    print("\n--- View All Books ---")
    inventory.display_all()


def handle_search(inventory: LibraryInventory) -> None:
    print("\n--- Search Books ---")
    print("1. Search by Title")
    print("2. Search by ISBN")
    try:
        choice_str = input("Enter your choice: ").strip()
        choice = int(choice_str)
    except ValueError:
        print("Invalid input. Returning to main menu.")
        return
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled. Returning to main menu.")
        return

    if choice == 1:
        title = get_non_empty_input("Enter title or part of title: ")
        if not title:
            return
        results = inventory.search_by_title(title)
        if not results:
            print("No books found with that title.")
        else:
            print(f"\nFound {len(results)} book(s):")
            for book in results:
                print("\n" + str(book))
    elif choice == 2:
        isbn = get_non_empty_input("Enter ISBN: ")
        if not isbn:
            return
        book = inventory.search_by_isbn(isbn)
        if not book:
            print("No book found with that ISBN.")
        else:
            print("\nBook found:")
            print(book)
    else:
        print("Invalid choice. Returning to main menu.")


# -------------------- Main Menu Loop -------------------- #
def main():
    inventory = LibraryInventory()

    print("======================================")
    print("   Library Inventory Manager (CLI)    ")
    print("======================================")

    while True:
        print("\nMain Menu:")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Books")
        print("6. Save & Exit")

        choice = get_menu_choice()

        if choice == 1:
            handle_add_book(inventory)
        elif choice == 2:
            handle_issue_book(inventory)
        elif choice == 3:
            handle_return_book(inventory)
        elif choice == 4:
            handle_view_all(inventory)
        elif choice == 5:
            handle_search(inventory)
        elif choice == 6:
            print("Saving catalog and exiting...")
            inventory.save_to_file()
            print("Goodbye!")
            break


if NameError == "_main_":
    try:
        main()
    except Exception as e:
        # catch any unhandled exception to avoid crashing without a message
        logging.error(f"Unhandled exception in main: {e}")
        print("An unexpected error occurred. Please check the log file for details.")
        