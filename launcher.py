from __future__ import print_function
import os
import sys
import subprocess
try:                                        # Older Python lack this but this
    import urllib.request                   # lets them reach the Python check
    from importlib.util import find_spec
except ImportError:
    pass
import platform
import webbrowser
import hashlib
import argparse
import shutil
import stat
import time
try:
    import pip
except ImportError:
    pip = None

REQS_DIR = "lib"
sys.path.insert(0, REQS_DIR)
REQS_TXT = "requirements.txt"
FFMPEG_BUILDS_URL = "https://ffmpeg.zeranoe.com/builds/"

INTRO = ("=============================\n"
         "MooBot Discord Bot - Launcher\n"
         "=============================\n")

IS_WINDOWS = os.name == "nt"
IS_MAC = sys.platform == "darwin"
IS_64BIT = platform.machine().endswith("64")
INTERACTIVE_MODE = not len(sys.argv) > 1  # CLI flags = non-interactive
PYTHON_OK = sys.version_info >= (3, 5)

FFMPEG_FILES = {
    "ffmpeg.exe"  : "e0d60f7c0d27ad9d7472ddf13e78dc89",
    "ffplay.exe"  : "d100abe8281cbcc3e6aebe550c675e09",
    "ffprobe.exe" : "0e84b782c0346a98434ed476e937764f"
}

def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="MooBot Discord Bot's "
                                                 "launcher")
    parser.add_argument("--start", "-s",
                        help="Starts MooBot",
                        action="store_true")
    parser.add_argument("--auto-restart",
                        help="Autorestarts MooBot in case of issues",
                        action="store_true")
    parser.add_argument("--update-moobot",
                        help="Updates MooBot (git)",
                        action="store_true")
    parser.add_argument("--update-reqs",
                        help="Updates requirements",
                        action="store_true")
    parser.add_argument("--repair",
                        help="Issues a git reset --hard",
                        action="store_true")
    return parser.parse_args()


def install_reqs():
    remove_reqs_readonly()
    interpreter = sys.executable

    if interpreter is None:
        print("Python interpreter not found.")
        return

    txt = REQS_TXT

    args = [
        interpreter, "-m",
        "pip", "install",
        "--upgrade",
        "--target", REQS_DIR,
        "-r", txt
    ]

    if IS_MAC: # --target is a problem on Homebrew.
        args.remove("--target")
        args.remove(REQS_DIR)

    code = subprocess.call(args)

    if code == 0:
        print("\nRequirements setup completed.")
    else:
        print("\nAn error occurred and the requirements setup might "
              "not be completed. Consult the docs.\n")


def update_pip():
    interpreter = sys.executable

    if interpreter is None:
        print("Python interpreter not found.")
        return

    args = [
        interpreter, "-m",
        "pip", "install",
        "--upgrade", "pip"
    ]

    code = subprocess.call(args)

    if code == 0:
        print("\nPip has been updated.")
    else:
        print("\nAn error occurred and pip might not have been updated.")


def update_moobot():
    try:
        code = subprocess.call(("git", "pull", "--ff-only"))
    except FileNotFoundError:
        print("\nError: Git not found. It's either not installed or not in "
              "the PATH environment variable.")
        return
    if code == 0:
        print("\nMooBot has been updated")
    else:
        print("\nMooBot could not update properly. If this is caused by edits "
              "you have made to the code you can try the repair option from "
              "the Maintenance submenu")


def reset_moobot(reqs=False, data=False, cogs=False, git_reset=False):
    if reqs:
        try:
            shutil.rmtree(REQS_DIR, onerror=remove_readonly)
            print("Installed local packages have been wiped.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred when trying to remove installed "
                  "requirements: {}".format(e))
    if data:
        try:
            shutil.rmtree("data", onerror=remove_readonly)
            print("'data' folder has been wiped.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred when trying to remove the 'data' folder: "
                  "{}".format(e))

    if cogs:
        try:
            shutil.rmtree("cogs", onerror=remove_readonly)
            print("'cogs' folder has been wiped.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred when trying to remove the 'cogs' folder: "
                  "{}".format(e))

    if git_reset:
        code = subprocess.call(("git", "reset", "--hard"))
        if code == 0:
            print("MooBot has been restored to the last local commit.")
        else:
            print("The repair has failed.")


