import netifaces

def get_ip_addresses(interface_name):
    try:
        addrs = netifaces.ifaddresses(interface_name)
        
        ipv4 = addrs[netifaces.AF_INET][0]['addr'] if netifaces.AF_INET in addrs else None
        ipv6 = addrs[netifaces.AF_INET6][0]['addr'] if netifaces.AF_INET6 in addrs else None
            
        return {
            "IPv4": ipv4,
            "IPv6": ipv6
        }
            
    except ValueError:
        print(f"Interface {interface_name} not found", flush=True)
    except Exception as e:
        print(f"Error: {str(e)}", flush=True)
        
    return None, None