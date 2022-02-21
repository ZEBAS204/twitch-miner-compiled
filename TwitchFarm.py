#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, shutil
import simplejson as json
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

#* Get absolute path to resource, works for dev and for PyInstaller
#* https://stackoverflow.com/a/44352931
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


file = "settings.json"

#* Check if settings.json exist
#* if not, restore bundled files
if not os.path.exists(file):
    #* Copy the bundled settings file to the current directory
    #* and the README.md just in case...
    #* If README exist, copying will override it
    shutil.copy2(resource_path(file), '.')
    shutil.copy2(resource_path('README.md'), '.')

    print("Please check and configure settings.json")

else:
    try:
        f = open(file, "r")
        data = json.loads(f.read())

        twitch_miner = TwitchChannelPointsMiner(
            data["userSettings"]["username"])
        twitch_miner.mine(data["main_loop"]["user_to_watch"], followers=data["main_loop"]["followers"], blacklist=[
                          data["main_loop"]["followersBlackList"]])

    except OSError as err:
        print(f"OS error: {err}")

    except ValueError as err:
        print(f"Value error: {err}")

    #* JSONDecodeError inherits ValueError
    except Exception as err:
        print(f"Unexpected error: {err}, {type(err)=}")

    except KeyboardInterrupt:
        #* TwitchChannelPointsMiner already handles Keyboard Interruptions
        pass

    except SystemExit as err:
        #* TwitchChannelPointsMiner contains exit() functions
        #* beacuse of that, we need to intercept them to make reading errors
        #* user-friendly and mainly not closing the console automatically.
        print(f"Script exited with return code {err.code}")


#********************************
#* Suppress automatically exiting
#* But if user spams keys while waiting to exit, the buffer will get full
#* and skipped leading to automatically closing the console...
#********************************
input("\n[ PRESS ENTER TO EXIT ]")
