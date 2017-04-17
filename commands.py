import discord_bot, json, os, sys, re, asyncio, random, os.path
from user import User
from util import get_user
from subprocess import call, check_output, Popen
from sql_connector import connection
from config import config
import threading, user
from ideone_connector import Ideone
from debugger import Logger

commands = {
    "stats": {
        "executor": stats,
        "man": "Prints stats on the current user or supplied user"
    },
    "promote": {
        "executor": promote,
        "rank": 2,
        "man": "Promotes the user to admin"
    },
    "demote": {
        "executor": demote,
        "rank": 2,
        "man": "Demotes the user from admin"
    },
    "update": {
        "executor": update,
        "rank": 1,
        "man": "Restarts Thompson and updates his software"
    },
    "reboot": {
        "executor": reboot,
        "rank": 1,
        "man": "Restarts Thompson"
    },
    "man": {
        "executor": manual,
        "man": "Print manual info for a given command"
    },
    "purge": {
        "executor": purge,
        "rank": 2,
        "man": "Purge data from the database or a cache"
    },
    "exec": {
        "executor": code_exec,
        "rank": 1,
        "man": "Execute a `code` sample or ```code\nblock``` in the given language"
    },
    "analysis": {
        "executor": analysis,
        "rank": 2,
        "man": "print analysis for last executed command"
    }
}
