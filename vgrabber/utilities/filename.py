import re

from vgrabber.utilities.accents import strip_accents

__re_invalid_chars = re.compile(r'[^a-zA-Z0-9\-_.()\\[\]]]')

__windows_reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                      'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
                      'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}


def correct_file_name(file_name):
    file_name = strip_accents(file_name)
    file_name = __re_invalid_chars.sub('-', file_name)
    if file_name in __windows_reserved:
        file_name = '-{0}-'.format(file_name)
    return file_name