def download_ffmpeg(bitness):
    clear_screen()
    repo = "https://github.com/evanq123/MooBot/raw/master/"
    verified = []

    if bitness == "32bit":
        print("Please download 'ffmpeg 32bit static' from the page that "
              "is about to open.\nOnce done, open the 'bin' folder located "
              "inside the zip.\nThere should be 3 files: ffmpeg.exe, "
              "ffplay.exe, ffprobe.exe.\nPut all three of them into the "
              "bot's main folder.")
        time.sleep(4)
        webbrowser.open(FFMPEG_BUILDS_URL)
        return

    for filename in FFMPEG_FILES:
        if os.path.isfile(filename):
            print("{} already present. Verifying integrity... "
                  "".format(filename), end="")
            _hash = calculate_md5(filename)
            if _hash == FFMPEG_FILES[filename]:
                verified.append(filename)
                print("Ok")
                continue
            else:
                print("Hash mismatch. Redownloading.")
        print("Downloading {}... Please wait.".format(filename))
        with urllib.request.urlopen(repo + filename) as data:
            with open(filename, "wb") as f:
                f.write(data.read())
        print("Download completed.")

    for filename, _hash in FFMPEG_FILES.items():
        if filename in verified:
            continue
        print("Verifying {}... ".format(filename), end="")
        if not calculate_md5(filename) != _hash:
            print("Passed.")
        else:
            print("Hash mismatch. Please redownload.")

    print("\nAll files have been downloaded.")


def verify_requirements():
    sys.path_importer_cache = {} # TODO: Test for cache reset side effects.
    basic = find_spec("discord")
    audio = find_spec("nacl")
    if not basic:
        return None
    elif not audio:
        return False
    else:
        return True


def is_git_installed():
    try:
        subprocess.call(["git", "--version"], stdout=subprocess.DEVNULL,
                                              stdin =subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False
    else:
        return True


def requirements_menu():
    clear_screen()
    while True:
        print(INTRO)
        print("Main requirements:\n")
        print("1. Install basic + audio requirements (recommended)")
        if IS_WINDOWS:
            print("\nffmpeg (required for audio):")
            print("2. Install ffmpeg 32bit")
            if IS_64BIT:
                print("3. Install ffmpeg 64bit (recommended on Windows 64bit)")
        print("\n0. Go back")
        choice = user_choice()

        if choice == "1":
            install_reqs()
            wait()
        elif choice == "2" and IS_WINDOWS:
            download_ffmpeg(bitness="32bit")
            wait()
        elif choice == "3" and (IS_WINDOWS and IS_64BIT):
            download_ffmpeg(bitness="64bit")
            wait()
        elif choice == "0":
            break
        clear_screen()


def update_menu():
    clear_screen()
    while True:
        print(INTRO)
        reqs = verify_requirements()
        if reqs is None:
            status = "No requirements installed"
        else:
            status = "Basic + audio requirements installed"
        print("Status: " + status + "\n")
        print("Update:\n")
        print("MooBot:")
        print("1. Update MooBot + requirements (recommended)")
        print("2. Update MooBot")
        print("3. Update requirements")
        print("\nOthers:")
        print("4. Update pip (might require admin privileges)")
        print("\n0. Go back")
        choice = user_choice()
        if choice == "1":
            update_moobot()
            print("Updating requirements...")
            reqs = verify_requirements()
            if reqs is not None:
                install_reqs()
            else:
                print("The requirements haven't been installed yet.")
            wait()
        elif choice == "2":
            update_moobot()
            wait()
        elif choice == "3":
            reqs = verify_requirements()
            if reqs is not None:
                install_reqs()
            else:
                print("The requirements haven't been installed yet.")
            wait()
        elif choice == "4":
            update_pip()
            wait()
        elif choice == "0":
            break
        clear_screen()


def maintenance_menu():
    clear_screen()
    while True:
        print(INTRO)
        print("Maintenance:\n")
        print("1. Repair MooBot (discards code changes, keeps data intact)")
        print("2. Wipe 'data' folder (all settings, cogs' data...)")
        print("3. Wipe 'lib' folder (all local requirements / local installed"
              " python packages)")
        print("4. Factory reset")
        print("\n0. Go back")
        choice = user_choice()
        if choice == "1":
            print("Any code modification you have made will be lost. Data/"
                  "non-default cogs will be left intact. Are you sure?")
            if user_pick_yes_no():
                reset_moobot(git_reset=True)
                wait()
        elif choice == "2":
            print("Are you sure? This will wipe the 'data' folder, which "
                  "contains all your settings and cogs' data.\nThe 'cogs' "
                  "folder, however, will be left intact.")
            if user_pick_yes_no():
                reset_moobot(data=True)
                wait()
        elif choice == "3":
            reset_moobot(reqs=True)
            wait()
        elif choice == "4":
            print("Are you sure? This will wipe ALL your MooBot's installation "
                  "data.\nYou'll lose all your settings, cogs and any "
                  "modification you have made.\nThere is no going back.")
            if user_pick_yes_no():
                reset_moobot(reqs=True, data=True, cogs=True, git_reset=True)
                wait()
        elif choice == "0":
            break
        clear_screen()


def run_moobot(autorestart):
    interpreter = sys.executable

    if interpreter is None: # How can this happen?
        raise Runtimeerror("Couldn't find Python's interpreter")

    if verify_requirements() is None:
        print("You don't have the requirements to start MooBot. "
              "Install them from the launcher.")
        if not INTERACTIVE_MODE:
            exit(1)

    cmd = (interpreter, "moobot.py")

    while True:
        try:
            code = subprocess.call(cmd)
        except KeyboardInterrupt:
            code = 0
            break
        else:
            if code == 0:
                break
            elif code == 26:
                print("Restarting MooBot...")
                continue
            else:
                if not autorestart:
                    break
    print("MooBot has been terminated. Exit code: {0}".format(code))

    if INTERACTIVE_MODE:
        wait()


def clear_screen():
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")


def wait():
    if INTERACTIVE_MODE:
        input("Press enter to continue.")


def user_choice():
    return input("> ").lower().strip()


def user_pick_yes_no():
    choice = None
    yes = ("yes", "y")
    no = ("no", "n")
    while choice not in yes and choice not in no:
        choice = input("Yes/No > ").lower().strip()
    return choice in yes


def remove_readonly(func, path, excinfo):
    os.chmod(path, 0o755)
    func(path)


def remove_reqs_readonly():
    if not os.path.isdir(REQS_DIR):
        return
    os.chmod(REQS_DIR, 0o755)
    for root, dirs, files in os.walk(REQS_DIR):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o755)


