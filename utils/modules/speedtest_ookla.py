import speedtest as speedtest
from datetime import datetime

def speedtest_ookla(source: str):
    try:
        st = speedtest.Speedtest(source_address=source, secure=True)
        return {
            "server": st.get_best_server(),
            "download": st.download(),
            "upload": st.upload()
        }
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Ookla Speedtest Error for {source}: {str(e)}", flush=True)
        return {
            "download": 0,
            "upload": 0
        }