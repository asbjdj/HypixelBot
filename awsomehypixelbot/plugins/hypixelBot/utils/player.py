import time
import aiohttp
from aiohttp import ContentTypeError
import hypixel
from hypixel import Player
from hypixel import PlayerNotFoundException
from .objs import BedwarsObj, SkywarsObj, PlayerObj
from nonebot import get_driver

from ..config import Config

_ = Config.parse_obj(get_driver().config)
hypixel.setKeys([_.token])

NEVER_ENTER_ERROR = "Never Enter"
NOT_EXIST_ERROR = "Not Exist"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


async def get_uuid(name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            ret = await r.json()
            uuid = ret["id"]
        return uuid


async def get_info(name):
    _player = PlayerObj
    try:
        uuid = await get_uuid(name)
    except (ContentTypeError, KeyError, aiohttp.ContentTypeError):
        _player.error = NOT_EXIST_ERROR
        return _player

    try:
        player = Player(uuid)
    except PlayerNotFoundException:
        _player.error = NEVER_ENTER_ERROR
        return _player

    keys = player.JSON.keys()
    json_keys = ["karma", "mostRecentGameType", "currentPet", "achievementPoints", "lastLogin", "lastLogout"]
    for key in json_keys:
        if key not in keys:
            player.JSON[key] = "未知"

    _player.level = int(player.getLevel())
    _player.name = player.getName()
    _player.uuid = player.UUID
    _player.karma = player.JSON["karma"]
    _player.firstLogin = time.strftime(TIME_FORMAT, time.localtime(player.JSON["firstLogin"] / 1000))
    _player.lastLogin = time.strftime(TIME_FORMAT, time.localtime(player.JSON["lastLogin"] / 1000))
    _player.lastLogout = time.strftime(TIME_FORMAT, time.localtime(player.JSON["lastLogout"] / 1000))
    _player.mostRecentGameType = player.JSON["mostRecentGameType"]
    _player.currentPet = player.JSON["currentPet"]
    _player.achievementPoints = player.JSON["achievementPoints"]
    _player.rank = player.getRank().get("rank").upper().replace("SUPERSTAR", "MVP++").replace(" PLUS", "+").replace("YOUTUBER", "YOUTUBE")
    return _player


async def get_bedwars(name):
    stats = BedwarsObj

    try:
        raw_json = Player(await get_uuid(name)).JSON
        bw_stats = raw_json["stats"]["Bedwars"]
        achievements = raw_json["achievements"]
    except (ContentTypeError, KeyError, aiohttp.ContentTypeError):
        stats.error = NEVER_ENTER_ERROR
        return stats
    except PlayerNotFoundException:
        stats.error = NOT_EXIST_ERROR
        return stats

    keys = bw_stats.keys()
    json_keys = ["total_challenges_completed", "coins", "wins_bedwars", "losses_bedwars", "beds_broken_bedwars", "beds_lost_bedwars", "fall_deaths_bedwars"]
    for key in json_keys:
        if key not in keys:
            bw_stats[key] = 0

    stats.coins = bw_stats["coins"]
    stats.wins_bedwars = bw_stats["wins_bedwars"]
    stats.losses_bedwars = bw_stats["losses_bedwars"]
    stats.winstreak = bw_stats["winstreak"]
    stats.level = achievements["bedwars_level"]
    stats.beds_broken_bedwars = bw_stats["beds_broken_bedwars"]
    stats.beds_lost_bedwars = bw_stats["beds_lost_bedwars"]
    stats.bedwars_boxes = bw_stats["bedwars_boxes"]
    stats.deaths_bedwars = bw_stats["deaths_bedwars"]
    stats.kills_bedwars = bw_stats["kills_bedwars"]
    stats.iron_resources_collected_bedwars = bw_stats["iron_resources_collected_bedwars"]
    stats.gold_resources_collected_bedwars = bw_stats["gold_resources_collected_bedwars"]
    stats.diamond_resources_collected_bedwars = bw_stats["diamond_resources_collected_bedwars"]
    stats.emerald_resources_collected_bedwars = bw_stats["emerald_resources_collected_bedwars"]
    stats.final_deaths_bedwars = bw_stats["final_deaths_bedwars"]
    stats.final_kills_bedwars = bw_stats["final_kills_bedwars"]
    stats.fall_deaths_bedwars = bw_stats["fall_deaths_bedwars"]
    stats.total_challenges_completed = bw_stats["total_challenges_completed"]
    stats.games_played_bedwars = bw_stats["games_played_bedwars"]
    return stats


async def get_skywars(name):
    stats = SkywarsObj

    try:
        raw_json = Player(await get_uuid(name)).JSON
        sw_stats = raw_json["stats"]["SkyWars"]
    except (ContentTypeError, KeyError, aiohttp.ContentTypeError):
        stats.error = NEVER_ENTER_ERROR
        return stats
    except PlayerNotFoundException:
        stats.error = NOT_EXIST_ERROR
        return stats

    keys = sw_stats.keys()
    json_keys = ["kills", "coins", "wins", "losses", "deaths", "souls", "most_kills_game", "heads", "games_played_skywars", "assists"]
    for key in json_keys:
        if key not in keys:
            sw_stats[key] = 0

    stats.coins = sw_stats["coins"]
    stats.souls = sw_stats["souls"]
    stats.heads = sw_stats["heads"]
    stats.levelFormatted = sw_stats["levelFormatted"]
    stats.win_streak = sw_stats["win_streak"]
    stats.games_played_skywars = sw_stats["games_played_skywars"]
    stats.most_kills_game = sw_stats["most_kills_game"]
    stats.assists = sw_stats["assists"]
    stats.kills = sw_stats["kills"]
    stats.deaths = sw_stats["deaths"]
    stats.wins = sw_stats["wins"]
    stats.losses = sw_stats["losses"]
    return stats
