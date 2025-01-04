import netifaces

def get_ip_addresses(interface_name):
    try:
        addrs = netifaces.ifaddresses(interface_name)
        
        ipv4 = addrs[netifaces.AF_INET][0]['addr'] if netifaces.AF_INET in addrs else None
        ipv6 = None
        if netifaces.AF_INET6 in addrs:
            for addr in addrs[netifaces.AF_INET6]:
                if 'addr' in addr:
                    current_ipv6 = addr['addr']
                    # Link-local (fe80::) and ULA (fc00:: หรือ fd00::)
                    if not (current_ipv6.startswith('fe80:') or 
                           current_ipv6.startswith('fc00:') or 
                           current_ipv6.startswith('fd00:')):
                        ipv6 = current_ipv6
                        break
                    
        return {
            "IPv4": ipv4,
            "IPv6": ipv6
        }
            
    except ValueError:
        print(f"Interface {interface_name} not found", flush=True)
    except Exception as e:
        print(f"Error: {str(e)}", flush=True)
        
    return None, None