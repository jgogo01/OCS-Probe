import netifaces

result = {}
gateways = netifaces.gateways()
result["gateways"] = gateways

interfaces = netifaces.interfaces()
result["interfaces"] = interfaces

interface_info = {}
for interface in interfaces:
    info = netifaces.ifaddresses(interface)
    interface_info[interface] = info
    
result["interface_info"] = interface_info

print(result)