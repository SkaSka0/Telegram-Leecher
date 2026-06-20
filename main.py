# @title <font color=red> 🖥️ Main Colab Leech Code

# @markdown <div><center><img src="https://user-images.githubusercontent.com/125879861/255391401-371f3a64-732d-4954-ac0f-4f093a6605e1.png" height=80></center></div>
# @markdown <center><h4><a href="https://github.com/XronTrix10/Telegram-Leecher/wiki/INSTRUCTIONS">READ</a><b> How to use</b></h4></center>
# @markdown <br><center><h2><font color=lime><strong>Fill all Credentials, Run The Cell and Start The Bot</strong></h2></center>
# @markdown <br><br>

# @markdown ---
# @markdown 
# @markdown ⚠️ **Important Setup**
# @markdown
# @markdown This notebook now uses **Colab Secrets** instead of `#@param`.
# @markdown
# @markdown Before running this cell, add the following variables in the **🔑 Colab Secrets panel**:
# @markdown
# @markdown - `API_ID`
# @markdown - `API_HASH`
# @markdown - `BOT_TOKEN`
# @markdown - `USER_ID`
# @markdown - `DUMP_ID`
# @markdown
# @markdown 📍 You can open Secrets from the **left sidebar → 🔑 Secrets**
# @markdown
# @markdown After adding them, simply **run this cell to start the bot**.
# @markdown 
# @markdown ---

from google.colab import userdata

API_ID = userdata.get("API_ID")
API_HASH = userdata.get("API_HASH")
BOT_TOKEN = userdata.get("BOT_TOKEN")
USER_ID = userdata.get("USER_ID")
DUMP_ID = userdata.get("DUMP_ID")

required_vars = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "USER_ID": USER_ID,
    "DUMP_ID": DUMP_ID
}

for key, value in required_vars.items():
    if value is None or value == "":
        raise ValueError(f"Missing secret: {key}")

# convert to int after validation
API_ID = int(API_ID)
USER_ID = int(USER_ID)
DUMP_ID = int(DUMP_ID)

import subprocess, json, shutil, os
from IPython.display import clear_output

# =====================================================================
# 📌 Unified Simple Logging
# =====================================================================
APPNAME = "TelegramLeecher"

def log(message, level="INFO"):
    print(f"{level}:{APPNAME}:{message}")

# =====================================================================
# 📌 Start
# =====================================================================

log("Initializing setup...")
log("Credentials loaded from Colab Secrets")

# Format DUMP_ID
if DUMP_ID and len(str(DUMP_ID)) == 10 and "-100" not in str(DUMP_ID):
    log(f"Formatting DUMP_ID: adding -100 prefix to {DUMP_ID}")
    DUMP_ID = int("-100" + str(DUMP_ID))

# Remove default Colab sample data
if os.path.exists("/content/sample_data"):
    log("Removing default Colab sample data directory")
    shutil.rmtree("/content/sample_data")

# Git repo data
repo_url = "https://github.com/lIlSkaSkaSkalIl/Telegram-Leecher"
repo_name = "Telegram-Leecher"

# Remove old folder if exists
if os.path.exists(repo_name):
    log(f"Existing '{repo_name}' folder found - removing...")
    shutil.rmtree(repo_name)

# Clone fresh repository
log(f"Cloning repository from {repo_url}")
clone_result = subprocess.run(["git", "clone", repo_url], capture_output=True, text=True)

if clone_result.returncode != 0:
    log(f"Failed to clone repository: {clone_result.stderr}", level="ERROR")
    raise RuntimeError("Repository cloning failed")

# Install system dependencies
log("Installing system dependencies (ffmpeg, aria2)...")
install_proc = subprocess.Popen(
    "apt install ffmpeg aria2 -y",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

while True:
    line = install_proc.stdout.readline()
    if not line:
        break
    if line.strip():
        log(line.strip())

install_proc.wait()

if install_proc.returncode != 0:
    log("System dependencies installation failed", level="ERROR")
    for line in install_proc.stderr:
        log(line.strip(), level="ERROR")

# Install Megatools
log("Installing megatools...")
megatools_proc = subprocess.Popen(
    "apt-get install -y megatools",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

while True:
    line = megatools_proc.stdout.readline()
    if not line:
        break
    if line.strip():
        log(line.strip())

megatools_proc.wait()

# Install Python dependencies
log("Installing Python dependencies...")
req_path = "/content/Telegram-Leecher/requirements.txt"
pip_proc = subprocess.Popen(
    ["pip3", "install", "-r", req_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

for line in pip_proc.stdout:
    log(line.strip())

pip_proc.wait()

if pip_proc.returncode != 0:
    log("Python dependencies installation failed", level="ERROR")

# Save credentials.json
log("Saving credentials to credentials.json...")
credentials = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "USER_ID": USER_ID,
    "DUMP_ID": DUMP_ID,
}

try:
    with open('/content/Telegram-Leecher/credentials.json', 'w') as file:
        json.dump(credentials, file, indent=4)
    log("Credentials saved successfully")
except Exception as e:
    log(f"Failed to save credentials: {e}", level="ERROR")
    raise

# Remove previous bot session
session_path = "/content/Telegram-Leecher/my_bot.session"
if os.path.exists(session_path):
    log("Removing previous bot session file")
    os.remove(session_path)

clear_output()
log("Launching Telegram Leecher bot...")

# Run bot
!cd /content/Telegram-Leecher/ && python3 -m colab_leecher  # type: ignore
