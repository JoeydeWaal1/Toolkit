from rich import print
from rich.panel import Panel
import json

file = False


def log_init(text):
    if file is not None:
        return
    print("[bold green][SYS][/bold green]  " + text)

def log_info(text):
    if file:
        return
    print(f"[bold green][INFO] [/bold green]{text}")
    pass

def log_error(text):
    if file is not None:
        with open(file, "w") as f:
            f.write(text)
        return
    print(f"[bold red][SYS] {text}[/bold red]")

def log_json(json_object):
    if file is not None:
        write_json(json_object)
        return
    print(Panel.fit(json.dumps(json_object, indent=2)))

def write_json(data):
    with open(file, "w") as f:
        f.write(json.dumps(data, indent=4))

def set_q(filename):
    global file
    file = filename
