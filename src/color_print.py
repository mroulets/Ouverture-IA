# print red if fail, green if pass, yellow if warn, blue if info, white if bold
class ColorPrint:
    # color red
    @staticmethod
    def print_fail(message, end = '\n'):
        print(f'\x1b[1;31m{message.strip()}\x1b[0m', end=end)
    # color green
    @staticmethod
    def print_pass(message, end = '\n'):
        print(f'\x1b[1;32m{message.strip()}\x1b[0m', end=end)
    # color yellow
    @staticmethod
    def print_warn(message, end = '\n'):
        print(f'\x1b[1;33m{message.strip()}\x1b[0m', end=end)
    # color blue
    @staticmethod
    def print_info(message, end = '\n'):
        print(f'\x1b[1;34m{message.strip()}\x1b[0m', end=end)
    # color white
    @staticmethod
    def print_bold(message, end = '\n'):
        print(f'\x1b[1;37m{message.strip()}\x1b[0m', end=end)
