🎬 SubtitleTranslator V12 (English Edition)
SubtitleTranslator V12 is a powerful Windows tool for automatically translating subtitle files.
It supports DeepL and multi‑threaded Google Translate, automatically detects subtitle formats and source language, and includes a modern GUI with progress bar, ETA, and a stop button.

📸 Screenshot
[Het resultaat is niet veilig om weer te geven. Laten we het anders aanpakken en iets anders proberen!]

📥 Downloads
🔧 Windows Installer (.exe)
Recommended for most users.

Creates Start Menu shortcut

Creates Desktop shortcut

Uses custom icon

Automatically launches after installation

👉 Download:  
https://github.com/UtCollector/SubtitleTranslator-V12/releases/latest

📦 Portable ZIP
No installation required.

Download the ZIP

Extract it

Double‑click the shortcut

Done

👉 Download:  
https://github.com/UtCollector/SubtitleTranslator-V12/releases/latest

✨ Key Features
🔍 Automatic Language Detection (NEW in V12)
The app analyzes a sample of subtitle lines and displays:

Detected language code (e.g., en)

Full language name (e.g., English)

Works for:

SRT

VTT

ASS

SSA

🧠 Automatic Subtitle Type Detection
The app automatically recognizes:

.srt → SRT

.vtt → VTT

.ass → ASS

.ssa → SSA

⚡ Multi‑Threaded Google Translate
Up to 10× faster than DeepL

No API key required

Ideal for large subtitle files

Parallel translation using ThreadPoolExecutor

🔑 DeepL Support
Uses your own DeepL API key

High‑quality translations

Full error handling

🎨 ASS/SSA Support
Only the text is translated

Styles, formatting, and timing remain intact

⏱ ETA (Estimated Time Remaining)
Shows real‑time progress, e.g.:

Code
Google: 120/800 — ETA 01:42
🛑 Stop Button
Interrupt translation at any time

Threads stop safely

No corrupted output files

🖥 Modern GUI
Progress bar

Status updates

Detected language display

Stop button

DeepL key storage

File picker dialog

📁 Supported Formats
.srt

.vtt

.ass

.ssa

🚀 How to Use
Portable Version
Download the ZIP

Extract it

Start the app via:

Code
SubtitleTranslator V12 EN.lnk
Done!

Installer Version
Download the .exe installer

Run it

Launch the app via Desktop shortcut or Start Menu

📦 Installation
🛠 Requirements
Windows 10 or 11

Python 3.10+ (only required for the portable version)

Internet connection for Google Translate / DeepL

Running the app manually (portable)
Code
python SubtitleTranslatorV12_EN.py
🔧 DeepL API Key
If you want to use DeepL:

Visit https://www.deepl.com

Create an API key

Enter it in the GUI

Click Save API key

Google Translate works without a key.

📁 Project Structure
Code
/
├── SubtitleTranslatorV12_EN.py
├── Start-SubtitleTranslatorV12_EN.bat
├── Start-SubtitleTranslatorV12_EN.vbs
├── SubtitleTranslator V12 EN.lnk
├── icon.ico
├── requirements.txt
├── README.md
├── LICENSE
└── screenshots/
    └── main-window.png
📝 License
This project is licensed under the MIT License.
See LICENSE for details.

❤️ Credits
Created by Frank & Copilot — a collaboration that keeps getting smarter.
