

class Commands:
    def __init__(connection):
        self.connection = connection
        self.commands = {
            "stats": self.stats
            "promote": self.promote,

        }

    def handle(self, executor, command, tagged):
        args = " ".split(command)
        
        self.commands[args[0]](args[1:], tagged)

    def promote(args, tagged):
