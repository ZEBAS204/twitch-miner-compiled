# Twitch_idle_farm

## 🎯 About Twitch Idle Farm

{{{   Describe your project   }}}

## 📛 What is and what is Not

* ✅ Intended to use without installing python

* ✅ Out-of-the-box usage

* ✅ Easy JSON configuration

* ✅ Console accessible

* ❌ **Replacement of the original project*

* ❌ **Up-to-date version:** The python dependency needs to be manually updated and fixes incompatibilities and re-compile it again manually.

* ❌ **1:1 with the actual project:** Even though the configuration follows the project examples, some manual changes need to be done to allow JSON. Please refer to [#Configuration]() for examples and differences.

* ❌ Error-free:** The `settings.json` keys need to follow the project configuration. The user is responsible for setting this error-free.

* ❌ **Python-less version:** Under the hood, the executable is extracting and using python inside the Temporary folder of your OS.

## ⏬ Downloading

You can compile it by yourself or use the precompiled binaries listed below on the [releases]() page:

* [Windows]()
* [Linux]()
* Mac: No support

## ⚙️ Configuration

### Differences

<br>

---

## Development

### 📂 Requirements

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com) and [Python]() installed.

### 🚀 Running

```bash
# Clone this project
$ git clone https://github.com/{{YOUR_GITHUB_USERNAME}}/_twitch_idle_farm

# Access
$ cd _twitch_idle_farm

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

# Or if you don't wish to use the provided spec file
# Note that NO ARCHITECTURE NOT OS will be embedded to the name
# If you are on WINDOWS Replace ":" ---> ";"
$ pyinstaller TwitchFarm.py \
    --name "TwitchFarm" \
    --onefile --console --clean \
    --add-data="README.md:." \
    --add-data="settings.json:."

# The executable will be placed inside the ./dist folder
# as TwitchFarm-{OS_name_and_architecture}.{OS_exec_extension}
```

## 📝 License

This project is under license from GNU V3. For more details, see the [LICENSE](LICENSE.md) file.

<a href="#top">Back to top</a>
