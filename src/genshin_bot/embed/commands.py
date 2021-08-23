from discord import Embed

from .base import EmbedService
from ..models.commands import CommandArgument, Command
from ..services.commands import commands


class CommandsInfoEmbedService(EmbedService):

    def __init__(self):
        self.embed = Embed()
        self.commands = commands
        self.add_commands_info()

    def add_commands_info(self):
        self.embed.title = "Информация о боте"
        self.embed.description = "Бот-гача с аниме девочками. Список команд ниже"
        for command in self.commands:
            self.embed.add_field(name=command.name, value=self.get_command_description_template(command), inline=False)

    def get_argument_template(self, argument: CommandArgument) -> str:
        return f"{argument.name} - {argument.description}"

    def get_command_description_template(self, command: Command) -> str:
        msg = f"{command.description}."
        if command.arguments is not None:
            msg += " Аргументы: \n"
            args_info = [self.get_argument_template(argument) for argument in command.arguments]
            msg += '\n'.join(args_info)
        return msg

    def get_embed(self) -> Embed:
        return self.embed
