from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

from .player import PlayerObj, get_info, NOT_EXIST_ERROR, NEVER_ENTER_ERROR, get_bedwars, \
    get_skywars


async def check_player(player: PlayerObj, event: MessageEvent):
    if player.error == NOT_EXIST_ERROR:
        return Message([MessageSegment.at(event.sender.user_id), "玩家不存在"])
    elif player.error == NEVER_ENTER_ERROR:
        return Message([MessageSegment.at(event.sender.user_id), "玩家未登录过Hypixel"])
    else:
        return None


def get_rank(player: PlayerObj):
    if player.rank.upper() == "NON":
        player.rank = ""
    else:
        player.rank = f"[{player.rank}] "


async def info_message(name, event: MessageEvent):
    player = await get_info(name)

    if (result := await check_player(player, event)) is None:
        get_rank(player)
        return Message([MessageSegment.at(event.sender.user_id),
                        f"\n{player.rank}{player.name} [Lv.{player.level}]"
                        f"\nUUID: {player.uuid}"
                        f"\nKarma: {('{:,}'.format(player.karma))}"
                        f"\nAchievement Points: {'{:,}'.format(player.achievementPoints)}"
                        f"\nFirst Login: {player.firstLogin}"
                        f"\nLast Login: {player.lastLogin}"
                        f"\nLast Logout: {player.lastLogout}"
                        f"\nMostRecentgames: {player.mostRecentGameType}"
                        f"\nCurrent Pet: {player.currentPet}"])
    else:
        return result


async def bedwars_message(name, event: MessageEvent):
    bw_stats = await get_bedwars(name)
    player = await get_info(name)

    if (result := await check_player(player, event)) is None:
        get_rank(player)
        return Message([MessageSegment.at(event.sender.user_id),
                        f"\n{player.rank}{player.name} [Lv.{bw_stats.level}]"
                        f"\n硬币: {bw_stats.coins} 战利品箱: {bw_stats.bedwars_boxes} 连胜: {bw_stats.winstreak} 总游戏场数: {bw_stats.games_played_bedwars} 已完成挑战: {bw_stats.total_challenges_completed}"
                        f"\n击杀: {bw_stats.kills_bedwars} 死亡: {bw_stats.deaths_bedwars} KDR: {round(bw_stats.kills_bedwars / bw_stats.deaths_bedwars, 2)}"
                        f"\n最终击杀: {bw_stats.final_kills_bedwars} 最终死亡: {bw_stats.final_deaths_bedwars} FKDR: {round(bw_stats.final_kills_bedwars / bw_stats.final_deaths_bedwars, 2)}"
                        f"\n摧毁床: {bw_stats.beds_broken_bedwars} 被摧毁床: {bw_stats.beds_lost_bedwars} BBLR: {round(bw_stats.beds_broken_bedwars / bw_stats.beds_lost_bedwars, 2)}"
                        f"\n胜场: {bw_stats.wins_bedwars} 败场: {bw_stats.losses_bedwars} WLR: {round(bw_stats.wins_bedwars / bw_stats.losses_bedwars, 2)}"
                        f"\n玩家{player.name}共摔死{bw_stats.fall_deaths_bedwars}次"])
    else:
        return result


async def skywars_message(name, event: MessageEvent):
    sw_stats = await get_skywars(name)
    player = await get_info(name)
    if (result := await check_player(player, event)) is None:
        get_rank(player)
        return Message([MessageSegment.at(event.sender.user_id),
                        f"\n{player.rank}{player.name} [{sw_stats.levelFormatted[2:]}]"
                        f"\n硬币: {sw_stats.coins} 灵魂: {sw_stats.souls} 头颅: {sw_stats.heads} 助攻: {sw_stats.assists}"
                        f"\n连胜: {sw_stats.win_streak} 总游戏场数: {sw_stats.games_played_skywars}"
                        f"\n击杀: {sw_stats.kills} 死亡: {sw_stats.deaths} KDR: {round(sw_stats.kills / sw_stats.deaths, 2)}"
                        f"\n胜场: {sw_stats.wins} 败场: {sw_stats.losses} WLR: {round(sw_stats.wins / sw_stats.losses, 2)}"])
    else:
        return result
