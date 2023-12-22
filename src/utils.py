
def get_cube_ip(starts_with=['192', '10'], default='localhost'):
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        for ip in adapter.ips:
            if isinstance(ip.ip, str):
                for c in starts_with:
                    if ip.ip.startswith(c):
                        return ip.ip
    return default
