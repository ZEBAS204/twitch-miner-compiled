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

# Shortbard of isEmpty function
# and allows and returning the value when defined
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
        dL_color = dLogger["color_palette"]
        dL_tel = dLogger["telegram_settings"]

        # * Configure the miner
        twitch_miner = TwitchChannelPointsMiner(
            username=isEmpty(dMiner["username"]),
            password=isEmpty(dMiner["password"]),
            claim_drops_startup=isEmpty(dMiner["claim_drops_startup"], True),
            priority=isEmpty(dMiner["priority"]),
            logger_settings=isDefined(dLogger, LoggerSettings(
                save=isEmpty(dLogger["save"], True),

                # * Logging intervals: https://docs.python.org/3/library/logging.html#logging-levels
                console_level=isEmpty(dLogger["console_level"], logging.INFO),
                file_level=isEmpty(dLogger["file_level"], logging.DEBUG),

                auto_clear=isEmpty(dLogger["auto_clear"], True),
                emoji=isEmpty(dLogger["emoji"], False),
                less=isEmpty(dLogger["less"]),

                colored=isEmpty(dLogger["colored"]),
                color_palette=isDefined(dL_color, ColorPalette(
                    #* [ STREAMER_OFFLINE, GAIN_FOR_RAID, GAIN_FOR_CLAIM, GAIN_FOR_WATCH,
                    #* GAIN_FOR_WATCH_STREAK, BET_WIN, BET_LOSE, BET_REFUND, BET_FILTERS, BET_GENERAL, BET_FAILED, ]
                    STREAMER_ONLINE = isEmpty(dL_color["STREAMER_ONLINE"]),
                    STREAMER_OFFLINE = isEmpty(dL_color["STREAMER_OFFLINE"]),
                    GAIN_FOR_RAID = isEmpty(dL_color["GAIN_FOR_RAID"]),
                    GAIN_FOR_CLAIM = isEmpty(dL_color["GAIN_FOR_CLAIM"]),
                    GAIN_FOR_WATCH = isEmpty(dL_color["GAIN_FOR_WATCH"]),
                    GAIN_FOR_WATCH_STREAK = isEmpty(dL_color["GAIN_FOR_WATCH_STREAK"]),
                    BET_WIN = isEmpty(dL_color["BET_WIN"]),
                    BET_LOSE = isEmpty(dL_color["BET_LOSE"]),
                    BET_REFUND = isEmpty(dL_color["BET_REFUND"]),
                    BET_FILTERS = isEmpty(dL_color["BET_FILTERS"]),
                    BET_GENERAL = isEmpty(dL_color["BET_GENERAL"]),
                    BET_FAILED = isEmpty(dL_color["BET_FAILED"])
                )),

                telegram=isDefined(dL_tel, Telegram(
                    chat_id=isEmpty(dL_tel["chat_id"]),
                    token=isEmpty(dL_tel["token"]),
                    disable_notification=isEmpty(
                        dL_tel["disable_notification"]),
                    events=isEmpty(dL_tel["events"])
                ))
            ), LoggerSettings()),

            streamer_settings=isDefined(dStreamer, StreamerSettings(
                make_predictions=isEmpty(dStreamer["make_predictions"], False),
                follow_raid=isEmpty(dStreamer["follow_raid"], True),
                claim_drops=isEmpty(dStreamer["claim_drops"], True),
                watch_streak=isEmpty(dStreamer["watch_streak"]),
                join_chat=isEmpty(dStreamer["join_chat"], True),

                bet=isDefined(dS_bet, BetSettings(
                    # * [MOST_VOTED, HIGH_ODDS, PERCENTAGE, SMART]
                    strategy=Strategy[isEmpty(dS_bet["strategy"], "SMART")],
                    percentage=isEmpty(dS_bet["percentage"]),
                    percentage_gap=isEmpty(dS_bet["percentage_gap"]),
                    max_points=isEmpty(dS_bet["max_points"]),
                    stealth_mode=isEmpty(dS_bet["stealth_mode"]),

                    # * [FROM_START, FROM_END, PERCENTAGE]
                    delay_mode=DelayMode["FROM_END"],
                    delay=isEmpty(dS_bet["delay"]),
                    minimum_points=isEmpty(dS_bet["minimum_points"]),

                    filter_condition=isDefined(dS_bet["filter_condition"], FilterCondition(
                        # [PERCENTAGE_USERS, ODDS_PERCENTAGE, ODDS, TOP_POINTS, TOTAL_USERS, TOTAL_POINTS]
                        #! by=OutcomeKeys[isEmpty(dS_bet["filter_condition"]["by"], "TOTAL_USERS")],
                        # 'by' must be [GT, LT, GTE, LTE] than value
                        #! where=Condition[isEmpty(dS_bet["filter_condition"]["where"], "LTE")],
                        value=isEmpty(dS_bet["filter_condition"]["value"])
                    ))
                ))
            ), StreamerSettings())
        )

        # * Start mining channels
        twitch_miner.mine(
            isEmpty(dWatch["user_to_watch"]),
            blacklist=isEmpty(dWatch["followersBlackList"]),
            followers=isEmpty(dWatch["followers"]),
            #! followers_order=FollowersOrder[isEmpty(dWatch["followers_order"], "ASC")]
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
