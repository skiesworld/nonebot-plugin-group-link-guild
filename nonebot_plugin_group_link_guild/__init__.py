from typing import Union

from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message
from nonebot_plugin_guild_patch import GuildMessageEvent

from .utils import (
    group_list,
    msg_rule,
    get_member_nickname,
    get_group_role,
    get_role_name,
    send_msgs,
    get_message, send_msgs_cmd
)

nonebot_plugin_group_link_guild = on_message(rule=msg_rule, priority=31)

nonebot_plugin_group_link_guild_cmd = on_command("link", aliases={"."}, rule=msg_rule, priority=30, block=True)


@nonebot_plugin_group_link_guild.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    sender_name, message = await get_message(bot, event)
    await send_msgs(bot, event, f"{sender_name}：\n{Message(message)}")


@nonebot_plugin_group_link_guild_cmd.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    sender_name, message = await get_message(bot, event)
    message = str(Message(message))
    if message[:4] == "link":
        message = message[4:]
    elif message[:1] == ".":
        message = message[1:]
    await send_msgs_cmd(bot, event, f"{sender_name}：\n{message}")
