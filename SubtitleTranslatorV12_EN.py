import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import deepl
from deep_translator import GoogleTranslator, single_detection
import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

stop_flag = threading.Event()

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {"api_key": ""}
    return {"api_key": ""}

def save_config(api_key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": api_key}, f)

config = load_config()

GOOGLE_LANG_MAP = {
    "NL": "nl",
    "EN-GB": "en",
    "EN-US": "en",
    "DE": "de",
    "FR": "fr",
    "ES": "es",
    "IT": "it",
    "PT-PT": "pt",
    "PT-BR": "pt",
    "HI": "hi",
    "JA": "ja",
    "TR": "tr",
    "ZH": "zh-cn"
}

LANG_NAME_MAP = {
    "nl": "Dutch",
    "en": "English",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "hi": "Hindi",
    "ja": "Japanese",
    "tr": "Turkish",
    "zh-cn": "Chinese (Simplified)",
    "zh": "Chinese"
}

def google_translate_line(text, target_lang):
    if stop_flag.is_set():
        return None
    google_code = GOOGLE_LANG_MAP.get(target_lang, "en")
    try:
        return GoogleTranslator(source="auto", target=google_code).translate(text)
    except:
        time.sleep(0.3)
        return GoogleTranslator(source="auto", target=google_code).translate(text)

def parse_ass_dialogue(line):
    if not line.startswith("Dialogue:"):
        return None, None
    parts = line.split(",", 9)
    if len(parts) < 10:
        return None, None
    header = parts[:9]
    text = parts[9].rstrip("\n")
    return header, text

def rebuild_ass_dialogue(header, text):
    return ",".join(header) + "," + text + "\n"

def detect_subtitle_type(lines):
    if any("Dialogue:" in line for line in lines):
        return "ASS"
    if lines and lines[0].startswith("WEBVTT"):
        return "VTT"
    if any("-->" in line for line in lines):
        return "SRT"
    return "SRT"

def detect_language_from_lines(lines, sub_type):
    texts = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if sub_type == "ASS":
            header, ass_text = parse_ass_dialogue(line)
            if header and ass_text:
                texts.append(ass_text)
        else:
            if "-->" in stripped or stripped.isdigit():
                continue
            texts.append(stripped)

        if len(texts) >= 5:
            break

    if not texts:
        return None, None

    sample = " ".join(texts)[:500]

    try:
        code = single_detection(sample, api_key=None)
        code = code.lower()
        name = LANG_NAME_MAP.get(code, code)
        return code, name
    except:
        return None, None

def translate_google_multithread(lines, target_lang, progress_var, status_label, sub_type):
    translated = [""] * len(lines)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        for i, line in enumerate(lines):
            if stop_flag.is_set():
                break

            stripped = line.strip()

            if sub_type == "ASS":
                header, ass_text = parse_ass_dialogue(line)
                if header:
                    futures[executor.submit(google_translate_line, ass_text, target_lang)] = (i, header)
                    continue

            if stripped.isdigit() or "-->" in stripped or stripped == "" or (sub_type == "VTT" and "-->" in stripped):
                translated[i] = line
                continue

            futures[executor.submit(google_translate_line, stripped, target_lang)] = (i, None)

        total = len(futures)
        if total == 0:
            return lines

        done_count = 0
        start_time = time.time()

        for future in as_completed(futures):
            if stop_flag.is_set():
                break

            idx, header = futures[future]
            try:
                result = future.result()
                if result is None:
                    translated[idx] = lines[idx]
                elif header:
                    translated[idx] = rebuild_ass_dialogue(header, result)
                else:
                    translated[idx] = result + "\n"
            except:
                translated[idx] = lines[idx]

            done_count += 1
            pct = int(done_count / total * 100)

            elapsed = time.time() - start_time
            eta = (elapsed / done_count) * (total - done_count)
            eta_str = time.strftime("%M:%S", time.gmtime(eta))

            progress_var.set(pct)
            status_label.config(text=f"Google: {done_count}/{total} — ETA {eta_str}")
            status_label.update_idletasks()

    return translated

def translate_deepl_single(lines, source_lang, target_lang, api_key, progress_var, status_label, sub_type):
    translator = deepl.Translator(api_key)
    translated = []

    total = len(lines)
    start_time = time.time()

    for i, line in enumerate(lines):
        if stop_flag.is_set():
            break

        stripped = line.strip()

        pct = int((i + 1) / total * 100)

        elapsed = time.time() - start_time
        eta = (elapsed / (i + 1)) * (total - (i + 1))
        eta_str = time.strftime("%M:%S", time.gmtime(eta))

        progress_var.set(pct)
        status_label.config(text=f"DeepL: {i+1}/{total} — ETA {eta_str}")
        status_label.update_idletasks()

        if sub_type == "ASS":
            header, ass_text = parse_ass_dialogue(line)
            if header:
                try:
                    if source_lang == "auto":
                        result = translator.translate_text(ass_text, target_lang=target_lang).text
                    else:
                        result = translator.translate_text(ass_text, source_lang=source_lang, target_lang=target_lang).text
                    translated.append(rebuild_ass_dialogue(header, result))
                except:
                    translated.append(line)
                continue

        if stripped.isdigit() or "-->" in stripped or stripped == "":
            translated.append(line)
            continue

        try:
            if source_lang == "auto":
                result = translator.translate_text(stripped, target_lang=target_lang).text
            else:
                result = translator.translate_text(stripped, source_lang=source_lang, target_lang=target_lang).text

            translated.append(result + "\n")

        except:
            translated.append(line)

    return translated

def translate_subtitles(input_file, output_file, source_lang, target_lang, api_key, method, progress_var, status_label, detected_label):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sub_type = detect_subtitle_type(lines)
    status_label.config(text=f"Detected type: {sub_type}")
    status_label.update_idletasks()

    code, name = detect_language_from_lines(lines, sub_type)
    if code and name:
        detected_label.config(text=f"Detected language: {name} ({code})")
    else:
        detected_label.config(text="Detected language: unknown")
    detected_label.update_idletasks()

    if method == "Google Translate":
        translated = translate_google_multithread(lines, target_lang, progress_var, status_label, sub_type)
    else:
        translated = translate_deepl_single(lines, source_lang, target_lang, api_key, progress_var, status_label, sub_type)

    if not stop_flag.is_set():
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(translated)
        status_label.config(text="Done!")
    else:
        status_label.config(text="Stopped by user")

def choose_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Subtitle files", "*.srt *.vtt *.ass *.ssa")]
    )
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def save_api_key_action():
    key = entry_api.get().strip()
    save_config(key)
    messagebox.showinfo("Saved", "API key saved.")

