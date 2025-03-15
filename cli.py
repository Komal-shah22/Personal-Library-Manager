import sys
import time
import itertools
import threading
import json

# File to save library
LIBRARY_FILE = "library.json"

# Initialize library
library = []

# 🌟 1. Welcome ASCII Art
def print_welcome():
    print("\033[94m")
    print("📚" * 10)
    print("  1PERSONAL LIBRARY MANAGER")
    print("📚" * 10)
    print("\033[0m")

# ⏳ 2. Smooth Typing Effect
def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# 🔄 3. Loading Animation
def loading_animation(message="Loading", duration=3):
    chars = itertools.cycle(["⠏", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    for _ in range(duration * 10):
        sys.stdout.write(f"\r\033[93m{message} {next(chars)}\033[0m")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r\033[92m✔ Done! \033[0m")

# 📊 4. Progress Bar for Statistics
def progress_bar(percentage, length=30):
    filled = int(length * percentage / 100)
    bar = "█" * filled + "-" * (length - filled)
    print(f"\033[92m[{bar}] {percentage:.2f}% Read\033[0m")

# 🔍 5. Blinking Search Effect
def blinking_text(text, duration=3):
    stop_event = threading.Event()
    
    def blink():
        visible = True
        while not stop_event.is_set():
            sys.stdout.write(f"\r\033[93m{text if visible else ' ' * len(text)}\033[0m")
            sys.stdout.flush()
            time.sleep(0.5)
            visible = not visible

    thread = threading.Thread(target=blink)
    thread.start()
    time.sleep(duration)
    stop_event.set()
    thread.join()
    print(f"\r\033[92m{text}\033[0m")

# 📌 6. Add a Book
def add_book():
    title = input("\033[94m📖 Enter the book title:\033[0m ").strip()
    author = input("\033[94m✍️ Enter the author name:\033[0m ").strip()
    year = input("\033[94m📅 Enter the publication year:\033[0m ").strip()
    genre = input("\033[94m📚 Enter the genre:\033[0m ").strip()
    read_status = input("\033[94m✅ Have you read this book? (yes/no):\033[0m ").strip().lower()

    book = {
        "Title": title,
        "Author": author,
        "Year": int(year),
        "Genre": genre,
        "Read": True if read_status == "yes" else False
    }
    library.append(book)
    slow_print("\033[92m✔ Book added successfully! 📖\033[0m")

# ❌ 7. Remove a Book
def remove_book():
    title = input("\033[94m🗑 Enter the title of the book to remove:\033[0m ").strip()
    for book in library:
        if book["Title"].lower() == title.lower():
            library.remove(book)
            slow_print("\033[91m✔ Book removed successfully! ❌\033[0m")
            return
    slow_print("\033[91m⚠ Book not found! 📕\033[0m")

# 🔍 8. Search for a Book
def search_book():
    choice = input("\033[94m🔍 Search by: 1) Title 2) Author: \033[0m").strip()
    term = input("\033[94m🔎 Enter search term:\033[0m ").strip().lower()
    blinking_text("Searching...")

    results = [book for book in library if (book["Title"].lower() == term or book["Author"].lower() == term)]
    
    if results:
        slow_print("\n\033[92m✔ Found Matching Books:\033[0m")
        for idx, book in enumerate(results, 1):
            status = "✅ Read" if book["Read"] else "📖 Unread"
            slow_print(f"{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
    else:
        slow_print("\033[91m⚠ No books found!\033[0m")

# 📜 9. Display All Books
def display_books():
    if not library:
        slow_print("\033[91m⚠ Library is empty! 📚\033[0m")
        return
    
    slow_print("\033[92m📚 Your Library:\033[0m")
    for idx, book in enumerate(library, 1):
        status = "✅ Read" if book["Read"] else "📖 Unread"
        slow_print(f"{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")

# 📊 10. Display Statistics
def display_statistics():
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    slow_print(f"\033[94m📚 Total books: {total_books}\033[0m")
    progress_bar(percentage_read)

# 💾 11. Save Library to File
def save_library():
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file)
    loading_animation("Saving library")

# 📂 12. Load Library from File
def load_library():
    global library
    try:
        with open(LIBRARY_FILE, "r") as file:
            library = json.load(file)
        loading_animation("Loading library")
    except (FileNotFoundError, json.JSONDecodeError):
        library = []

# 📌 13. Main Menu
def main():
    load_library()
    print_welcome()

    while True:
        print("\n\033[94m📌 Menu:\033[0m")
        print("1️⃣ Add a book")
        print("2️⃣ Remove a book")
        print("3️⃣ Search for a book")
        print("4️⃣ Display all books")
        print("5️⃣ Display statistics")
        print("6️⃣ Exit")

        choice = input("\n\033[94m🎯 Enter your choice:\033[0m ").strip()
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            save_library()
            slow_print("\033[92m✔ Library saved! Goodbye! 👋\033[0m")
            break
        else:
            slow_print("\033[91m⚠ Invalid choice, try again! 🚨\033[0m")

# Run the program
if __name__ == "__main__":
    main()
