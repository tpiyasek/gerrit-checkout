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

- `--gerrit-server`: Gerrit server hostname (default: gerrit.neo.volvocars.net)
- `--repo`: Repository path (default: current directory)
- `--init-config`: Create `~/.gerrit-checkout.cfg` with default values
- `-v, --verbose`: Enable verbose output

### Config file

`--init-config` creates this file:

```ini
[gerrit]
server = gerrit.neo.volvocars.net
repo_path = .
```

If the config file already exists, the command keeps the current file and exits.

### Examples

```bash
# From repo workspace root
cd /path/to/repo-workspace
gerrit-checkout ARTCEE-10261

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
