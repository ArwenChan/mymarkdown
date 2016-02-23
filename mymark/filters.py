import re


class Filter:
    '''
    super class of filters, filters are used to replace every mark with html label
    '''
    def __init__(self, pattern, repl):
        self.pattern = pattern
        self.repl = repl

    def filter(self, block):
        return re.sub(self.pattern, self.repl, block)


class EmFilter(Filter):
    '''
    <em> begin and end with *
    '''
    def __init__(self):
        self.pattern = r'\*(.+?)\*'
        self.repl = r'<em>\1</em>'


class StrongFilter(Filter):
    '''
    <strong> begin and end with **
    '''
    def __init__(self):
        self.pattern = r'\*\*(.+?)\*\*'
        self.repl = r'<strong>\1</strong>'


class EmailFilter(Filter):
    '''
    email put in < >
    '''
    def __init__(self):
        self.pattern = r'<([\.\-a-zA-Z_0-9]+@[\.a-zA-Z0-9]+)>'
        self.repl = r'<a href="mailto:\1">\1</a>'


class SimpleLinkFilter(Filter):
    '''
    simple link directly put in < >
    '''
    def __init__(self):
        self.pattern = r'\((http[s]?://.+?)\)'
        self.repl = r'<a href="\1">\1</a>'


class ComplicateLinkFilter(Filter):
    '''
    complicate link like this: [text](link)
    '''
    def __init__(self):
        self.pattern = r'\[(.+?)\]\((http[s]?://.+?)\)'
        self.repl = r'<a href="\2">\1</a>'


class PictureFilter(Filter):
    '''
    picture use link like this: ![picturename](picturelink)
    '''
    def __init__(self):
        self.pattern = r'!\[(.+?)\]\((http[s]?://.+?)\)'
        self.repl = r'<p><center><img src="\2" alt="\1"></center></p>'


class InlineCodeFilter(Filter):
    '''
    inline code put in ``
    '''
    def __init__(self):
        self.pattern = r'[^`]`([^`]+)`[^`]'
        self.repl = r'<code>\1</code>'
