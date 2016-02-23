import sys
from .util import *
from .rules import *
from .filters import *


class Parser:
    def __init__(self, htmlfile):
        self.rules = []
        self.filters = []
        sys.stdout = htmlfile

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, myfilter):
        self.filters.append(myfilter)

    def parse(self, perfile):
        Rule.start(self)
        for block in blocks(perfile):
            for myfilter in self.filters:
                block = myfilter.filter(block)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block)
                    if last:
                        break
        Rule.end(self)


class BasicTextParser(Parser):
    def __init__(self, htmlfile):
        super().__init__(htmlfile)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(QuoteRule())
        self.addRule(CodeBlockRule())
        self.addRule(HorizontalRule())
        self.addRule(ParagraphRule())

        self.addFilter(StrongFilter())
        self.addFilter(EmFilter())
        self.addFilter(PictureFilter())
        self.addFilter(ComplicateLinkFilter())
        self.addFilter(SimpleLinkFilter())
        self.addFilter(EmailFilter())
        self.addFilter(InlineCodeFilter())
