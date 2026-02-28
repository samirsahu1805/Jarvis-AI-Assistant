# Jarvis-AI-Assistant
Jarvis is a Python-based AI voice assistant that uses speech recognition, translation, Selenium automation, and environment-based configuration to execute commands, interact with the web, and respond intelligently in real time.
# JARVIS – AI Voice Assistant 🤖

JARVIS is a Python-based AI voice assistant designed to perform automated tasks, interact with the web, and respond intelligently to user commands using speech recognition and browser automation.

---

## 🚀 Features

* 🎙️ Voice command recognition
* 🌐 Web automation using Selenium
* 🌍 Multi-language input support
* 🔁 Real-time command execution
* 🔐 Secure configuration using environment variables
* 🧠 Modular and extensible project structure

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Speech Recognition (Web Speech API)**
* **Selenium WebDriver**
* **webdriver-manager**
* **mtranslate**
* **HTML + JavaScript** (for voice input)
* **dotenv** for environment management

---

## 📁 Project Structure

```
Jarvis/
│── Data/
│   └── Voice.html
│── src/
│   └── main.py
│── .env
│── requirements.txt
│── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/jarvis.git
cd jarvis
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
InputLanguage=en
```

---

## ▶️ How to Run

```bash
python src/main.py
```

Ensure Google Chrome is installed. ChromeDriver will be handled automatically.

---

## 🧩 How It Works (High-Level)

1. Voice input is captured via a browser-based HTML interface.
2. Speech is converted to text using Web Speech API.
3. Python processes the command and translates if required.
4. Selenium automates browser actions based on the command.
5. JARVIS responds or executes tasks in real time.

---

## 🧪 Use Cases

* Personal voice-controlled automation
* Browser task automation
* Learning project for Selenium + Voice AI
* Foundation for advanced AI assistants

---

## 🔮 Future Improvements

* Integrate NLP models (GPT / LLMs)
* Add wake-word detection
* Support background execution
* Desktop application interface
* Plugin-based command system

---

## ⚠️ Disclaimer

This project is for educational and experimental purposes. Some automated actions may violate website terms if misused.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👤 Author

**Sammy**
Engineer | Python & Automation Enthusiast

---

⭐ If you find this project useful, consider giving it a star!
