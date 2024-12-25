import icmplib

def ping_ipv4(source: str, destination: str, count: int):
    try:
        if source == None:
            raise Exception("Source IP Address is None") 
           
        result = icmplib.ping(source=source, count=count, address=destination)
        return {
            "minRTT": result.min_rtt,
            "maxRTT": result.max_rtt,
            "avgRTT": result.avg_rtt,
            "packetLoss": result.packet_loss,
            "packetsReceived": result.packets_received,
            "packetsSent": result.packets_sent
        }
    except Exception as e:
        print(f"ICMP Error for {destination}: {str(e)}", flush=True)
        return {
            "minRTT": 0,
            "maxRTT": 0,
            "avgRTT": 0,
            "packetLoss": 100,
            "packetsReceived": 0,
            "packetsSent": 0
        }