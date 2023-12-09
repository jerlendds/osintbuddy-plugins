#!/usr/bin/env python
"""OSINTBuddy plugins server script

This script contains the commands needed to manage an OSINTBuddy Plugins service, which is used by the OSINTBuddy project.

Basic Commands:
    Plugins service command(s):
        `start` : Starts the FastAPI microservice (`ctrl+c` to stop the microservice)
        `lsp` : Start the language server for code completion in the OSINTBuddy app
    Database Command(s):
        `plugin create` : Run the setup wizard for creating new plugin(s)
        `load $GIT_URL` : Load plugin(s) from a remote git repository
"""

from os import getpid, devnull
from argparse import ArgumentParser, BooleanOptionalAction
from pyfiglet import figlet_format
from termcolor import colored
import osintbuddy

APP_INFO = \
"""____________________________________________________________________
| Find, share, and get help with OSINTBuddy plugins:
| https://forum.osintbuddy.com/c/plugin-devs/5
|___________________________________________________________________
| If you run into any bugs, please file an issue on Github:
| https://github.com/jerlendds/osintbuddy
|___________________________________________________________________
|
| OSINTBuddy plugins: v{osintbuddy_version}
| PID: {pid}
| Endpoint: 0.0.0.0:42562 
""".rstrip()


def _print_server_details():
    print(colored(figlet_format(f"OSINTBuddy plugins", font='smslant'), color="blue"))
    print(colored(APP_INFO.format(
        osintbuddy_version=osintbuddy.__version__,
        pid=getpid(),
    ), color="blue"))
    colored("Created by", color="blue"), colored("jerlendds", color="red")


def _print_lsp_details():
    import jedi_language_server
    print(colored(figlet_format(f"OSINTBuddy LSP", font='smslant'), color="blue"))
    colored("Created by", color="blue"), colored("jerlendds", color="red")
    print(colored(f"""____________________________________________________________________
| Jedi Language Server: v{jedi_language_server.__version__}
| Endpoint: {'ws://0.0.0.0:54332'} 
""", color="blue"))

def start_lsp():
    _print_lsp_details() 
    import subprocess
    FNULL = open(devnull, 'w')
    jedi_language_server = subprocess.Popen(
        ["ps", "aux", "|", "pkill", "jedi-language-", "&&","jedi-language-server", "--ws", "--host", "0.0.0.0", "--port", "54332"],
        stdout=FNULL,
        stderr=subprocess.STDOUT
    )
    return jedi_language_server


def start():
    # jedi_language_server = start_lsp()
    _print_server_details()
    # import signal
    import uvicorn
    uvicorn.run(
        "osintbuddy.server:app",
        host="127.0.0.1",
        port=42562,
        loop='asyncio',
        reload=True,
        workers=4,
        headers=[('server', f"OSINTBuddy")],
        log_level='info'
    )

    # def signal_handler(sig, frame):
    #     jedi_language_server.wait(timeout=1)

    # signal.signal(signal.SIGINT, signal_handler)
    # signal.pause()


def create_plugin_wizard():
    # TODO: setup prompt process for initializing an osintbuddy plugin(s) project
    pass


def main():
    commands = {
        "lsp": start_lsp,
        "start": start,
        "plugin create": create_plugin_wizard,
    }
    parser = ArgumentParser()
    parser.add_argument('command', type=str, nargs="*", help="[CATEGORY (Optional)] [ACTION]")

    args = parser.parse_args()
    command = commands.get(' '.join(args.command))

    if command:
        command()
    else:
        parser.error("Command not recognized")


if __name__ == '__main__':
    main()
