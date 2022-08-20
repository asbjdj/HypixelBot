from dataclasses import dataclass


@dataclass()
class PlayerObj:
    name = None
    uuid = None
    karma = None
    level = None
    rank = None
    firstLogin = None
    lastLogin = None
    lastLogout = None
    currentPet = None
    mostRecentGameType = None
    achievementPoints = None
    error = None


@dataclass()
class BedwarsObj:
    coins = None
    level = None
    kills_bedwars = None
    deaths_bedwars = None
    bedwars_boxes = None
    winstreak = None
    diamond_resources_collected_bedwars = None
    emerald_resources_collected_bedwars = None
    gold_resources_collected_bedwars = None
    iron_resources_collected_bedwars = None
    final_deaths_bedwars = None
    final_kills_bedwars = None
    losses_bedwars = None
    wins_bedwars = None
    games_played_bedwars = None
    beds_lost_bedwars = None
    beds_broken_bedwars = None
    fall_deaths_bedwars = None
    total_challenges_completed = None
    error = None


@dataclass()
class SkywarsObj:
    coins = None
    souls = None
    levelFormatted = None
    games_played_skywars = None
    deaths = None
    kills = None
    assists = None
    losses = None
    wins = None
    win_streak = None
    most_kills_game = None
    heads = None
