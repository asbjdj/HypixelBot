from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters.onebot.v11 import PRIVATE_FRIEND, GROUP
from nonebot.params import CommandArg

from .config import Config
from .utils.messageBuilder import *

plugin_config = Config.parse_obj(get_driver().config)

hyp = on_command(
    "hyp",
    priority=5,
    aliases={"hypixel"},
    permission=GROUP | PRIVATE_FRIEND,
    block=True
)


@hyp.handle()
async def handle_func(event: MessageEvent, cmd_arg: Message = CommandArg()):
    cmd_args = cmd_arg.extract_plain_text().strip().split()
    if len(cmd_args) < 2:
        await hyp.send(await info_message(cmd_args[0], event))
    else:
        match cmd_args[1].lower():
            case "bw" | "bedwars":
                await hyp.send(await bedwars_message(cmd_args[0], event))
            case "sw" | "skywars":
                await hyp.send(await skywars_message(cmd_args[0], event))
            case "uhc":
                pass
            case "mcgo":
                pass
