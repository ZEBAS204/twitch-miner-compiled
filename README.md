# Twitch Idle Farm

This is just a compiled version of [Twitch Channel Points Miner v2 (forked)](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2)

> **Note**
>
> The original version of [Twitch Channel Points Miner v2](https://github.com/Tkd-Alex/Twitch-Channel-Points-Miner-v2) is currently unmaintained. Instead, this project uses an up-to-date fork by [rdavydov](https://github.com/rdavydov).

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

### 🏃‍♂️ First Steps

1. After downloading it, on the first run, a `settings.json` will be created so you can configure it.
2. Go to the `settings.json` file, and configure your username (replace `your-}twitch-username` value of `miner_settings.username`) and password (replace `your-twitch-password` value of `miner_settings.password`)
   * You can remove the password key:value pair if you want to write it manually on the console.

3. Configure the rest to your liking (see [#Configuration differences](#-configuration-differences) to avoid errors)
4. Open the executable and follow the instructions if needed.

> **Warning**
> **Pasting your password does not work as intended, please write it manually or set up in `settings.json` as indicated in the second step.**

#### 📜 Settings Templates

The [`/settings.json`](/settings.json) file contains all the available configurations that are supported but, not limited to newer ones.

If you want to use pre-configured basic templates, you can hop and take a look into the [`/examples`](/examples) folder and copy any of them.

### 🔄 Updating

To install an update, just replace the executable file with the newer executable version downloaded.

If an error occurs with your old settings and you are not sure how to solve it, you can always delete the `settings.json` file so the executable can generate a valid version automatically.

### 🔀 Configuration differences

The main difference between the `settings.json` file with the actual python-written configuration of the original project is how functions and mapped values are handled:

> **Note** You can compare the code of [How to use](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2#how-to-use) section and the [settings.json](/settings.json) file to better understand these differences!

* **Mapped values**
  * Priority like `Priority.STREAK`, colors `Fore.GREEN`, discord/telegram events like `Events.STREAMER_ONLINE`, etc are written as strings without the event (e.g. `STREAK`, `GREEN`, `STREAMER_ONLINE`, etc)

* **Functions**
  * Functions are written as objects with the key being their variable name and, inside that object, their arguments as key-value pairs. E.g. `color_palette=ColorPalette(...)` is wrote as `color_palette: { "streamer_offline": "red", ... }`
  * Functions can nest other functions, just follow the same logic as above.
  * Reminder: new functions need to be manually added.

* **Logger**
  * The log level (used in `file_level`, `console_level`, etc) is written as an integer. For example, `logging.DEBUG` becomes `10`, `logging.INFO` becomes `20`, etc.
  * Logging will always follow the [logging module of python](https://docs.python.org/3/library/logging.html#logging-levels):
    * `CRITICAL`: 50
    * `ERROR`: 40
    * `WARNING`: 30
    * `INFO`: 20
    * `DEBUG`: 10
    * `NOTSET`: 0

---

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
$ python -m venv venv

# Activate virtual environment
$ source venv/bin/activate

# Install dependencies
$ python -m pip install -r requirements.txt

# Download TwitchChannelPointsMiner's scripts
$ ./download_directory.sh

# Run the script locally
$ python TwitchFarm.py

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
