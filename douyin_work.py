import requests
from pprint import pprint
import json
import aiohttp
import asyncio
import os
from typing import TypeAlias, IO, BinaryIO, TextIO
import re
from loguru import logger
from urllib.parse import unquote
import time
VIDEO_URL: TypeAlias = str

# 定义颜色常量
RESET = "\033[0m"  # 重置颜色
BOLD = "\033[1m"  # 加粗
UNDERLINE = "\033[4m"  # 下划线
BLACK = "\033[30m"  # 黑色
RED = "\033[31m"  # 红色
GREEN = "\033[32m"  # 绿色
YELLOW = "\033[33m"  # 黄色
BLUE = "\033[34m"  # 蓝色
MAGENTA = "\033[35m"  # 品红
CYAN = "\033[36m"  # 青色
WHITE = "\033[37m"  # 白色

p_cookies = {

}

p_headers = {
    
}

p_params = {
    
}


w_cookies = {
    
}

w_headers = {
    
}

w_params = {
    
}

async def custom_func(src:VIDEO_URL, save_path:str, cnt:int) -> BinaryIO:
    # print(src)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=src, headers=w_headers, params=w_params, cookies=w_cookies) as response:
            response_content = await response.read()
            with open(f"{save_path}//{cnt}.mp4", mode='wb') as f:
                f.write(response_content)

    # video_content = requests.get(url=src, headers=w_headers, cookies=w_cookies).content
    # with open('a.mp4', mode='wb') as f:
    #     f.write(video_content)

async def get_addr(aweme_id:str, url:str, cnt:int) -> BinaryIO:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=w_params, headers=w_headers, cookies=w_cookies) as response:
            response_text = await response.text()
            # print(response_text)
            json_dict = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', response_text)[0]
            # pprint(json_dict)
            a = json.loads(unquote((json_dict)))
            video_url =  a['app']['videoDetail']['video']['bitRateList'][0]['playAddr'][1]
            await custom_func(**video_url, save_path="store", cnt=cnt)

cnt = 0
async def batch_req(sec_user_id):
    P_params = p_params.copy()
    while True:
        global cnt
        response = requests.get('https://www.douyin.com/aweme/v1/web/aweme/post/', params=P_params, cookies=p_cookies, headers=p_headers)
        max_cursor = json.loads(response.text)['max_cursor']
        P_params['max_cursor'] = max_cursor
        # pprint(json.loads(response.text))
        nickname = json.loads(response.text)['aweme_list'][0]['author']['nickname']
        # print(nickname)
        # break
        for idx in json.loads(response.text)['aweme_list']:
            aweme_id = idx['aweme_id']
            desc = idx['desc']
            # print(aweme_id)
            cnt += 1
            w_params['modal_id'] = aweme_id
            url = f"https://www.douyin.com/user/{sec_user_id}?from_tab_name=main&modal_id={aweme_id}&vid=7496658529341050112"
            await get_addr(aweme_id, url, cnt)
            logger.info(f">>>>>{CYAN}{nickname}{RESET}的第{cnt}个作品：{BLUE}{desc}{RESET}---------下载完成")
        if not json.loads(response.text)['has_more']:
            break


    
async def main():
    p_params['sec_user_id'] = 'MS4wLjABAAAAiEdTJStt_v5pqfD1SmXNy__FzyM9fYwUARoeouw9zII'
    await batch_req(p_params['sec_user_id'])

asyncio.run(main())





















