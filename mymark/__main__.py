import wx
import wx.html2
import urllib.parse
from .markup import BasicTextParser


class MyFrame(wx.Frame):
    def __init__(self, *args1, **args2):
        super().__init__(*args1, **args2)
        panel = wx.Panel(self)
        self.openbtn = wx.Button(panel, label="open")
        self.savebtn = wx.Button(panel, label="Save")
        self.renderbtn = wx.Button(panel, label="render")
        self.filename = wx.TextCtrl(panel)
        self.contents = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL)
        hbox = wx.BoxSizer()
        hbox.Add(self.filename, proportion=1, flag=wx.EXPAND)
        hbox.Add(self.openbtn, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.renderbtn, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.savebtn, proportion=0, flag=wx.LEFT, border=5)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(self.contents, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        panel.SetSizer(vbox)

        self.openbtn.Bind(wx.EVT_BUTTON, self.load)
        self.renderbtn.Bind(wx.EVT_BUTTON, self.render)
        self.savebtn.Bind(wx.EVT_BUTTON, self.save)

    def load(self, event):
        file_name = wx.FileSelector("Choose a file to open")
        if file_name:
            self.filename.SetValue(file_name)
            files = open(file_name)
            self.contents.SetValue(files.read())
            files.close()

    def render(self, event):
        if self.filename.GetValue():
            frame2 = wx.Frame(None, title="My Broswer", size=(900, 700), pos=(200, 100))
            webbox = wx.html2.WebView.New(frame2)

            name = self.filename.GetValue()
            names = name.split('.')
            names[1] = 'html'
            htmlname = '.'.join(names)

            htmlfile = open(htmlname, 'w')
            ftxt = open(name)
            parser = BasicTextParser(htmlfile)
            parser.parse(ftxt)
            ftxt.close()
            htmlfile.close()
            # 可能有中文名，需要处理一下
            htmlurl = urllib.parse.quote(htmlname, encoding='utf-8')
            webbox.LoadURL(htmlurl)
            frame2.Show()
        else:
            wx.MessageBox('请先打开一个文件或保存一个文件', caption='Tip')

    def save(self, event):
        if not self.contents.GetValue():
            wx.MessageBox('文件是空的', caption='Tip')
            return
        if not self.filename.GetValue():
            self.filename.SetValue(wx.SaveFileSelector('', 'txt'))
        if self.filename.GetValue():
            files = open(self.filename.GetValue(), 'w')
            files.write(self.contents.GetValue())
            files.close()


app = wx.App()
win = MyFrame(None, title="Simple Markdown", size=(800, 700), pos=(200, 100))
win.Show()
app.MainLoop()
