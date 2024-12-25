import speedtest as speedtest
from datetime import datetime

def speedtest_ookla(source: str):
    try:
        if source == None:
            raise Exception("Source IP Address is None") 
           
        st = speedtest.Speedtest(source_address=source, secure=True)
        return {
            "server": st.get_best_server(),
            "download": st.download() / (1024 * 1024), #Byte to MB
            "upload": st.upload() / (1024 * 1024)
        }
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Ookla Speedtest Error for {source}: {str(e)}", flush=True)
        return {
            "server": "",
            "download": 0,
            "upload": 0
        }