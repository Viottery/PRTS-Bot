# this is test file for qq bot
import botpy
# qq_id: 3889606250, appid: 102699684 token: j8jhjCShQi2U8UJAe6TJjMm0CI2jMrKT  app_secret lXJ5rdPBxkXK7uhUI6uiWK8wlaPE3shX
import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message, DirectMessage, C2CMessage



# test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0,
              msg_id=message.id,
              content=f"收到了消息：{message.content}")
        _log.info(messageResult)
    async def on_direct_message_create(self, message: DirectMessage):
        """
        此处为处理该事件的代码
        """
        print(123321)

    async def on_c2c_message_create(self, message: C2CMessage):
        print(1211111)
        await message._api.post_c2c_message(
            openid=message.author.user_openid,
            msg_type=0, msg_id=message.id,
            content=f"我收到了你的消息：{message.content}"
        )



if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True, direct_message=True, public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid="102699684", secret="lXJ5rdPBxkXK7uhUI6uiWK8wlaPE3shX")