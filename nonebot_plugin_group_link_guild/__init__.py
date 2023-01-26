from typing import Union

from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message
from nonebot_plugin_guild_patch import GuildMessageEvent

from .utils import (
    get_group_list,
    msg_rule,
    get_member_nickname,
    get_group_role,
    get_role_name,
    send_msgs,
    get_message
)

nonebot_plugin_group_link_guild = on_message(rule=msg_rule)


@nonebot_plugin_group_link_guild.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    sender_name = await get_member_nickname(bot, event, event.user_id)
    if get_group_role():
        sender_name = await get_role_name(bot=bot, event=event) + sender_name
    await send_msgs(bot, event, f"{sender_name}：\n{Message(await get_message(bot, event))}")
