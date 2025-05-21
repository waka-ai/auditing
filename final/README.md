# Code Auditing Tool Web GUI

This project adds a modern, cozy web-based GUI to your Python Code Auditing Tool using **Flask** (backend API) and **React** (frontend).

---

## 📁 Directory Structure

```
your-project/
│
├─ code_auditing_tool_with_reporting.py
├─ vuln_to_cve_mapping.json
├─ vuln_mitigations.json
│
├─ web-backend/
│   ├─ app.py
│   ├─ requirements.txt
│
└─ web-frontend/
    ├─ package.json
    ├─ public/
    │   └─ index.html
    └─ src/
        ├─ App.js
        ├─ App.css
        └─ index.js
```

## 🚀 Quick Start

### 1. Backend (Flask API)

```bash
cd web-backend
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows
pip install -r requirements.txt
python app.py
```

- The backend will run at `http://localhost:5000/`
- Make sure `code_auditing_tool_with_reporting.py` is in the parent directory.

### 2. Frontend (React App)

```bash
cd web-frontend
npm install
npm start
```

- The React app will open at `http://localhost:3000/`
- Make sure the backend (`app.py`) is running for API calls.

### 3. Usage

1. Open the React app in your browser.
2. Select a Python `.py` file to audit.
3. Click **Run Audit**.
4. View the results in a beautiful, cozy table.
5. Download or copy the HTML report as needed.

---

## 🛠️ How it Works

- The React frontend lets you upload a Python file.
- The Flask backend receives the file, runs your auditing tool, and returns the HTML report.
- The frontend displays the results instantly.

---

## 💡 Customization

- For directory scans or advanced features, extend the backend and frontend logic as desired.
- The code is well-commented for easy understanding and modification.

---

## 🧑‍💻 Authors & Credits

- Inspired by the original code-auditing-tool by Group 7.
- Web GUI by [waka-ai](https://github.com/waka-ai) with Copilot’s assistance.

---

## 📸 Screenshots

![UI Preview](screenshots/html_report.jpeg)
![Terminal Output](screenshots/terminal_output.jpeg)

---

## 🔒 Disclaimer

This tool is for authorized auditing only. Use responsibly!
