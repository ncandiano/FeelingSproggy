# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 00:34:27 2014

@author: nathan
"""
import praw
import wx
import random

user_agent = ('Just Gathering Sprogs Awesome Verses, Sirs and Madams 1.0 by u/Candiana')
r = praw.Reddit(user_agent=user_agent)
thing_limit = None
user_name = 'Poem_for_your_sprog'
user = r.get_redditor(user_name)
gen = user.get_comments(limit=thing_limit)
def fetchSprog():
    sprogstuff = {}
    with open ('sprogtext.txt', 'w') as sprogtext:
        for comment in gen:
            text = comment.body
            cLink = comment.id
            sLink = comment.link_id[3:]
            commentLink = 'http://www.reddit.com/comments/' + sLink + '/_/' + cLink
            sprogstuff.update({text: commentLink})
            sprogtext.write(str(sprogstuff))
        sprogtext.close()
    return sprogstuff

def getSomeSprog():
    randompoem = random.choice(sprogstuff.keys())
    select_poem = str(randompoem)
    select_link = str(sprogstuff[randompoem])
    return select_poem, select_link

class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(400,600))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        select_poem, select_link = getSomeSprog()

        menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        helpm = wx.Menu()

        menubar.Append(filem, '&File')
        menubar.Append(editm, '&Edit')
        menubar.Append(helpm, '&Help')
        fitem = filem.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        ppanel = wx.TextCtrl(panel, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CENTRE)
        ppanel.AppendText(select_poem)
        hbox1.Add(ppanel, proportion=1, flag = wx.EXPAND)
        vbox.Add(hbox1, proportion=1, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 25))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        lpanel = wx.HyperlinkCtrl(panel, wx.ID_ANY, 'Link to Sprog', url=select_link)
        hbox2.Add(lpanel)
        vbox.Add(hbox2, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 25))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        cbtn = wx.Button(panel, label='Close', size =(70,30))
        cbtn.Bind(wx.EVT_BUTTON, self.On_Quit)
        hbox3.Add(cbtn)
        rbtn = wx.Button(panel, label='Refresh', size=(70,30))
        rbtn.Bind(wx.EVT_BUTTON, self.On_Refresh)
        hbox3.Add(rbtn, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_MENU, self.On_Quit, fitem)
        self.ppanel = ppanel
        self.ppanel.ShowPosition(0)
        self.lpanel = lpanel

        self.SetMenuBar(menubar)

    def On_Quit(self, e):
        self.Close()

    def On_Refresh(self, e):
        newselect_poem, newselect_link = getSomeSprog()
        self.ppanel.ChangeValue(newselect_poem)
        self.lpanel.SetURL(newselect_link)
        self.Refresh()

if __name__ == '__main__':

    sprogstuff = fetchSprog()
    app = wx.App()
    MainFrame(None, title='Feeling Sproggy?')
    app.MainLoop()
