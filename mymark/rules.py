class Rule:
    '''
    super class of rules, rules are used to mark a whole paragraph
    '''

    def action(self, block):
        self.start()
        self.feed(block)
        self.end()
        return True

    def start(self):
        print('''<html><head>
            <title></title>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <link rel="stylesheet" type="text/css" href=''' + '"' + __file__ + '''/../css/GitHub2.css"/>
            <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.0.0/styles/railscasts.min.css">
            <script src="http://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.0.0/highlight.min.js"></script>
            <script>hljs.initHighlightingOnLoad();</script>
            </head>
            <body>''')

    def end(self):
        print('''</body>
            </html>''')

    def feed(self, block):
        print(block)


class HeadingRule(Rule):
    '''
    headings begin with #, numbers of # means the level of heading
    '''
    def condition(self, block):
        return block[0] == '#'

    def action(self, block):
        n = 0
        while block[n] == '#':
            n += 1
        self.start(n)
        self.feed(block[n:])
        self.end(n)
        return True

    def start(self, n):
        print('<h' + str(n) + '>')

    def end(self, n):
        print('</h' + str(n) + '>')


class TitleRule(HeadingRule):
    '''
    the first heading is the title, to be different, appended with a <hr>
    '''
    def __init__(self):
        self.first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condition(self, block)

    def end(self, n):
        print('</h' + str(n) + '><hr/>')


class QuoteRule(Rule):
    '''
    blockquotes begin with >
    '''

    def condition(self, block):
        return block[0] == '>'

    def action(self, block):
        self.start()
        self.feed(block[1:].strip())
        self.end()
        return True

    def start(self):
        print('<blockquote>')

    def end(self):
        print('</blockquote>')


class ListItemRule(Rule):
    '''
    lists begin with - or +
    '''

    def condition(self, block):
        if block[0] == '-' or block[0] == '+':
            return block[0]
        else:
            return ''

    def action(self, block):
        self.start()
        self.feed(block[1:].strip())
        self.end()
        return True

    def start(self):
        print('<li>')

    def end(self):
        print('</li>')


class ListRule(ListItemRule):
    '''
    lists begin with - mean unordered, with + mean ordered
    '''

    def __init__(self):
        self.inside = False
        self.ordered = False

    def condition(self, block):
        return True

    def action(self, block):
        list_or_not = super().condition(block)
        if not self.inside and list_or_not:
            if list_or_not == '+':
                self.ordered = True
            self.start()
            self.inside = True
        elif self.inside and not list_or_not:
            self.end()
            self.inside = False
            self.ordered = False
        return False  # 这里返回false因为这部分还需要用其他Rule覆盖

    def start(self):
        if self.ordered:
            print('<ol>')
        else:
            print('<ul>')

    def end(self):
        if self.ordered:
            print('</ol>')
        else:
            print('</ul>')


class HorizontalRule(Rule):
    '''
    *** mean a <hr>
    '''

    def condition(self, block):
        return block == '***'

    def action(self, block):
        print('<hr>')
        return True


class CodeBlockRule(Rule):
    '''
    blockcode put between ``` and ```
    '''

    def condition(self, block):
        if block[0:3] == '```' and block[-3:] == '```':
            return True

    def action(self, block):
        header, noheader = block.split('\n', 1)
        codetype = header[3:].strip()
        self.start(codetype)
        self.feed(noheader[:-3])
        self.end()
        return True

    def start(self, codetype):
        print('<pre><code class="' + codetype + '">')

    def end(self):
        print('</code></pre>')


class ParagraphRule(Rule):
    '''
    ordinary paragraph
    '''

    def condition(self, block):
        return True

    def start(self):
        print('<p>')

    def end(self):
        print('</p>')
