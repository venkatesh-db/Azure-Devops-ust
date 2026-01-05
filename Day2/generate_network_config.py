# Python script to dynamically generate network configurations

import json
import argparse

def generate_network_config(subnet_count, cidr_prefix):
    """Generate dynamic network configuration."""
    network_config = {
        "vnet": {
            "name": "vnet-dynamic",
            "address_space": f"10.{cidr_prefix}.0.0/16",
            "subnets": []
        }
    }

    for i in range(subnet_count):
        subnet = {
            "name": f"subnet-{i+1}",
            "address_prefix": f"10.{cidr_prefix}.{i}.0/24"
        }
        network_config["vnet"]["subnets"].append(subnet)

    return network_config

def main():
    parser = argparse.ArgumentParser(description="Generate dynamic network configurations.")
    parser.add_argument("--subnet-count", type=int, required=True, help="Number of subnets to create.")
    parser.add_argument("--cidr-prefix", type=int, required=True, help="CIDR prefix for the virtual network.")

    args = parser.parse_args()

    config = generate_network_config(args.subnet_count, args.cidr_prefix)
    print(json.dumps(config, indent=4))

if __name__ == "__main__":
    main()