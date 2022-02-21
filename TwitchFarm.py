#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import simplejson as json
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings


file = "settings.json"

if not os.path.exists(file):
    with open(file, "w") as f:
        f.write("""{
    "userSettings": {
        "username": "your-twitch-username"
    },

    "main_loop": {
        "user_to_watch": [
            "streamer-username09",
            "streamer-username10",
            "streamer-username11"
        ],
        "followers": false,
        "followersBlackList": ["user1", "user2"]
    }
}""")
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
