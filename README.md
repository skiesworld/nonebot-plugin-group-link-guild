# nonebot-plugin-group-link-guild

互通QQ群聊与QQ频道消息的插件

## 可同步消息类型

- 文本
- 表情
- 图片
- 视频
- @

未支持的类型将被转为：`[消息类型]`，如：`[语音]`、`[json]` 等等

## 安装

- 脚手架安装
    ```shell
    pip install nonebot-plugin-group-link-guild
    ```
  在 `pyproject.toml` 中启用插件


- NB商店安装
    ```shell
    nb plugin install nonebot-plugin-group-link-guild
    ```

## 配置

```json
# 互通的群与频道列表
group_link_guild = '[
    {
        "group_id": 123456789,
        "group_cmd": ".",
        "guild_id": 123456789098765,
        "channel_id": 2356423,
        "guild_cmd": "#",
        "self_id": 123456789
    }
]'

# 是否发送头衔，仅支持：[群主]、[管理员]、[频道主]、[超级管理员]
display_role = true
```

## 使用

当配置中 `xxx_cmd` 为 `任意命令前缀`

在本群聊中需要使用 `设置的命令前缀` + 消息 才能发送消息

## 特别感谢

- [NoneBot2](https://github.com/nonebot/nonebot2)： 插件使用的开发框架。
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)： 稳定完善的 CQHTTP 实现。

## 许可证

本项目使用 [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) 作为开源许可证。
