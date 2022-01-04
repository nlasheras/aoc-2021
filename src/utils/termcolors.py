class TermColors:
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def __color__(i:int):
        return f'\033[{90+i}m'

    BLACK = __color__(0)
    RED = __color__(1)
    GREEN = __color__(2)
    YELLOW = __color__(3)
    BLUE = __color__(4)
    MAGENTA = __color__(5)
    CYAN = __color__(6)
    WHITE = __color__(7)
