from colorama import Fore, init                                                     # the 'chat effects' are from the colorama module
init(convert=True)                                                                  # set convert to True, avoiding, character display bugs

default_color = 0x4A86E8                                                            # embed 'default' color
error_color = 0xFF4040                                                              # embed 'error' color
warning_color = 0xEED202                                                            # embed 'warning' color
admin_color = 0x00B054                                                              # embed 'admin' color


def red(text: str):                                                                 # func. that gen. a 'red' color
    colored_text = Fore.LIGHTRED_EX + str(text) + Fore.RESET
    return colored_text


def blue(text: str):                                                                # func. that gen. a 'blue' color
    colored_text = Fore.LIGHTBLUE_EX + str(text) + Fore.RESET
    return colored_text


def green(text: str):                                                               # func. that gen. a 'green' color
    colored_text = Fore.LIGHTGREEN_EX + str(text) + Fore.RESET
    return colored_text


def yellow(text: str):                                                              # func. that gen. a 'yellow' color
    colored_text = Fore.LIGHTYELLOW_EX + str(text) + Fore.RESET
    return colored_text


def pink(text: str):                                                                # func. that gen. a 'pink' color
    colored_text = Fore.LIGHTMAGENTA_EX + str(text) + Fore.RESET
    return colored_text


def cyan(text: str):                                                                # func. that gen. a 'cyan' color
    colored_text = Fore.LIGHTCYAN_EX + str(text) + Fore.RESET
    return colored_text