def calculate_md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_fast_start_scripts():
    """Creates scripts for fast boot of MooBot without going
    through the launcher"""
    interpreter = sys.executable
    if not interpreter:
        return

    call = "\"{}\" launcher.py".format(interpreter)
    start_moobot = "{} --start".format(call)
    start_moobot_autorestart = "{} --start --auto-restart".format(call)
    modified = False

    if IS_WINDOWS:
        ccd = "pushd %~dp0\n"
        pause = "\npause"
        ext = ".bat"
    else:
        ccd = 'cd "$(dirname "$0")"\n'
        pause = "\nread -rsp $'Press enter to continue...\\n'"
        if not IS_MAC:
            ext = ".sh"
        else:
            ext = ".command"

    start_moobot             = ccd + start_moobot             + pause
    start_moobot_autorestart = ccd + start_moobot_autorestart + pause

    files = {
        "start_moobot"             + ext : start_moobot,
        "start_moobot_autorestart" + ext : start_moobot_autorestart
    }

    if not IS_WINDOWS:
        files["start_launcher" + ext] = ccd + call

    for filename, content in files.items():
        if not os.path.isfile(filename):
            print("Creating {}... (fast start scripts)".format(filename))
            modified = True
            with open(filename, "w") as f:
                f.write(content)

    if not IS_WINDOWS and modified: # Let's make them executable on Unix
        for script in files:
            st = os.stat(script)
            os.chmod(script, st.st_mode | stat.S_IEXEC)


def main():
    print("Verifying git installation...")
    has_git = is_git_installed()
    is_git_installation = os.path.isdir(".git")
    if IS_WINDOWS:
        os.system("TITLE MooBot Discord Bot - Launcher")
    clear_screen()

    try:
        create_fast_start_scripts()
    except Exception as e:
        print("Failed making fast start scripts: {}\n".format(e))

    while True:
        print(INTRO)

        if not is_git_installation:
            print("WARNING: It doesn't look like MooBot has been "
                  "installed with git.\nThis means that you won't "
                  "be able to update and some features won't be working.\n"
                  "A reinstallation is recommended. Follow the guide "
                  "properly this time:\n") # TODO: Add github.io guide for bot

        if not has_git:
            print("WARNING: Git not found. This means that it's either not "
                  "installed or not in the PATH environment variable like "
                  "requested in the guide.\n")

        print("1. Run MooBot /w autorestart in case of issues")
        print("2. Run MooBot")
        print("3. Update")
        print("4. Install requirements")
        print("5. Maintenance (repair, reset...)")
        print("\n0. Quit")
        choice = user_choice()
        if choice == "1":
            run_moobot(autorestart=True)
        elif choice == "2":
            run_moobot(autorestart=False)
        elif choice == "3":
            update_menu()
        elif choice == "4":
            requirements_menu()
        elif choice == "5":
            maintenance_menu()
        elif choice == "0":
            break
        clear_screen()

args = parse_cli_arguments()

if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    # Sets current directory to the script's
    os.chdir(dirname)
    if not PYTHON_OK:
        print("MooBot needs Python 3.5. Install the required version\n"
              "Press enter to continue.")
        if INTERACTIVE_MODE:
            wait()
        exit(1)
    if pip is None:
        print("MooBot cannot work without the pip module. Please make sure to "
              "install Python without unchecking any option during the setup")
        wait()
        exit(1)
    if args.repair:
        reset_moobot(git_reset=True)
    if args.update_moobot:
        update_moobot()
    if args.update_reqs:
        install_reqs()
    if INTERACTIVE_MODE:
        main()
    elif args.start:
        print("Starting MooBot...")
        run_moobot(autorestart=args.auto_restart)
