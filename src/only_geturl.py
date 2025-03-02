import re
import requests
import json
import logging

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"


def request_liveroom(url):
    """
    解析直播的弹幕websocket地址
    :param url:直播地址
    :return:
    """
    headers = {
        "authority": "live.douyin.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "xgplayer_user_id=251959789708; passport_assist_user=Cj1YUtyK7x-Br11SPK-ckKl61u5KX_SherEuuGPYIkLjtmV3X8m3EU1BAGVoO541Sp_jwUa8lBlNmbaOQqheGkoKPOVVH42rXu6KEb9WR85pUw4_qNHfbcotEO-cml5itrJowMBlYXDaB-GDqJwNMxMElMoZUycGhzdNVAT4XxCJ_74NGImv1lQgASIBA3Iymus%3D; n_mh=nNwOatDm453msvu0tqEj4bZm3NsIprwo6zSkIjLfICk; LOGIN_STATUS=1; store-region=cn-sh; store-region-src=uid; sid_guard=b177a545374483168432b16b963f04d5%7C1697713285%7C5183999%7CMon%2C+18-Dec-2023+11%3A01%3A24+GMT; ttwid=1%7C9SEGPfK9oK2Ku60vf6jyt7h6JWbBu4N_-kwQdU-SPd8%7C1697721607%7Cc406088cffa073546db29932058720720521571b92ba67ba902a70e5aaffd5d6; odin_tt=1f738575cbcd5084c21c7172736e90f845037328a006beefec4260bf8257290e2d31b437856575c6caeccf88af429213; __live_version__=%221.1.1.6725%22; device_web_cpu_core=16; device_web_memory_size=8; live_use_vvc=%22false%22; csrf_session_id=38b68b1e672a92baa9dcb4d6fd1c5325; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; __ac_nonce=0658d6780004b23f5d0a8; __ac_signature=_02B4Z6wo00f01Klw1CQAAIDAXxndAbr7OHypUNCAAE.WSwYKFjGSE9AfNTumbVmy1cCS8zqYTadqTl8vHoAv7RMb8THl082YemGIElJtZYhmiH-NnOx53mVMRC7MM8xuavIXc-9rE7ZEgXaA13; webcast_leading_last_show_time=1703765888956; webcast_leading_total_show_times=1; webcast_local_quality=sd; xg_device_score=7.90435294117647; live_can_add_dy_2_desktop=%221%22; msToken=sTwrsWOpxsxXsirEl0V0d0hkbGLze4faRtqNZrIZIuY8GYgo2J9a0RcrN7r_l179C9AQHmmloI94oDvV8_owiAg6zHueq7lX6TgbKBN6OZnyfvZ6OJyo2SQYawIB_g==; tt_scid=NyxJTt.vWxv79efmWAzT2ZAiLSuybiEOWF0wiVYs5KngMuBf8oz5sqzpg5XoSPmie930; pwa2=%220%7C0%7C1%7C0%22; download_guide=%223%2F20231228%2F0%22; msToken=of81bsT85wrbQ9nVOK3WZqQwwku95KW-wLfjFZOef2Orr8PRQVte27t6Mkc_9c_ROePolK97lKVG3IL5xrW6GY6mdUDB0EcBPfnm8-OAShXzlELOxBBCdiQYIjCGpQ==; IsDouyinActive=false; odin_tt=7409a7607c84ba28f27c62495a206c66926666f2bbf038c847b27817acbdbff28c3cf5930de4681d3cfd4c1139dd557e; ttwid=1%7C9SEGPfK9oK2Ku60vf6jyt7h6JWbBu4N_-kwQdU-SPd8%7C1697721607%7Cc406088cffa073546db29932058720720521571b92ba67ba902a70e5aaffd5d6",
        "referer": "https://live.douyin.com/721566130345?cover_type=&enter_from_merge=web_live&enter_method=web_card&game_name=&is_recommend=&live_type=game&more_detail=&room_id=7317569386624125734&stream_type=vertical&title_type=&web_live_tab=all",
        "upgrade-insecure-requests": "1",
        "user-agent": USER_AGENT,
    }
    res = requests.get(url=url, headers=headers)
    return res


def get_video_url(res: str):
    """

    Args:
        res (str): Response text

    """

    # 获取m3u8直播流地址：m3u8直播比flv延迟2秒左右
    res_stream = re.search(r'hls_pull_url_map\\":(\{.*?})', res)
    res_stream_m3u8s = json.loads(res_stream.group(1).replace('\\"', '"'))
    # HD1和FULL_HD1随机获取，优先获取FULL_HD1
    res_m3u8_hd1 = res_stream_m3u8s.get("FULL_HD1", "").replace("http", "https")
    if not res_m3u8_hd1:
        res_m3u8_hd1 = res_m3u8_hd1.get("HD1", "").replace("http", "https")
    logger.info(f"直播流m3u8链接地址是: {res_m3u8_hd1}")

    # 找到flv直播流地址:区分标清|高清|蓝光
    res_flv_search = re.search(r'flv\\":\\"(.*?)\\"', res)
    res_stream_flv = (
        res_flv_search.group(1).replace('\\"', '"').replace("\\\\u0026", "&")
    )
    if "https" not in res_stream_flv:
        res_stream_flv = res_stream_flv.replace("http", "https")
    logger.info(f"直播流FLV地址是: {res_stream_flv}")

    return {
        "m3u8": res_m3u8_hd1,
        "flv": res_stream_flv,
    }


def parseLiveRoomUrl_new(url):
    res = request_liveroom(url)
    return get_video_url(res.text)


if __name__ == "__main__":
    LIVE_ROOM_URL = "https://live.douyin.com/2434238838"
    print(parseLiveRoomUrl_new(LIVE_ROOM_URL))
