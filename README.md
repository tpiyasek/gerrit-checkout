# gerrit-checkout

CLI tool to fetch and checkout Gerrit changes related to a Topic into your local Git workspace.

## Installation

### From GitHub (pip)

```bash
pip install git+https://github.com/yourusername/gerrit-checkout.git
```

### From source

```bash
git clone https://github.com/yourusername/gerrit-checkout.git
cd gerrit-checkout
pip install -e .
```

## Usage

```bash
gerrit-checkout <topic> [options]
```

### Options

- `--gerrit-url URL`: Gerrit instance URL (default: https://gerrit.example.com)
- `--repo PATH`: Git repository path (default: current directory)
- `-v, --verbose`: Enable verbose output

### Examples

```bash
# Fetch changes for a topic
gerrit-checkout my-feature --gerrit-url https://gerrit.mycompany.com

# Use current directory
gerrit-checkout my-feature --repo .

# Enable verbose output
gerrit-checkout my-feature -v
```

## Development

### Setup development environment

```bash
git clone https://github.com/yourusername/gerrit-checkout.git
cd gerrit-checkout
pip install -e .
```

### Requirements

- Python 3.7+

## License

MIT License - see [LICENSE](LICENSE) file for details
