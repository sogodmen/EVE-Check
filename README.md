
# EVE-Check - EVE Local Chat Monitoring System

A project for automatically monitoring local chat in EVE with Discord notifications about the appearance of hostile and neutral targets.

🎯 Main Features
- Automatic detection of targets in EVE local chat
- Color-coded target classification: red (enemies), orange (enemies), yellow (neutrals)
- Notification system: Discord
- Sound alerts with gradation based on the number of targets
- Game client status monitoring (detection of disconnections)

---

## 🔧 System Requirements

- Windows 10 or higher
- Python 3.12+
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

### TOKEN (bot token):

1. **Go to the [Discord Developer Portal](https://discord.com/developers/applications)**
2. **Create a new application** or select an existing one
3. **In the "Bot" section**, create a bot and copy the token
4. **Enable the following permissions in the bot settings:**
- PRESENCE INTENT
- SERVER MEMBERS INTENT
- MESSAGE CONTENT INTENT
- In the "Privileged Gateway Intents" section

### GUILD_ID (server ID):

1. **Enable developer mode in Discord:**
- Settings → Advanced → Developer Mode
2. **Right-click the server** → "Copy Server ID"

### CHANNEL_ID (voice channel ID):

1. **Make sure the mode is set to [unspecified] Developer permissions enabled**
2. **Right-click on a voice channel** → "Copy Channel ID"

### Adding a bot to a server:

1. **In the Discord Developer Portal**, under "OAuth2" → "URL Generator"
2. **Select scopes:**
- `bot`
- `applications.commands`
3. **Select permissions:**
- `Connect` (connect to voice channels)
- `Speak` (speak in voice channels)
- `Use Voice Activity` (use voice activity)
- `View Channel` (view channels)
4. **Copy the generated link** and follow it
5. **Select a server** and add the bot with the specified permissions

### Configuring bot permissions on the server:

1. **On the Discord server**, go to the server settings
2. **The "Roles" section** - Find your bot's role
3. **Make sure the bot has the following permissions**
- Connect to voice channels
- Speak in voice channels
- View desired voice channels
4. **In the voice channel settings**, allow the bot to connect

### Connection check:

After setup, make sure the bot:
- ✅ Appears in the server participant list
- ✅ Can connect to the specified voice channel
- ✅ Has the necessary permissions to play sound

---

## 🚀 Launch

### Option 1: Via `.bat`
- Double-click Start.bat

### Option 2: Via Terminal

# To launch the Discord bot, run the command:

```bash
python EVE_Check.py
```

---

## 📌 Notes

- Uses `.wav` files from `Sound/` to play audio for events
- The bot sends notifications to Discord when events are detected
- Language Note: If you need sound files in Russian, replace the files in the Sound/ folder with the ones from the Sound [RU] folder.

---
# First Launch Process

## Initial Scan Area Setup

When you first launch the program, you will see a welcome message:

`
Welcome to the EVE_Check program.
Do you want to load settings from a file? (y/n):
`

### Important First Launch Points:

- ⚠️ **On first launch**, the scan area settings file is not yet configured.
- 🔧 **Select "`n`"** (no) to begin scanning area setup.

### Scan Area Setup Process:

1. **After selecting "`n`", the program will prompt you to configure the scan area:**

`
Please move your mouse to the upper left corner of the area and press F12.
Then move your mouse to the lower right corner of the area and press F12 again.
`

2. **Setup steps:**

- **Step 1:** Move your mouse cursor to the **upper left corner** of the local chat area in the EVE client
- **Press F12** to set the first point
- **Step 2:** Move your mouse cursor to the **lower right corner** of the local chat area
- **Press F12 again** to complete the setup

3. **Automatic saving:**
- Region settings are automatically saved to the `Config_Region.json` file
- The program will use the saved settings for subsequent launches

### For subsequent launches:

- ✅ **If settings have already been saved** - select "`y`" to load from file
- 🔄 **If you need to reconfigure the local chat area** - select "`n`" to reconfigure

📌 **Recommendation:** 
- The scan area should cover the EVE local chat window where the Enemy ships. Ensure the area includes all possible target spawn locations.
- **UI Important Setting**: For more accurate target monitoring in the local chat, change the color of neutral targets from gray to yellow in the settings.

---

# 💬 Important Message from the Developer

I have a very negative attitude toward bots in the game, but this bot was created as your first line of defense during your favorite pastime. Don't overuse it. I believe you'll find it useful.

**Fly safe, capsuleer! 🚀**
