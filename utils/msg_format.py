from datetime import datetime
from zoneinfo import ZoneInfo

def msg_format(info, msg):
    thai_time = datetime.now(ZoneInfo('Asia/Bangkok'))
    print(f"{thai_time.strftime('%Y-%m-%d %H:%M:%S')} {info}: {msg}", flush=True)
    