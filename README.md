# gerrit-checkout

Fetch and checkout Gerrit changes by topic.

## Installation

```bash
pip install git+https://github.com/tpiyasek/gerrit-checkout.git
```

This will automatically install all required dependencies (rich, git, ssh).

## Usage

```bash
gerrit-checkout <topic> [--gerrit-server SERVER] [--repo PATH] [-v]
```

### Options

- `--gerrit-server`: Gerrit server hostname (default: csp-gerrit-ssh.volvocars.net)
- `--repo`: Repository path (default: current directory)
- `-v, --verbose`: Enable verbose output

### Examples

```bash
# Fetch changes for a topic
gerrit-checkout ARTCEE-10261

# From repo workspace root
cd /workspace/tpiyasek/MASTER
gerrit-checkout ARTCEE-10261

# From single git repository
cd /path/to/repo
gerrit-checkout my-topic
```

## Requirements

- Python 3.7+
- Git
- SSH access to Gerrit

## License

MIT
