"""Read a YAML host inventory and print a fleet report grouped by role.


Usage: python3 01_server_inventory.py [--file hosts.yml]
"""
import argparse
import sys
import yaml

def load_inventory(path: str) -> dict:
    """Load and parse the YAML file, exiting cleanly if it's missing or broken"""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"error: inventory file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"error: invalid YAML in {path}: {e}", file=sys.stderr)
        sys.exit(1)

def group_by_role(hosts: list) -> dict:
    """Bucket hosts by role so the report can print one section per role."""
    by_role = {}
    for host in hosts:
        by_role.setdefault(host["role"], []).append(host)
    return by_role

def print_report(data: dict) -> None:
    """Human-readable stdout report — the whole point of the script."""
    hosts = data["hosts"]
    by_role = group_by_role(hosts)
    print(f"FLEET INVENTORY — {len(hosts)} hosts, {len(by_role)} roles\n")
    for role, members in by_role.items():
        print(f"== {role} ({len(members)}) ==")
        for h in members:
            notes = (h.get("notes") or "")[:40]
            line = f"  {h['name']:<20}{h['ip']:<16}{h['os']:<14}{notes}"
            print(line.rstrip())
        print()


def main() -> None:
    """Parse CLI args and run the report."""
    parser = argparse.ArgumentParser(description="Print a fleet report from a YAML inventory.")
    parser.add_argument("--file", default="hosts.yml", help="path to inventory YAML")
    args = parser.parse_args()
    print_report(load_inventory(args.file))


if __name__ == "__main__":
    main()