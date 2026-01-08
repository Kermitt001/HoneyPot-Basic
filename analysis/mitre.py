
# Map simple keywords to MITRE ATT&CK Techniques
PATTERNS = {
    "wget": ("T1105", "Ingress Tool Transfer"),
    "curl": ("T1105", "Ingress Tool Transfer"),
    "whoami": ("T1033", "System Owner/User Discovery"),
    "id": ("T1033", "System Owner/User Discovery"),
    "uname": ("T1082", "System Information Discovery"),
    "ps": ("T1057", "Process Discovery"),
    "cat /etc/passwd": ("T1003", "OS Credential Dumping"),
    "cat /etc/shadow": ("T1003", "OS Credential Dumping"),
    "ssh": ("T1021", "Remote Services"),
}

def analyze_command(cmd: str):
    """
    Returns (TacticID, Name) if match found, else None
    """
    for keyword, (tid, name) in PATTERNS.items():
        if keyword in cmd:
            return tid, name
    return None, None
