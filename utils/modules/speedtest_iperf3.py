import iperf3
from datetime import datetime

def speedtest_iperf3(source: str, destination: str, duration: int, port: int):
    
    try:
        client = iperf3.Client()
        client.duration = duration
        client.server_hostname = destination
        client.port = port
        client.bind_address = source
        result = client.run()
        
        return {
            "received_Mbps": result.received_Mbps,
            "sent_Mbps": result.sent_Mbps
            }
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IPerf3 Speedtest Error for {destination}: {str(e)}", flush=True)
        return {
            "download": 0,
            "upload": 0
        }
