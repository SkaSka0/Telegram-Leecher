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
# @markdown - `DUMP_ID` `(Private Channel/Grub)`
# @markdown
# @markdown 📍 You can open Secrets from the **left sidebar → 🔑 Secrets**
# @markdown
# @markdown After adding them, simply **run this cell to start the bot**.
# @markdown
# @markdown ---

import json
import os
import shutil
import subprocess
import re
import importlib
from importlib import metadata

from IPython.display import clear_output

# 📌 Config
APPNAME = "TelegramLeecher"
REPO_URL = "https://github.com/SkaSka0/Telegram-Leecher"
REPO_NAME = "Telegram-Leecher"
REQUIRED_SECRETS = ("API_ID", "API_HASH", "BOT_TOKEN", "USER_ID", "DUMP_ID")

# Maps executable name -> apt package that provides it
SYSTEM_TOOLS = {
    "ffmpeg": "ffmpeg",
    "aria2c": "aria2",
    "megadl": "megatools",
}

target_branch = "main"  # @param ["colab-mirror", "main"]

# 📌 Logging
def log(message, level="INFO"):
    print(f"{level}:{APPNAME}:{message}")

# 📌 Shell helper (replaces the 3x duplicated Popen+readline blocks)
def run_streamed(cmd, error_message=None):
    """Run a command, streaming each stdout/stderr line through log().

    cmd can be a string (shell=True) or a list (shell=False), matching
    how the original script mixed both styles.
    """
    proc = subprocess.Popen(
        cmd,
        shell=isinstance(cmd, str),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for line in proc.stdout:
        if line.strip():
            log(line.strip())

    proc.wait()

    if proc.returncode != 0:
        log(error_message or f"Command failed: {cmd}", level="ERROR")

    return proc.returncode

# 📌 Steps
def parse_requirements(path: str) -> list[str]:
    """Extracts package names from a requirements.txt file.

    Args:
        path: Path to the requirements file.

    Returns:
        A list of bare package names (version specifiers, extras and
        comments removed).
    """
    names = []
    with open(path, "r") as file:
        for line in file:
            line = line.split("#")[0].strip()
            if not line or line.startswith("-"):
                continue
            name = re.split(r"[<>=!~;\[\s]", line, maxsplit=1)[0]
            if name:
                names.append(name)
    return names


def check_dependencies() -> dict:
    """Verifies that system tools and Python packages are installed.

    Returns:
        A dict with two lists: 'missing_tools' (executables not on PATH)
        and 'missing_packages' (Python packages with no installed metadata).
    """
    importlib.invalidate_caches()

    missing_tools = [
        f"{tool} (apt: {pkg})"
        for tool, pkg in SYSTEM_TOOLS.items()
        if shutil.which(tool) is None
    ]

    missing_packages = []
    req_path = f"/content/{REPO_NAME}/requirements.txt"
    for name in parse_requirements(req_path):
        try:
            metadata.version(name)
        except metadata.PackageNotFoundError:
            missing_packages.append(name)

    return {"missing_tools": missing_tools, "missing_packages": missing_packages}


def report_dependency_status(status: dict) -> None:
    """Logs a summary of the dependency check.

    Args:
        status: The dict returned by check_dependencies().
    """
    missing_tools = status["missing_tools"]
    missing_packages = status["missing_packages"]

    if not missing_tools and not missing_packages:
        log("Dependency check: all dependencies installed successfully")
        return

    log("Dependency check: some dependencies failed to install", level="ERROR")
    for item in missing_tools:
        log(f"Missing system tool: {item}", level="ERROR")
    for item in missing_packages:
        log(f"Missing Python package: {item}", level="ERROR")

def load_credentials():
    """Read + validate secrets from Colab, return a normalized dict."""
    from google.colab import userdata

    log("Initializing setup...")

    raw = {key: userdata.get(key) for key in REQUIRED_SECRETS}

    missing = [key for key, value in raw.items() if value is None or value == ""]
    if missing:
        for key in missing:
            log(f"Missing secret: {key}", level="ERROR")
        raise ValueError(f"Missing secret(s): {', '.join(missing)}")

    log("Credentials loaded from Colab Secrets")

    creds = {
        "API_ID": int(raw["API_ID"]),
        "API_HASH": raw["API_HASH"],
        "BOT_TOKEN": raw["BOT_TOKEN"],
        "USER_ID": int(raw["USER_ID"]),
        "DUMP_ID": int(raw["DUMP_ID"]),
    }

    # Format DUMP_ID (add -100 prefix for channel/supergroup IDs)
    dump_id_str = str(creds["DUMP_ID"])
    if len(dump_id_str) == 10 and "-100" not in dump_id_str:
        log(f"Formatting DUMP_ID: adding -100 prefix to {creds['DUMP_ID']}")
        creds["DUMP_ID"] = int("-100" + dump_id_str)

    return creds


def clean_sample_data():
    if os.path.exists("/content/sample_data"):
        log("Removing default Colab sample data directory")
        shutil.rmtree("/content/sample_data")


def clone_repo(branch):
    if os.path.exists(REPO_NAME):
        log(f"Existing '{REPO_NAME}' folder found - removing...")
        shutil.rmtree(REPO_NAME)

    log(f"Cloning repository from {REPO_URL} branch: {branch}")
    result = subprocess.run(
        ["git", "clone", "-b", branch, REPO_URL], capture_output=True, text=True
    )

    if result.returncode != 0:
        log(f"Failed to clone repository: {result.stderr}", level="ERROR")
        raise RuntimeError("Repository cloning failed")


def install_system_deps():
    log("Installing system dependencies (ffmpeg, aria2)...")
    run_streamed(
        "apt install ffmpeg aria2 -y",
        error_message="System dependencies installation failed",
    )


def install_megatools():
    log("Installing megatools...")
    run_streamed(
        "apt-get install -y megatools",
        error_message="Megatools installation failed",
    )


def install_python_deps():
    log("Installing Python dependencies...")
    req_path = f"/content/{REPO_NAME}/requirements.txt"
    run_streamed(
        ["pip3", "install", "-r", req_path],
        error_message="Python dependencies installation failed",
    )


def save_credentials(creds):
    log("Saving credentials to credentials.json...")
    creds_path = f"/content/{REPO_NAME}/credentials.json"
    try:
        with open(creds_path, "w") as file:
            json.dump(creds, file, indent=4)
        log("Credentials saved successfully")
    except Exception as e:
        log(f"Failed to save credentials: {e}", level="ERROR")
        raise


def clear_old_session():
    session_path = f"/content/{REPO_NAME}/my_bot.session"
    if os.path.exists(session_path):
        log("Removing previous bot session file")
        os.remove(session_path)

def prepare_launch(status: dict):
    """Clears the cell output, reports dependency status, then announces launch.

    Args:
        status: The dict returned by check_dependencies().
    """
    clear_output()
    report_dependency_status(status)
    log("Launching Telegram Leecher bot...")


def main():
    creds = load_credentials()
    clean_sample_data()
    clone_repo(target_branch)
    install_system_deps()
    install_megatools()
    install_python_deps()
    status = check_dependencies()
    save_credentials(creds)
    clear_old_session()
    prepare_launch(status)


main()

# Run bot (must stay at cell-level to use Colab's `!` magic command)
get_ipython().system(f'cd /content/{REPO_NAME}/ && python3 -m colab_leecher')  # type: ignore
