
# Personal Library Manager

## 📌 Overview
The **Personal Library Manager** is a Streamlit-based web application that allows users to efficiently manage their personal book collection. It includes features for adding, searching, and removing books, as well as AI-generated summaries and cover image descriptions using the Gemini API.

## 🚀 Features
- 📖 Add, remove, and search books
- 🔍 AI-generated book summaries and cover descriptions
- 📚 View and manage book details
- 📊 Library statistics (total books, read books percentage)
- 🎨 External book cover search and online reading links

## 🏗️ Project Setup
This project is initialized using `uv` for environment and dependency management.

### Prerequisites
Ensure you have **Python 3.12** installed on your system.

### Installation Steps
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/library-manager.git
   cd library-manager
   ```

2. **Initialize the environment using `uv`:**
   ```sh
   uv init
   uv add dependencies name
   ```

3. **Set up environment variables:**
   Create a `.env` file and add your Gemini API key:
   ```sh
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application:**
   ```sh
   uv pip install streamlit
   streamlit run app.py
   ```


## 📌 Dependencies
This project uses the following dependencies:
- `streamlit` - UI framework
- `litellm` - AI API integration
- `python-dotenv` - Environment variable management

Install dependencies using:
```sh
uv add command
```

## 🤖 AI Integration
This project uses the **Gemini API** to generate book summaries and cover descriptions. The AI call is made via `litellm`:
```python
response = completion(
    model="gemini/gemini-1.5-flash",
    messages=[{"role": "user", "content": prompt}],
    api_key=os.getenv("GEMINI_API_KEY")
)
```

## 📜 License
This project is licensed under the MIT License.

## 📞 Contact
For any queries or contributions, feel free to reach out:
📧 Email: komalfareed93@gmail.com
GitHub: [komal Shah](https://github.com/Komal-shah22)

"# Personal-Library-Manager" 
