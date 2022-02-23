#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import traceback
import logging
import simplejson as json
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

# * Get absolute path to resource, works for dev and for PyInstaller
# * https://stackoverflow.com/a/44352931


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# * Allows to check values and restore their defaults
# * if is empty, returning None will use the default value
# * of the TwitchChannelPointsMiner for that key
def isEmpty(value, default=None, returnBool=False):
    # ? Check if value is None
    # ? Check if value is object and is empty
    # ? Check if value is array and is empty
    # print(f"CHECKING ATTRIBUTE: {value} - DEFAULT: {default}, RETURN: {returnBool}")

    if value is None or value == "" or value == {} or value == []:
        if returnBool:
            return True
        return default
    else:
        if returnBool:
            return False
        return value

# * Shortbard of isEmpty function
# * and allows and returning the value when defined
def isDefined(value, returnDefined, returnNotDefined=None):
    if isEmpty(value, None, True):
        return returnNotDefined
    return returnDefined


file = "settings.json"

#! When debugging should be enabled to skip the file check
skipMe = False

# * Check if settings.json exist
# * if not, restore bundled files
if not skipMe and not os.path.exists(file):
    # * Copy the bundled settings file to the current directory
    # * and the README.md just in case...
    # * If README exist, copying will override it
    shutil.copy2(resource_path(file), '.')
    shutil.copy2(resource_path('README.md'), '.')

    print("Please check and configure settings.json")

else:
    try:
        f = open(file, "r")
        data = json.loads(f.read())

        # * Make life easier
        dMiner = data["miner_settings"]
        dWatch = data["watch_settings"]
        # streamer_settings
        dStreamer = data["streamer_settings"]
        dS_bet = dStreamer["bet"]
        # logger_settings
        dLogger = data["logger_settings"]
        dL_tel = dLogger["telegram_settings"]

        # * Configure the miner
        twitch_miner = TwitchChannelPointsMiner(
            **dMiner,

            logger_settings=isDefined(dLogger, LoggerSettings(
                # * Color palette is function
                # * Telegram is function
                **{
                    k: v for k, v in dLogger.items() if
                    not k == 'color_palette' and not k == 'telegram_settings'
                },

                color_palette=isDefined(dLogger["color_palette"], ColorPalette(
                    **dLogger["color_palette"]
                )),

                telegram=isDefined(dL_tel, Telegram(
                    **dL_tel
                ))
            )),

            streamer_settings=isDefined(dStreamer, StreamerSettings(
                # * Bet is function
                **{k: v for k, v in dStreamer.items() if not k == 'bet'},

                bet=isDefined(dS_bet, BetSettings(
                    # * filter_condition is function
                    **{k: v for k, v in dS_bet.items() if not k == 'filter_condition'},

                    filter_condition=isDefined(dS_bet["filter_condition"], FilterCondition(
                        **dS_bet["filter_condition"]
                    ))
                ))
            ))
        )

        # * Analytics web-server
        isDefined(data["analytics_settings"],
                  data["analytics_settings"]["enabled"] and twitch_miner.analytics(**{
                      k: v for k, v in data["analytics_settings"].items() if not k == 'enabled'
                  })
                  )

        # * Start mining channels
        twitch_miner.mine(
            isEmpty(dWatch["user_to_watch"]),

            # * Ignore user_to_watch as is an empty array
            **{k: v for k, v in dWatch.items() if not k == 'user_to_watch'}
        )

    except OSError as err:
        print(f"OS error: {err}")
        traceback.print_exc()

    except ValueError as err:
        print(f"Value error: {err}")
        traceback.print_exc()

    # * JSONDecodeError inherits ValueError
    except Exception as err:
        print(f"Unexpected error: {err}, {type(err)=}")
        traceback.print_exc()

    except KeyboardInterrupt:
        # * TwitchChannelPointsMiner already handles Keyboard Interruptions
        pass

    except SystemExit as err:
        # * TwitchChannelPointsMiner contains exit() functions
        # * beacuse of that, we need to intercept them to make reading errors
        # * user-friendly and mainly not closing the console automatically.
        print(f"Script exited with return code {err.code}")


# ********************************
# * Suppress automatically exiting
# * But if user spams keys while waiting to exit, the buffer will get full
# * and skipped leading to automatically closing the console...
# ********************************
input("\n[ PRESS ENTER TO EXIT ]")
