# SubtitleTranslator V12 (English Edition)
SubtitleTranslator V12 is a powerful Windows tool for automatically translating subtitle files.  
It supports DeepL and multi‑threaded Google Translate, automatically detects subtitle formats and source language, and includes a modern GUI with progress bar, ETA, and a stop button.

## ✨ Key Features

### 🔍 Automatic Language Detection (NEW in V12)
The app analyzes a sample of subtitle lines and displays:
- Detected language code (e.g., `en`)
- Full language name (e.g., `English`)

Works for:
- SRT  
- VTT  
- ASS  
- SSA  

### 🧠 Automatic Subtitle Type Detection
The app automatically recognizes:
- `.srt` → SRT  
- `.vtt` → VTT  
- `.ass` → ASS  
- `.ssa` → SSA  

### ⚡ Multi‑Threaded Google Translate
- Up to **10× faster** than DeepL  
- No API key required  
- Ideal for large subtitle files  
- Parallel translation using ThreadPoolExecutor  

### 🔑 DeepL Support
- Uses your own DeepL API key  
- High‑quality translations  
- Full error handling  

### 🎨 ASS/SSA Support
- Only the **text** is translated  
- Styles, formatting, and timing remain intact  

### ⏱ ETA (Estimated Time Remaining)
Shows real‑time progress:
Google: 120/800 — ETA 01:42


### 🛑 Stop Button
- Interrupt translation at any time  
- Threads stop safely  
- No corrupted output files  

### 🖥 Modern GUI
- Progress bar  
- Status updates  
- Detected language display  
- Stop button  
- DeepL key storage  
- File picker dialog  

---

## 📁 Supported Formats
- `.srt`
- `.vtt`
- `.ass`
- `.ssa`

---

## 📦 Installation

### 1. Install requirements
Make sure Python 3.10+ is installed.

pip install -r requirements.txt

### 2. Run the app

python SubtitleTranslatorV12_EN.py

## 🔧 DeepL API Key
If you want to use DeepL:

1. Visit https://www.deepl.com  
2. Create an API key  
3. Enter it in the GUI  
4. Click **Save API key**

Google Translate works without a key.

---

## 📁 Project Structure
/
├── SubtitleTranslatorV12_EN.py
├── README.md
├── LICENSE
└── requirements.txt

---

## 📝 License
This project is licensed under the MIT License.  
See `LICENSE` for details.

---

## ❤️ Credits
Created by Frank & Copilot — a collaboration that keeps getting smarter.
