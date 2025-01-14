import iperf3
from datetime import datetime
from utils.msg_format import msg_format
def speedtest_iperf3(source: str, destination: str, duration: int, port: int):
    
    try:
        if source == None:
            raise Exception("Source IP Address is None")
        
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
        msg_format("ERROR", f"IPerf3 Speedtest Error for {destination}: {str(e)}")
        return {
            "received_Mbps": 0,
            "sent_Mbps": 0
        }
