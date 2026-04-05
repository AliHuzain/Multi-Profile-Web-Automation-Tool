# Multi-Profile-Web-Automation-Tool

A desktop-based automation tool built with Python that enables users to manage multiple browser sessions and perform repeated web interactions through a clean graphical interface.

## 🚀 Features

* Multi-profile browser sessions (isolated cookies & storage)
* Automated button interaction on any website
* Persistent sessions (auto-save & reload)
* Simple and modern GUI (CustomTkinter)
* Hotkey control (F8 to start/stop all profiles)
* Configurable target URL and button text
* Real-time logging system

## 🛠️ Tech Stack

* Python
* Playwright (browser automation)
* CustomTkinter (GUI)
* Pynput (keyboard listener)

## ⚙️ Configuration

Before running the tool, update the following variables in the script:

```python
TARGET_URL = "https://example.com"
BUTTON_TEXT = "Click me"
CLICK_INTERVAL = 65.0
```

* `TARGET_URL`: The website you want to automate
* `BUTTON_TEXT`: The visible text of the button to click
* `CLICK_INTERVAL`: Time between actions (in seconds)

## ▶️ How It Works

1. Launch the application
2. Click **"Add Profile"** to create a new session
3. Click **"Run"** on a profile
4. The browser will open and navigate to the target URL
5. The tool will search for the button and click it automatically
6. Sessions are saved and reused

## 🎮 Controls

* **F8** → Start / Stop all profiles instantly

## 📂 Session Management

Each profile has its own session stored locally:

```
/profiles/Profile_1/state.json
/profiles/Profile_2/state.json
```

This allows:

* Staying logged in
* Running multiple accounts independently

## ⚠️ Disclaimer

This tool is intended for:

* Testing
* Automation workflows
* Educational purposes

Make sure to comply with the terms of service of any website you interact with.

## 📦 Installation

```bash
pip install playwright customtkinter pynput
playwright install
```

## ▶️ Run the App

```bash
python main.py
```

## 📌 Future Improvements

* Scheduler (run at specific times)
* Proxy support
* Headless mode toggle
* Advanced element selectors (CSS/XPath)

---

## 👨‍💻 Author

I'm Ali Huzain, a Software Engineer who developed this project to explore browser automation, multi-session management, and GUI-based tooling.
