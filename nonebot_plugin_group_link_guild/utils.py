from typing import Union

from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot_plugin_guild_patch import GuildMessageEvent

group_role = {
    "owner": "[群主]",
    "admin": "[管理员]",
    "member": ""
}
"""群角色字典"""


def get_group_list() -> list:
    """获取 互通群聊列表"""
    try:
        return list(get_driver().config.group_guild_list)
    except AttributeError:
        return []


def get_group_role() -> bool:
    """获取 是否发送群聊头衔"""
    try:
        return bool(get_driver().config.group_guild_role)
    except AttributeError:
        return False


group_list = get_group_list()
"""互通群列表"""


async def msg_rule(event: Union[GroupMessageEvent, GuildMessageEvent]) -> bool:
    """聊天规则"""
    if isinstance(event, GroupMessageEvent):
        for group in group_list:
            if event.group_id == int(group["group"]):
                return True
    elif isinstance(event, GuildMessageEvent):
        # 返回频道成员昵称
        for group in group_list:
            if f"{event.guild_id}:{event.channel_id}" == group["guild"]:
                return True
    return False


async def get_role_name(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]) -> str:
    """获取角色名"""
    role_name = ""
    if isinstance(event, GroupMessageEvent):
        role_name = group_role[event.sender.role]
    elif isinstance(event, GuildMessageEvent):
        roles = set(
            role["role_id"]
            for role in (
                await bot.get_guild_member_profile(
                    guild_id=event.guild_id, user_id=event.user_id
                )
            )["roles"]
        )
        if "4" in roles:
            role_name = "[频道主]"
        elif "2" in roles:
            role_name = "[管理员]"
    return role_name


async def get_message(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    """获取message列表"""
    sender_name = await get_member_nickname(bot, event, event.user_id)
    if get_group_role():
        sender_name = await get_role_name(bot=bot, event=event) + sender_name
    message = []
    for msg in event.message:
        # 文本
        # 视频
        if msg.type == "video":
            msgData = MessageSegment.video(msg.data['url'])
            message.append(msgData)
            sender_name = await get_member_nickname(bot, event, event.user_id)
            await bot.send_msgs(bot, event, f"{sender_name} 发送了视频消息：")
            return message
        elif msg.type == "text":
            msgData = MessageSegment.text(msg.data['text'])
        # 图片
        elif msg.type == "image":
            msgData = MessageSegment.image(msg.data['url'])
        # 表情
        elif msg.type == "face":
            msgData = MessageSegment.face(int(msg.data['id']))
        # 语音
        elif msg.type == "record":
            msgData = MessageSegment.text('[语音]')
            # @
        elif msg.type == "at":
            # 获取被@ 群/频道 昵称
            at_member_nickname = await get_member_nickname(bot, event, msg.data['qq'])
            msgData = MessageSegment.text(f"@{at_member_nickname}")
        # share
        elif msg.type == "share":
            msgData = MessageSegment.share(url=msg.data['url'], title=msg.data['title'])
        # forward
        elif msg.type == "forward":
            msgData = MessageSegment.text('[合并转发]')
        else:
            msgData = MessageSegment.text(msg.type)
        message.append(msgData)
    return sender_name, message


async def send_msgs(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent], result):
    """发送消息"""
    if isinstance(event, GroupMessageEvent):
        for group in group_list:
            if event.group_id == int(group["group"]) and not group["group_cmd"]:
                await bot.send_guild_channel_msg(
                    guild_id=group["guild"][:group["guild"].find(":")],
                    channel_id=group["guild"][group["guild"].find(":") + 1:],
                    message=result
                )
    else:
        for group in group_list:
            if f"{event.guild_id}:{event.channel_id}" == group["guild"] and not group["guild_cmd"]:
                await bot.send_group_msg(group_id=int(group["group"]), message=result)


async def send_msgs_cmd(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent], result):
    """发送消息"""
    if isinstance(event, GroupMessageEvent):
        for group in group_list:
            if event.group_id == int(group["group"]):
                await bot.send_guild_channel_msg(
                    guild_id=group["guild"][:group["guild"].find(":")],
                    channel_id=group["guild"][group["guild"].find(":") + 1:],
                    message=result
                )
    else:
        for group in group_list:
            if f"{event.guild_id}:{event.channel_id}" == group["guild"]:
                await bot.send_group_msg(group_id=int(group["group"]), message=result)


async def get_member_nickname(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent], user_id) -> str:
    """获取昵称"""
    # 判断从 群/频道 获取成员信息
    if isinstance(event, GroupMessageEvent):
        # 如果获取发送者的昵称
        if event.user_id == int(user_id):
            # 如果群名片为空，则发送昵称
            if event.sender.card == "":
                return event.sender.nickname
            # 如果群名片不为空，发送群名片
            else:
                return event.sender.card
        # 如果获取其他人的昵称
        else:
            return (await bot.get_group_member_info(
                group_id=event.group_id,
                user_id=user_id,
                no_cache=True
            ))['nickname']
    elif isinstance(event, GuildMessageEvent):
        # 返回频道成员昵称
        if event.user_id == user_id:
            return event.sender.nickname
        else:
            return (await bot.get_guild_member_profile(
                guild_id=event.guild_id,
                user_id=user_id))['nickname']
