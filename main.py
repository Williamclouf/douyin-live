import logging
from src import dy_live
from src.utils.common import init_global
from src.utils.http_send import send_start


if __name__ == "__main__":
    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.ERROR)

    # 初始化要做的事情：比如初始化全局变量
    # init_global()

    # 推送直播点赞等数据
    # send_start()

    LIVE_ROOM_URL = "https://live.douyin.com/2434238838"
    print(dy_live.parseLiveRoomUrl_new(LIVE_ROOM_URL))
