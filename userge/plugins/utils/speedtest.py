# Copyright (C) 2020-2021 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os
import wget
import speedtest
from userge import userge, Message, pool
from userge.utils import humanbytes

CHANNEL = userge.getCLogger(__name__)


@userge.on_cmd("speed", about={'header': "test your server speed"})
async def speedtst(message: Message):
    await message.edit("`Tes kecepatan server . . .`")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
#        await message.try_to_edit("`Melakukan tes unduhan . . .`")
        test.download()
#        await message.try_to_edit("`Melakukan tes unggah . . .`")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await message.err(text=e)
        return
    path = await pool.run_in_thread(wget.download)(result['share'])
    output = f"""📡 ISP: `{result['client']['isp']}`
🌏 Country: `{result['client']['country']}`
📍Ping: `{result['ping']}`
📥 Download: `{humanbytes(result['download'])}/s`
📤 Upload: `{humanbytes(result['upload'])}/s`**"""
    await CHANNEL.fwd_msg(msg)
    os.remove(path)
    await message.delete()