def stop_translation():
    stop_flag.set()

def start_translation():
    stop_flag.clear()

    input_file = entry_file.get()
    source_lang = dropdown_source.get()
    target_lang = dropdown_target.get()
    api_key = entry_api.get().strip()
    method = dropdown_method.get()

    if not input_file:
        messagebox.showerror("Error", "Please select a subtitle file.")
        return

    if method == "DeepL" and not api_key:
        messagebox.showerror("Error", "Please enter a DeepL API key.")
        return

    base, ext = os.path.splitext(input_file)
    output_file = base + f"_{target_lang}{ext}"

    def run_translation():
        try:
            translate_subtitles(
                input_file,
                output_file,
                source_lang,
                target_lang,
                api_key,
                method,
                progress_var,
                status_label,
                detected_label
            )
            if not stop_flag.is_set():
                messagebox.showinfo("Done!", f"Saved as:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run_translation).start()

root = tk.Tk()
root.title("Subtitle Translator V12 (English Edition)")

tk.Label(root, text="Translation method:").pack()
dropdown_method = tk.StringVar(value="Google Translate")
tk.OptionMenu(root, dropdown_method, "DeepL", "Google Translate").pack()

tk.Label(root, text="DeepL API key:").pack()
entry_api = tk.Entry(root, width=50)
entry_api.insert(0, config.get("api_key", ""))
entry_api.pack()
tk.Button(root, text="Save API key", command=save_api_key_action).pack(pady=5)

tk.Label(root, text="Choose subtitle file (.srt / .vtt / .ass / .ssa):").pack()
entry_file = tk.Entry(root, width=50)
entry_file.pack()
tk.Button(root, text="Browse", command=choose_file).pack(pady=5)

tk.Label(root, text="Source language (DeepL only):").pack()
dropdown_source = tk.StringVar(value="auto")
tk.OptionMenu(root, dropdown_source,
              "auto", "NL", "EN-GB", "EN-US", "DE", "FR", "ES", "IT",
              "PT-PT", "PT-BR", "HI", "JA", "TR", "ZH").pack()

tk.Label(root, text="Target language:").pack()
dropdown_target = tk.StringVar(value="EN-GB")
tk.OptionMenu(root, dropdown_target,
              "NL", "EN-GB", "EN-US", "DE", "FR", "ES", "IT",
              "PT-PT", "PT-BR", "HI", "JA", "TR", "ZH").pack()

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="Not started...")
status_label.pack()

detected_label = tk.Label(root, text="Detected language: not yet detected")
detected_label.pack()

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Translate", command=start_translation, bg="#4CAF50", fg="white", width=12).pack(side="left", padx=5)
tk.Button(frame_buttons, text="STOP", command=stop_translation, bg="#E53935", fg="white", width=12).pack(side="left", padx=5)

root.mainloop()
