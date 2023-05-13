import json
from typing import Union

from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment, Message
from nonebot_plugin_guild_patch import GuildMessageEvent

from .config import plugin_config


async def msg_rule(event: Union[GroupMessageEvent, GuildMessageEvent], enable_cmd: bool) -> bool:
    """聊天规则"""
    for link in plugin_config.group_link_guild:
        if event.self_id == link.self_id:  # 确保交给需要的bot处理
            if isinstance(event, GroupMessageEvent):
                if event.group_id == link.group_id:
                    if enable_cmd and link.group_cmd:
                        return True
                    elif not enable_cmd and not link.group_cmd:
                        return True
            elif isinstance(event, GuildMessageEvent):
                if event.guild_id == link.guild_id:
                    if enable_cmd and link.guild_cmd:
                        return True
                    elif not enable_cmd and not link.guild_cmd:
                        return True
    return False


async def msg_rule_no_cmd(event: Union[GroupMessageEvent, GuildMessageEvent]) -> bool:
    """无命令头 聊天规则"""
    return await msg_rule(event, False)


async def msg_rule_cmd(event: Union[GroupMessageEvent, GuildMessageEvent]) -> bool:
    """命令头 聊天规则"""
    return await msg_rule(event, True)


async def get_role_name(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]) -> str:
    """获取角色名"""
    role_name = ""
    if isinstance(event, GroupMessageEvent):
        if event.sender.role == "owner":
            role_name = "[群主]"
        elif event.sender.role == "admin":
            role_name = "[管理员]"
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
            role_name = "[超级管理员]"
    return role_name


async def get_message(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    """获取message列表"""
    sender_name = await get_member_nickname(bot, event, event.user_id)
    if plugin_config.display_role:
        role_name = await get_role_name(bot=bot, event=event)
    else:
        role_name = ""

    message = [MessageSegment.text(f"{role_name}{sender_name} 说：\n")]

    for msg in event.message:
        # 文本
        # 视频
        if msg.type == "video":
            msgData = MessageSegment.video(msg.data['url'])
            message.append(msgData)

            await send_msgs(event=event, result=f"{sender_name} 发送了视频消息：")
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
        # redbag
        elif msg.type == "redbag":
            msgData = MessageSegment.text('[QQ红包]')
        # json
        elif msg.type == "json":
            json_data = msg.data["data"]
            print(json_data)
            print("==============")
            print(json.loads(json_data))

            data = str(msg.data["data"]) if isinstance(event, GroupMessageEvent) else str(msg.data["data"]).replace(
                "\\\\", "\\")
            msgData = MessageSegment.json(json.loads(json_data))
            message.append(msgData)

            await send_msgs(event=event, result=f"{sender_name} 发送了卡片消息：")
            return message
        else:
            msgData = MessageSegment.text(msg.type)
        message.append(msgData)
    return message


async def send_msgs(event: Union[GroupMessageEvent, GuildMessageEvent], result: Union[str, Message, MessageSegment]):
    """发送消息"""
    for link in plugin_config.group_link_guild:
        if bot := get_bot(str(link.self_id)):
            if isinstance(event, GroupMessageEvent):
                if event.group_id == link.group_id:
                    await bot.send_guild_channel_msg(
                        guild_id=link.guild_id,
                        channel_id=link.channel_id,
                        message=result
                    )
            elif isinstance(event, GuildMessageEvent):
                await bot.send_group_msg(group_id=link.group_id, message=result)


async def get_member_nickname(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent], user_id) -> str:
    """获取昵称"""
    # 判断从 群/频道 获取成员信息
    if isinstance(event, GroupMessageEvent):
        # 如果获取发送者的昵称
        if event.user_id == int(user_id):
            # 如果群名片为空，则发送昵称
            return event.sender.card or event.sender.nickname
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
