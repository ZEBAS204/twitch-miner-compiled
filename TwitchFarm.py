#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import path
import logging
import traceback
from shutil import copy2
import simplejson as json
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import (
    Strategy,
    BetSettings,
    Condition,
    OutcomeKeys,
    FilterCondition,
    DelayMode,
)
from TwitchChannelPointsMiner.classes.entities.Streamer import (
    Streamer,
    StreamerSettings,
)


def resource_path(relative_path):
    # * Get absolute path to resource, works for dev and for PyInstaller
    # * https://stackoverflow.com/a/44352931
    base_path = getattr(sys, "_MEIPASS", path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)


def isEmpty(value=None, default=None, returnBool=False):
    """
    Allows to check values and restore their defaults
    if is empty, will return None and use the default value
    of the TwitchChannelPointsMiner for that key.
    """
    # ? Check if value is None
    # ? Check if value is an empty string
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


def deep_get(data, keys, default=None):
    """
    Example:
        d = {'meta': {'status': 'OK', 'status_code': 200}}
        deep_get(d, ['meta', 'status_code'])          # => 200
        deep_get(d, ['garbage', 'status_code'])       # => None
        deep_get(d, ['meta', 'garbage'], default='-') # => '-'

    See: https://stackoverflow.com/a/50173148
    """
    assert type(keys) is list
    if data is None:
        return default
    if not keys:
        return data
    return deep_get(data.get(keys[0]), keys[1:], default)


def safe_dict(
    object, key_to_extract=None, ignored_keys=[], callback=None, default=None
):
    """
    Safely get a dictionary from other dictionary with the ability to filter the
    returned keys.-
    Note that the idea of this function is to avoid using setdefault all over the place.
    """
    if isEmpty(object, returnBool=True):
        return default

    # We know the dictionary is not empty and if not key_to_extract was set,
    # return the same dictionary to avoid any error.
    if not key_to_extract:
        return object

    if key_to_extract in object and not isEmpty(
        object.get(key_to_extract), returnBool=True
    ):
        if not ignored_keys:
            if callback:
                return callback(**object[key_to_extract])
            return object[key_to_extract]
        else:
            # To avoid any mutation of the current dictionary,
            # return a new dictionary with the filtered keys
            temp: dict = object[key_to_extract].copy()
            for key in ignored_keys:
                if key in temp.keys():
                    del temp[key]
            if callback:
                return callback(**temp)
            return temp

    return default


# * Check if settings.json exist
# * if not, restore bundled files
file = "settings.json"
if not path.exists(file):
    # * Copy the bundled settings file to the current directory
    copy2(resource_path(file), ".")

    print("Please check and configure settings.json")
    # * Suppress automatically exiting
    input("\n[ PRESS ENTER TO EXIT ]")
    sys.exit(1)

else:
    try:
        f = open(file, "r")
        data = json.loads(f.read())

        # * Make life easier
        dMiner = deep_get(data, ["miner_settings"], {})
        dWatch = deep_get(data, ["watch_settings"], {})
        # streamer_settings
        dStreamer = deep_get(data, ["streamer_settings"], {})
        dS_bet = deep_get(data, ["streamer_settings", "bet"], {})
        # logger_settings
        dLogger = deep_get(data, ["logger_settings"], {})
        dL_tel = deep_get(data, ["logger_settings", "telegram_settings"], {})

        # * Configure the miner
        twitch_miner = TwitchChannelPointsMiner(
            **dMiner,
            #! If no logger_settings is defined, and we create the variable
            #! an error will be raised as is REQUIRED if defined
            logger_settings=isDefined(
                dLogger,
                LoggerSettings(
                    # * Color palette is a function
                    # * Telegram is a function
                    safe_dict(
                        dLogger, ignored_keys=["color_palette", "telegram_settings"]
                    ),
                    #! If no color_palette is defined, and we create the variable
                    #! an error will be raised as is REQUIRED if defined
                    color_palette=safe_dict(
                        dLogger, key_to_extract="color_palette", callback=ColorPalette
                    ),
                    telegram=safe_dict(
                        dLogger, key_to_extract="telegram_settings", callback=Telegram
                    ),
                    discord=safe_dict(
                        dLogger, key_to_extract="discord_settings", callback=Discord
                    ),
                ),
                # ! logger_settings default value
                LoggerSettings(None),
            ),
            streamer_settings=isDefined(
                dStreamer,
                StreamerSettings(
                    # * Bet is function
                    safe_dict(dStreamer, ignored_keys=["bet"]),
                    bet=isDefined(
                        dS_bet,
                        BetSettings(
                            # * filter_condition is function
                            safe_dict(dS_bet, ignored_keys=["filter_condition"]),
                            filter_condition=isDefined(
                                dS_bet.get("filter_condition"),
                                FilterCondition(safe_dict(dLogger, "filter_condition")),
                            ),
                        ),
                    ),
                ),
                # ! streamer_settings default value
                StreamerSettings(None),
            ),
        )

        # * Analytics web-server
        if deep_get(data, ["analytics_settings", "enabled"]):
            twitch_miner.analytics(
                **{
                    # * Enabled must be ignored and it's only there to allow
                    # * to toggle analytics without removing the whole object
                    k: v
                    for k, v in data["analytics_settings"].items()
                    if k != "enabled"
                }
            )

        # * Start mining channels
        twitch_miner.mine(
            # * Ignore user_to_watch as can be an optional array
            safe_dict(dWatch, "user_to_watch", default=[]),
            # * Ignore user_to_watch as is an empty array
            **{k: v for k, v in dWatch.items() if k != "user_to_watch"},
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
        # * because of that, we need to intercept them to make reading errors
        # * user-friendly and mainly prevent closing the console automatically.
        print(f"Script exited with return code {err.code}")


# **********************************
# * Suppress automatically exiting *
# **********************************
input("\n[ PRESS ENTER TO EXIT ]")
