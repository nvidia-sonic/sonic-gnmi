import argparse
import json


def ip2int(ip):
    return sum(int(v) * 256 ** (3 - i) for i, v in enumerate(ip.split(".")))

def int2ip(number):
    result = []
    for i in range(4):
        number, mod = divmod(number, 256)
        result.insert(0, mod)
    return ".".join(str(i) for i in result)

def generate_route(num):
    ret = {}
    ip = "10.0.50.1"
    pos = ip2int(ip)
    for i in range(num):
        pos += 1
        key = "F4939FEFC47E:" + int2ip(pos) + "/32"
        data = {"action_type":"vnet", "vnet":"Vnet%07d"%i}
        ret[key] = data
    return ret

def generate_mapping(num):
    ret = {}
    ip = "10.0.50.1"
    pos = ip2int(ip)
    for i in range(num):
        pos += 1
        key = "Vnet%07d:"%i + int2ip(pos)
        data = {"routing_type":"vnet_encap", "underlay_ip":"2601:12:7a:1::1234", "mac_address":"F9-22-83-99-22-A%d"%(i%10)}
        ret[key] = data
    return ret

def main():
    parser = argparse.ArgumentParser(description="Generate DASH_ROUTE_TABLE and DASH_VNET_MAPPING_TABLE")
    parser.add_argument('--table', default="DASH_ROUTE_TABLE")
    parser.add_argument('--num', default=1000, type=int)
    args = parser.parse_args()

    if args.num <= 0:
        return
    if args.table == "DASH_ROUTE_TABLE":
        output = generate_route(args.num)
    elif args.table == "DASH_VNET_MAPPING_TABLE":
        output = generate_mapping(args.num)
    else:
        raise Exception("Invalid table %s"%args.table)
    
    print(json.dumps(output))

if __name__ == '__main__':
    main()

