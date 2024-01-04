# Living Hosts Getter

This Python script checks the availability of a list of hosts through both HTTP and HTTPS, and captures a screenshot of their corresponding web pages.

# Prerequisites

- Python
- Pip

## Installation

```bash
$ pip install requests selenium
```

## Usage

1. Update the hosts list in the data.py file with the desired list of host addresses.

2. Run the script:

```bash
python main.py
```

## Outputs

- **Screenshots**: ./screenshots/
- **Parsed Hosts**: ./hosts/
- **Hosts check**: ./hosts-check/

## Configuration

`CHECK_TIMEOUT`: Adjust the timeout for the HTTP/HTTPS request checks (in seconds). This can greatly reduce the time the script takes to complete.

`options.add_argument('--headless')`: Comment it if you want to view the browser during execution.
