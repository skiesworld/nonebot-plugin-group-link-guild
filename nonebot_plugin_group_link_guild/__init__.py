from typing import Union

from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message
from nonebot.params import CommandArg
from nonebot_plugin_guild_patch import GuildMessageEvent

from .utils import (
    msg_rule_cmd,
    msg_rule_no_cmd,
    get_message,
    send_msgs
)

nonebot_plugin_group_link_guild = on_message(rule=msg_rule_no_cmd, priority=31)

nonebot_plugin_group_link_guild_cmd = on_command("link", aliases={"."}, rule=msg_rule_cmd, priority=30, block=True)


@nonebot_plugin_group_link_guild.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    message = await get_message(bot, event)
    await send_msgs(event, message)


@nonebot_plugin_group_link_guild_cmd.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent], args: Message = CommandArg()):
    message = await get_message(bot, event)
    if message[:4] == "link":
        message = message[4:]
    elif message[:1] == ".":
        message = message[1:]
    await send_msgs(event, message)
