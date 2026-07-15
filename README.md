# python-for-devops

## Purpose

This repository is dedicated to demonstrating fluency and competency with
Python to solve tasks that are asked of a DevOps engineer. I am creating
this to sharpen my sword while simultaneously making my life easier in my
own homelab environment, task by task. Each script has a clearly defined
purpose and use case that makes me stronger and improves efficiency.

Every script here runs against my real infrastructure — a Proxmox-based
homelab with a 6-node Kubernetes cluster, ~30 LXCs and VMs, and the
supporting network services. No toy data.

## Philosophy

- **Real inputs over tutorials.** Every script consumes data from my actual
  fleet. If it doesn't work on real infrastructure, it sadly won't make the cut.
- **Ship every session.** One session, one runnable script, one commit.
  Ship ugly, refactor next session.
- **CLI-first.** Every script supports `--help` and behaves like a proper
  Unix tool: clean errors to stderr, meaningful exit codes.
- **Minimal dependencies.** Standard library where possible. The one
  exception so far is `pyyaml` — Python has no stdlib YAML parser, and
  YAML is the lingua franca of the infrastructure I manage.

## How to run

Each script is standalone. From the repo root:

python3 01_server_inventory.py --help

Requires Python 3.11+ and `pyyaml`. If `python3 -c "import yaml"` fails,
install it in a venv (`uv add pyyaml` or `pip install pyyaml` in a venv —
never system-wide).

## Scripts

| # | Script | Purpose |
|---|--------|---------|
| 01 | `01_server_inventory.py` | Reads `hosts.yml` and prints a fleet report grouped by role |

## hosts.yml schema

`hosts.yml` is the canonical inventory for this repo — every script that
needs to know about the fleet reads this file. One entry per host:

- `name` — unique hostname (lowercase, no spaces)
- `ip` — primary IPv4 address
- `role` — functional grouping key, always a lowercase slug
  (`k8s-worker`, `dns`, `media-acquisition`). Scripts group and filter
  on this field, so consistency matters more than descriptiveness.
- `os` — base OS as a slug (`ubuntu`, `debian`, `rocky-linux`, `freebsd`)
- `distro_version` — version string, always quoted (unquoted `15.0`
  parses as a float and breaks string handling)
- `purpose` — one line of human-readable prose describing the host's job
- `notes` — free text: virtualization type, hardware, and any
  intentional anomalies (e.g. hosts on isolated VLANs are marked as such
  so the inventory explains itself)

Conventions: machine-read fields (`name`, `role`, `os`) are slugs;
prose lives only in `purpose` and `notes`.