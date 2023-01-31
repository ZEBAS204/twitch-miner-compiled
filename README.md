# Twitch_idle_farm

This is just a compiled version of [Twitch Channel Points Miner v2](https://github.com/Tkd-Alex/Twitch-Channel-Points-Miner-v2).

## 📛 What is and what is Not

* ✅ Intended to use without installing python

* ✅ Out-of-the-box usage

* ✅ Easy JSON configuration

* ❌ **Replacement of the original project**

* ❌ **Up-to-date version:** The python dependency needs to be manually updated and fixes incompatibilities and re-compile it again manually.

* ❌ **1:1 with the actual project:** Even though the configuration follows the project examples, some manual changes need to be done to allow JSON configuration.

* ❌ **Error-free:** The `settings.json` keys need to follow the project configuration. The user is responsible for setting this error-free.

* ❌ **Python-less version:** Under the hood, the executable is extracting and using python inside the Temporary folder of your OS.

## ⏬ Downloading

You can compile it by yourself or use the precompiled binaries listed below on the [releases](https://github.com/ZEBAS204/twitch-miner-compiled/releases) page:

* [Windows](https://github.com/ZEBAS204/twitch-miner-compiled/releases/latest/download/TwitchFarm-win-amd64.exe)
* [Linux](https://github.com/ZEBAS204/twitch-miner-compiled/releases/latest/download/TwitchFarm-linux-x86_64)
* Mac: No support

## Development

### 📂 Requirements

Before starting, you will need to have [Git](https://git-scm.com) and [Python3](https://www.python.org/) installed.

### 🚀 Running

```bash
# Clone this project
$ git clone https://github.com/ZEBAS204/twitch-miner-compiled

# Access
$ cd twitch-miner-compiled

# Create virtual environment (use the one you wish)
$ python venv venv

# Activate virtual environment
$ source venv/Scripts/Activate

# Install dependencies
$ py -m pip install -r requirements.txt

# Run the script locally
$ py TwitchFarm.py

# To compile the python script
$ ./compile.sh

# To clean the files left when testing and allow to start over
$ ./clean.sh

# If Analytics server is enabled, will initialize in the <http://localhost:5000>
```

### 🛠️ Compiling

Compiling the script into an executable **will only produce an executable for your current platform and architecture**. For more information, please refer to [PyInstaller's "Building the Bootloader" documentation](https://pyinstaller.readthedocs.io/en/stable/bootloader-building.html).

The executable name will follow as `TwitchFarm-{OS_name_and_architecture}.{OS_exec_extension}`.
For more information about the OS name and architecture used, please refer to the [Python sysconfig documentation](https://docs.python.org/3/library/sysconfig.html#sysconfig.get_platform).

```bash
# * Using a virtual environment is recommended *
# Compiling the python script
$ ./compile.sh

# Or without the help of the bash script
$ pyinstaller TwitchFarm.spec

# The executable will be placed inside the ./dist folder
```

## 📝 License

The project follows the GNU V3 license and no modifications have been made to the original code. Instead, the project is a wrapper for the original code. This means that the project provides an interface for accessing and utilizing the functionality of the original code, without modifying its underlying implementation.
