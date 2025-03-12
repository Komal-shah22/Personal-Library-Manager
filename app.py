
import os
import json
import streamlit as st # type: ignore
from dotenv import load_dotenv, find_dotenv # type: ignore
from litellm import completion # type: ignore


# Load API key
_: bool = load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# File to store library data
LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Get AI-generated book summary & cover
def get_book_info(title):
    prompt = f"""
    1. Summarize the book '{title}' in a few sentences.
    2. Generate a book cover image description for '{title}', focusing on a visually appealing and relevant theme.
    Return both summary and image description.
    """
    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}],
            api_key=GEMINI_API_KEY
        )
        if "choices" in response and response["choices"]:
            content = response["choices"][0].get("message", {}).get("content", "").strip()
            parts = content.split("\n\n")
            summary = parts[0] if len(parts) > 0 else "No summary available."
            image_description = parts[1] if len(parts) > 1 else "No image description available."
            return summary, image_description
        return "Could not generate summary.", "Could not generate image description."
    except Exception as e:
        return f"Error: {str(e)}", f"Error: {str(e)}"

def get_book_cover(title):
    search_query = f"{title} book cover"
    google_search_url = f"https://www.google.com/search?tbm=isch&q={search_query.replace(' ', '+')}"
    return google_search_url

def get_read_book_link(title):
    search_query = f"{title} read online"
    google_books_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    return google_books_url

# Streamlit UI
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

# Load library
library = load_library()

# Sidebar menu
menu = st.sidebar.radio("📌 Menu", ["📖 Add Book", "❌ Remove Book", "🔎 Search Book", "📚 Display All Books", "📊 Statistics"])

if menu == "📖 Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("Enter book title:", key="add_title")
    author = st.text_input("Enter author name:")
    year = st.number_input("Enter publication year:", min_value=0, max_value=2100, step=1)
    genre = st.text_input("Enter book genre:")
    read_status = st.radio("Have you read this book?", ["Yes", "No"]) == "Yes"

    if st.button("Add Book"):
        if not title.strip():
            st.error("❌ Please enter a book title!")
        else:
            new_book = {
                "title": title.strip(),
                "author": author.strip(),
                "year": year,
                "genre": genre.strip(),
                "read": read_status
            }
            library.append(new_book)
            save_library(library)
            st.success(f"✅ '{title}' added to your library!")

if menu == "❌ Remove Book":
    st.subheader("❌ Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove:", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"✅ '{book_to_remove}' removed successfully!")
    else:
        st.warning("No books in library.")

if menu == "🔎 Search Book":
    st.subheader("🔎 Search for a Book")
    search_option = st.radio("Search by:", ["Title", "Author"])
    search_query = st.text_input("Enter search query:")

    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book[search_option.lower()].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
                st.markdown("---")
        else:
            st.warning("No matching books found. Fetching AI-generated details...")
            with st.spinner("Fetching book details..."):
                summary, image_description = get_book_info(search_query)
            st.subheader("📜 AI-Generated Book Summary")
            st.info(summary)

            st.subheader("🎨 AI-Generated Book Cover Description")
            st.write(image_description)

            cover_image_url = get_book_cover(search_query)
            st.markdown(f"[🔍 Click here to see book cover images]({cover_image_url})")

            read_link = get_read_book_link(search_query)
            st.markdown(f"[📖 Read this book online]({read_link})")

if menu == "📚 Display All Books":
    st.subheader("📚 Your Library")
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
            
            if st.button(f"📜 Get Summary & Cover for '{book['title']}'", key=book['title']):
                with st.spinner("Fetching summary & image description..."):
                    summary, image_description = get_book_info(book['title'])
                st.subheader("📜 Book Summary")
                st.info(summary)

                st.subheader("🎨 Book Cover Image Description")
                st.write(image_description)

                cover_image_url = get_book_cover(book['title'])
                st.markdown(f"[🔍 Click here to see book cover images]({cover_image_url})")
            
            read_link = get_read_book_link(book['title'])
            st.markdown(f"[📖 Read this book online]({read_link})")
            
            st.markdown("---")
    else:
        st.warning("No books in library.")

if menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books}")
    st.write(f"📈 **Percentage Read:** {percentage_read:.2f}%")

    if total_books > 0:
        if st.button("📚 Show All Books"):
            st.subheader("📚 All Books")
            for book in library:
                st.write(f"📖 **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
                st.markdown("---")








