import re

from mcdreforged.handler.impl import *
from mcdreforged.api.types import ServerInterface

def get_handler():

    server = ServerInterface.get_instance()
    handler = server.get_mcdr_config().get('handler', '')

    if handler == 'vanilla_handler':
        return VanillaHandler
    elif handler == 'forge_handler':
        return ForgeHandler
    elif handler == 'bukkit_handler':
        return BukkitHandler
    elif handler == 'bukkit14_handler':
        return Bukkit14Handler
    elif handler == 'cat_server_handler':
        return CatServerHandler
    elif handler == 'arclight_handler':
        return ArclightHandler
    
class CommandblockHandler(get_handler()):

    def get_name(self) -> str:
        return 'commandblock_handler'

    def parse_server_stdout(self, text: str):

        info = super().parse_server_stdout(text)
        if not info.player:
            m = re.fullmatch(r'(?:\[Not Secure\] )?\[(?P<name>[^\]]+)\] (?P<message>.*)', info.content)
            if m and m['name'] == 'Server':
                info.player, info.content = 'function', m['message']
            elif m and m['name'] == '@':
                info.player, info.content = 'commandblock', m['message']
        return info

def on_load(server, prev_module):

    server.register_server_handler(CommandblockHandler())