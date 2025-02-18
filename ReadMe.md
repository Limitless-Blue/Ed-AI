# Running the Application
   ```bash
   .venv\Scripts\activate
   ```
   ```bash
   uvicorn API_Endpoint.main:app --reload
   ```
   ## open this Link
   ```bash
   http://127.0.0.1:8000/docs
   ```
---

# Getting Started

## Prerequisites
* Python 3.7+ (or the version you're using)
* `pip` (Python package installer)

## Installation
1. **Create a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   ```
   ```bash
   .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Install ffmpeg on Windows


### Step 1: Download ffmpeg

1. Visit the ffmpeg Download Page:
   - Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html).

2. Download a Windows Build:
   - Under the "Get packages & executable files" section, look for a Windows build.
   - A popular choice is from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/). Click on the "Download Build" link and then choose the "ffmpeg-release-essentials.zip" file (or a similar static build).

---

### Step 2: Extract and Place ffmpeg in a Permanent Location

1. Extract the Downloaded ZIP File:
   - Right-click the downloaded ZIP file and select "Extract All...".
   - Choose a location that you’ll remember. For example, extract it to `C:\ffmpeg`.

2. Locate the `bin` Folder:
   - Inside the extracted folder, locate the `bin` directory. It contains `ffmpeg.exe`, `ffprobe.exe`, etc.

---

### Step 3: Add ffmpeg to the System PATH

1. Open Environment Variables:
   - Press `Win + R`, type `sysdm.cpl`, and press Enter.
   - In the System Properties window, go to the "Advanced" tab and click on "Environment Variables...".

2. Edit the PATH Variable:
   - Under "System variables", scroll and find the variable named "Path". Select it and click "Edit".
   - Click "New" and add the path to the `bin` folder. For example:  
     ```
     C:\ffmpeg\bin
     ```
   - Click "OK" to close all dialogs.

3. Verify the Installation:
   - Open a new Command Prompt (press `Win + R`, type `cmd`, and press Enter).
   - Type the command:
     ```bash
     ffmpeg -version
     ```
   - If installed correctly, you should see version information about ffmpeg.

