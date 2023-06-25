from typing import Union

from nonebot import on_message, on_command, require
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message
from nonebot.params import CommandArg
require("nonebot_plugin_guild_patch")
from nonebot_plugin_guild_patch import GuildMessageEvent

from .config import Config

from .utils import (
    msg_rule_cmd,
    msg_rule_no_cmd,
    get_message,
    send_msgs
)

__plugin_meta__ = PluginMetadata(
    name="群频互通",
    description="将QQ群与QQ频道的消息互通",
    usage="在群聊发送消息即可同步",
    config=Config,
    type="application",
    homepage="https://github.com/17TheWord/nonebot-plugin-group-link-guild",
    supported_adapters=[
        "nonebot.adapters.onebot.v11"
    ]
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
