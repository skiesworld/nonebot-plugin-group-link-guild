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
# 互通的群与频道列表，因 NoneBot读取配置文件问题，请填写完毕之后缩减至一行
GROUP_GUILD_LIST=[
  {
    "group_cmd": false,
    "guild_cmd": false,
    "group": "群号1",
    "guild": "频道A ID:子频道A ID"
  },
  {
    "group_cmd": false,
    "guild_cmd": false,
    "group": "群号2",
    "guild": "频道B ID:子频道B ID"
  }
]

# 是否发送头衔，仅支持：[群主]、[管理员]、[频道主]
GROUP_GUILD_ROLE=true
```

## 使用

当配置中 `xxx_cmd` 为 `true`

在本群聊中需要使用命令前缀 `link` 或 `.` + 消息 才能发送消息

## 特别感谢

- [NoneBot2](https://github.com/nonebot/nonebot2)： 插件使用的开发框架。
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)： 稳定完善的 CQHTTP 实现。

## 许可证

本项目使用 [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) 作为开源许可证。
