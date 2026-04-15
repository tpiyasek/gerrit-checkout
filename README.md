# gerrit-checkout

Fetch and checkout Gerrit changes by topic.

## Installation

```bash
pip install git+https://github.com/tpiyasek/gerrit-checkout.git
```

Python dependency (`rich`) is installed by pip. `git` and `ssh` must be available on your system.

## Usage

```bash
gerrit-checkout --init-config
gerrit-checkout <topic> [--gerrit-server SERVER] [--repo PATH] [-v]
```

### Options

- `--gerrit-server`: Gerrit server hostname (overrides config for this run only)
- `--repo`: Repository path (default: current directory)
- `--init-config`: Create `~/.gerrit-checkout.cfg` with default values
- `-v, --verbose`: Enable verbose output

Server value precedence:

1. `--gerrit-server` (CLI override, current run only)
2. `~/.gerrit-checkout.cfg` -> `[gerrit].server`

If no server is set in either place, the command exits with an error.

Note: `gerrit.exsample-com` in the config template below is a sample only. Update it to your actual Gerrit hostname.

### Config file

`--init-config` creates this file:

```ini
[gerrit]
server = gerrit.exsample-com
repo_path = .
```

After creating the file, set `server` to your Gerrit hostname before running checkout.

If the config file already exists, the command keeps the current file and exits.

### Examples

```bash
# From repo workspace root
cd /path/to/repo-workspace
gerrit-checkout ARTXXX-12345

# Create default config once (optional)
gerrit-checkout --init-config

```

## Requirements

- Python 3.7+
- Git
- SSH access to Gerrit

## Uninstall

```bash
python3 -m pip uninstall -y gerrit-checkout && rm -f ~/.gerrit-checkout.cfg
```

## License

MIT
