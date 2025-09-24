
# EVE_Check 2.0 - EVE Online Local Chat Monitoring System

A project for automatically monitoring local chat in EVE Online with Discord and Telegram notifications about the appearance of hostile and neutral targets.

🎯 Main Features
- Automatic detection of targets in EVE Online local chat
- Color-coded target classification: red (enemies), orange (enemies), yellow (neutrals)
- Dual notification system: Discord + Telegram
- Sound alerts with gradation based on the number of targets
- Game client status monitoring (detection of disconnections)

---
# First Launch Process

## Initial Scan Area Setup

When you first launch the program, you will see a welcome message:

Welcome to the EVE_Check program.
Do you want to load settings from a file? (y/n):

### Important First Launch Points:

- ⚠️ **On first launch**, the scan area settings file is not yet configured.
- 🔧 **Select "n"** (no) to begin scanning area setup.

### Scan Area Setup Process:

1. **After selecting "n", the program will prompt you to configure the scan area:**

Please move your mouse to the upper left corner of the area and press F12.
Then move your mouse to the lower right corner of the area and press F12 again.

2. **Setup steps:**

- **Step 1:** Move your mouse cursor to the **upper left corner** of the local chat area in the EVE Online client
- **Press F12** to set the first point
- **Step 2:** Move your mouse cursor to the **lower right corner** of the local chat area
- **Press F12 again** to complete the setup

3. **Automatic saving:**
- Region settings are automatically saved to the `Config_Region.json` file
- The program will use the saved settings for subsequent launches

### For subsequent launches:

- ✅ **If settings have already been saved** - select "y" to load from file
- 🔄 **If you need to reconfigure the local chat area** - select "n" to reconfigure

📌 **Recommendation:** The scan area should cover the EVE Online local chat window where the Enemy ships. Ensure the area includes all possible target spawn locations.

---

## 🔧 System Requirements

- Windows 10 or higher
- Python 3.10+
- ffmpeg

---

## 📦 Installation

### 1. Install Python

Download and install Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
During installation, check the **"Add Python to PATH"** box.

### 2. Installing dependencies

Open a terminal (cmd/PowerShell) in the project folder and run:

```bash
python install_requirements.py
```

The script will install libraries from `install_packages.json`.

---

## 📁 Adding FFmpeg to the PATH environment variable

Download the FFmpeg archive from Google Drive:
- **Link**: https://drive.google.com/file/d/1lpm9JWwwDcHCoijf81RwGlEbhBhZKQcH/view?usp=sharing
- Download the file `ffmpeg.zip`

### Step 2: Unpacking

Unpack the archive:
- `C:\Tools\ffmpeg\` (recommended)

## Step 3: Setting the PATH environment variable

1. Press Win + R, type sysdm.cpl, and press Enter
2. Go to the Advanced tab → Environment Variables
3. Under System Variables, find Path
4. Click Edit → New
5. Add the path to the bin folder (example: C:\Tools\ffmpeg\bin)
6. Click OK on all windows

Check:

```bash
ffmpeg -version
```

---

## ⚙️ Configuring Configurations

Edit the files:

- `Config_Telegram.json` — Telegram chat token and ID
- `Config_Discord.json` — Discord token/webhook
- `Config_Region.json`, `Config_System.json` — system parameters

Example:
```json
{
    "TOKEN": "Your Discord API Token",
    "GUILD_ID": "Your Discord group ID",
    "CHANNEL_ID": "Your Discord Channel ID"
}
```

---

## 🚀 Launch

### Option 1: Via `.bat`
- Discord only: Double-click Start.bat
- Discord + Telegram: Double-click Start_Full.bat

### Option 2: Via Terminal

# To launch only the Discord bot, run the command:

```bash
python EVE_Check.py
```
# To launch the bot with Telegram and Discord support, run the command:

```bash
python EVE_Check_2.0.py
```

---

## 📌 Notes

- Uses `.wav` files from `Sound/` to play audio for events
- The bot sends notifications to Telegram/Discord when events are detected

---

## ⚠️ Important Note Regarding Security and Compliance

EVE Check is an **external application** (overlay) that runs alongside the EVE Online client, but **does not modify or interact with it directly**.

### Key Points:
* **No Client Interference**: The application does not inject code, read or modify game memory (RAM), or intercept network traffic.
* **OCR-Based**: Data analysis is performed solely by reading text from your computer screen (Optical Character Recognition - OCR technology). This is the same as if you were reading the information yourself.
* **EULA and TOS Compliance**: This method of operation does not violate the [End User License Agreement (EULA)](https://www.eveonline.com/en/agreement/eula) and [Terms of Service (TOS)](https://www.eveonline.com/en/agreement/tos) of EVE Online.

**Conclusion:** Using EVE Check **will not result in an account ban** by EVE Online security systems (e.g., Easy Anti-Cheat - EAC), as these systems are designed to detect programs that directly interact with the game. EVE Check is not such a program.  
