# 🚀 cutieAPI - Your Friendly Command-Line API Client 🚀

cutieAPI is a Python-based, interactive command-line tool designed to make API testing and interaction easy and enjoyable, right from your terminal! It's built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output and `requests` for robust HTTP communication.

Think of it as a lightweight, terminal-first companion for your API development workflow, similar in spirit to tools like Postman or Insomnia, but living entirely in your console.

## ✨ Features

*   **Interactive Request Building:** Guided prompts for HTTP method, URL, headers, query parameters, and body.
*   **Multiple Body Types:**
    *   JSON (with multi-line input and syntax highlighting)
    *   Form Data (`application/x-www-form-urlencoded`)
    *   Raw Text (for XML, plain text, etc.)
    *   File Uploads (`multipart/form-data`) including text fields.
*   **Pretty Output:**
    *   Colorized and formatted display of request and response details.
    *   Syntax highlighting for JSON and HTML responses.
    *   Clear status codes, headers, and timing information.
*   **Request History:** Automatically saves recent requests for quick re-runs.
*   **Saved Requests:** Name and save frequently used request configurations to files.
*   **Environment Variables:** Define placeholders (e.g., `{{base_url}}`, `{{auth_token}}`) and manage them within the tool for easy switching between environments or reusing common values.
*   **Bearer Token Helper:** Quickly add or update `Authorization: Bearer <token>` headers.
*   **Save Response to File:** Option to save the raw response body directly to a local file.
*   **Cross-Platform:** Runs wherever Python and Rich are supported (Linux, macOS, Windows).

## 🛠️ Installation

1.  **Prerequisites:**
    *   Python 3.8+ (though it might work on slightly older versions, 3.8+ is recommended)
    *   `pip` (Python package installer)

2.  **Clone the Repository (Optional, if you have the `main.py` file directly, skip this):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/api-buddy.git # Replace YOUR_USERNAME/api-buddy
    cd api-buddy
    ```

3.  **Install Dependencies:**
    API Buddy relies on `requests` and `rich`. You can install them using pip:
    ```bash
    pip install requests rich
    ```
    Alternatively, if you plan to manage dependencies for a project, consider using a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install requests rich
    ```

## 🚀 How to Use

1.  **Run the Script:**
    Navigate to the directory containing `main.py` (or `api_buddy.py` if you renamed it) and run:
    ```bash
    python main.py
    ```

2.  **Follow the Interactive Prompts:**
    API Buddy will guide you through configuring your API request:

    *   **Start with?**:
        *   `new`: Create a new request from scratch.
        *   `history`: View and re-run a request from your history.
        *   `load`: Load a previously saved request configuration.
        *   `env`: Manage your environment variables (e.g., add `{{base_url}}`).
        *   `quit`: Exit the application.

    *   **HTTP Method**: Choose from GET, POST, PUT, DELETE, etc.
    *   **URL**: Enter the full API endpoint URL. You can use environment variables like `{{base_url}}/users`.
    *   **Query Parameters**: Add key-value pairs for URL query parameters.
    *   **Headers**: Add custom request headers (e.g., `Content-Type: application/json`, `X-API-Key: yourkey`).
        *   **Bearer Token Helper**: A shortcut to add/update the `Authorization: Bearer <token>` header.
    *   **Body Type (for POST, PUT, PATCH):**
        *   `json`: Paste your JSON payload. Use Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) to finish multi-line input.
        *   `form`: Enter `application/x-www-form-urlencoded` data as key=value pairs.
        *   `file`: For `multipart/form-data`. You can add both text fields (key=value) and file uploads (provide field name and local file path).
        *   `raw`: Paste any raw text body (e.g., XML).
        *   `none`: Send no body.

3.  **View the Response:**
    After the request is sent, API Buddy will display:
    *   Request details (what was sent).
    *   Response status code and reason.
    *   Response duration.
    *   Response headers.
    *   Response body (pretty-printed and syntax-highlighted for JSON/HTML).

4.  **Post-Request Actions:**
    *   **Save Response Body**: You'll be asked if you want to save the received body to a local file.
    *   **Save Request Configuration**: You'll be asked if you want to save the current request setup (URL, headers, body structure, etc.) for later use via the `load` option.
    *   **Make Another Request?**: Loop back to make more requests or quit.

**Data Storage:**
*   **History (`~/.api_buddy_history.json`):** Automatically stores the last 50 requests (configurable in code).
*   **Saved Requests (`~/.api_buddy_saved_requests/`):** Stores named request configurations as JSON files in this directory in your user's home folder.

## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, new features, or documentation improvements, please feel free to:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or fix (`git checkout -b feature/your-feature-name`).
3.  **Make your changes.**
4.  **Test your changes thoroughly.**
5.  **Commit your changes** (`git commit -am 'Add some feature'`).
6.  **Push to the branch** (`git push origin feature/your-feature-name`).
7.  **Create a new Pull Request.**

If you encounter any bugs or have feature suggestions, please open an issue on GitHub.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE.md). (You'll need to create a `LICENSE.md` file with the MIT license text if you want this).

---

Happy API Bashing! 🎉
