import time
from storage.logger import event_logger
from storage.database import insert_command

class HoneypotShell:
    def __init__(self, session_id):
        self.session_id = session_id
        self.prompt = "root@server:~# "
        self.hostname = "server"
        self.cwd = "/root"

    def handle_command(self, cmd_line):
        cmd_line = cmd_line.strip()
        if not cmd_line:
            return ""

        parts = cmd_line.split()
        cmd = parts[0]
        
        # Log the command
        event_logger.log_event("command", {
            "session_id": self.session_id,
            "command": cmd_line
        })
        
        # Determine response
        response = ""
        response_type = "emulated"
        tactic = None

        if cmd == "ls":
            response = "snap  todo.txt  payload.sh\n"
        elif cmd == "pwd":
            response = f"{self.cwd}\n"
        elif cmd == "whoami":
            response = "root\n"
            tactic = "Discovery"
        elif cmd == "id":
            response = "uid=0(root) gid=0(root) groups=0(root)\n"
            tactic = "Discovery"
        elif cmd == "uname":
            if "-a" in parts:
                response = "Linux server 5.4.0-150-generic #167-Ubuntu SMP Mon May 20 17:33:24 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux\n"
            else:
                response = "Linux\n"
            tactic = "Discovery"
        elif cmd == "ps":
            response = "  PID TTY          TIME CMD\n    1 ?        00:00:01 systemd\n 1337 pts/0    00:00:00 bash\n 1338 pts/0    00:00:00 ps\n"
            tactic = "Discovery"
        elif cmd == "cat":
            if len(parts) > 1:
                if "todo.txt" in parts[1]:
                    response = "- Update system\n- Check logs\n- Buy milk\n"
                elif "passwd" in parts[1]:
                    response = "root:x:0:0:root:/root:/bin/bash\nuser:x:1000:1000:user:/home/user:/bin/bash\n"
                    tactic = "Discovery"
                else:
                    response = f"cat: {parts[1]}: No such file or directory\n"
            else:
                return "" # Interactive cat not fully supported
        elif cmd == "exit":
            return "EXIT"
        elif cmd in ["wget", "curl"]:
            response = f"{cmd}: command not found\n" # Safe fail, but logged
            tactic = "Command and Control"
        else:
            response = f"{cmd}: command not found\n"
            response_type = "not_found"

        insert_command({
            "session_id": self.session_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "command": cmd_line,
            "response_type": response_type,
            "mitre_tactic": tactic
        })

        return response
