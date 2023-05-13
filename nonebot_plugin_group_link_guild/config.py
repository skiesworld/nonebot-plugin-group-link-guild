from typing import Optional, List

from nonebot import get_driver
from pydantic import BaseModel, Extra, Field


class PerLink(BaseModel):
    """每个链接的配置"""
    group_id: int
    group_cmd: Optional[str] = ""
    guild_id: int
    channel_id: int
    guild_cmd: Optional[str] = ""
    self_id: int


class Config(BaseModel, extra=Extra.ignore):
    group_link_guild: List[PerLink] = Field(default_factory=list)
    display_role: Optional[bool] = False


plugin_config: Config = Config.parse_obj(get_driver().config)
