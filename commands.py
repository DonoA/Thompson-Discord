class Commands:
    def __init__(connection, client):
        self.connection = connection
        self.discord = client
        self.commands = {
            "stats": {
                executor: self.stats
            },
            "promote": {
                executor: self.promote,
                rank: 1
            },
            "demote": {
                executor: self.demote,
                rank: 1
            },
            "update": {
                executor: self.update,
                rank: 1
            },
            "man": {
                executor: self.manual
            }
        }

    def handle(self, executor, command, tagged):
        args = " ".split(command.content)
        if args[0][0] == "$" || tagged:
            cmd = self.commands[args[0][1:]]
            if ('rank' in cmd and cmd['rank'] == executor.rank) or 'rank' not in cmd:
                if cmd['args'] and cmd['args'] <= len(args)-1:
                    cmd['executor'](args[1:])
                else:
                    self.man([args[0]])
            else:
                await self.discord.send_message(message.channel, "You have insufficient permissions to preform this action")



    def stats(args):
        # print the stats of the current user

    def promote(args):
        # promote the user

    def demote(args):
        # demote the user

    def man(args):
        # print man data

    def update(args):
        # try to self update
