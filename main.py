# -*- coding: utf-8 -*-
'''
Created on 2013-1-20

@author: Yaojie
'''

import Books
import wx
import httplib2
import json

class DoubanReader(wx.App):
    def OnInit(self):
        self.Start = 0          #请求书籍的起始页
        self.Count = 2          #一次请求的数量
        self.Total = 0          #请求结果的总数量

        self.frame = wx.Frame(parent = None, title = u'书目查询', size=(600,600))
        
        self.panel = wx.Panel(self.frame, -1)
        #标题
        title = wx.StaticText(self.panel, -1, u'书   目   查   询',
                              style = wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL,
                              size = (480,50))
        title.SetFont(wx.Font(20,wx.SWISS,wx.NORMAL,wx.BOLD))
        title.SetForegroundColour('white')
        title.SetBackgroundColour('grey')
        #输入框,搜索按钮
        self.bookName = wx.TextCtrl(self.panel, -1,u"请输入需要查询的书名、作者、ISBN", pos = (10,60), size = (350,20))
        self.buttonOk = wx.Button(self.panel, -1, 'search', pos = (370,60))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOk)

        #布局
        #垂直的sizer========
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(title,0,wx.EXPAND)
        
        #搜索sizer
        searchSizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=5)
        searchSizer.AddGrowableCol(0)
        searchSizer.AddGrowableCol(1)
        searchSizer.Add(self.bookName,1,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        searchSizer.Add(self.buttonOk,1,wx.EXPAND)
        self.mainSizer.Add(searchSizer,0,wx.EXPAND|wx.ALL,10)
        #分割线
        self.mainSizer.Add(wx.StaticLine(self.panel),0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)

        #翻页显示
        self.footSizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=5)
        self.footSizer.AddGrowableCol(0)
        self.footSizer.AddGrowableCol(1)
        self.mainSizer.Add(self.footSizer,0,wx.EXPAND)
        
        #书籍信息显示
        self.bookInfoSizer = wx.GridBagSizer(hgap=5,vgap=5) 
        self.mainSizer.Add(self.bookInfoSizer)
        
        self.panel.SetSizer(self.mainSizer)
        self.panel.Refresh()

        self.frame.Show()

        return True
    #查询图书，返回书籍列表
    def search_book(self,book,start,count):
        h = httplib2.Http()
        url_search = "https://api.douban.com/v2/book/search"+"?q="+book+"&start="+str(start)+"&count="+str(count)
        try:
            resp, content = h.request(url_search,"GET")
        except:
            #对网络异常进行处理
            return None
        #解析json数据
        s = json.loads(content,encoding="utf-8")
        self.Total = s["total"]
        #返回书籍信息
        return s['books']
    
    #查询按钮
    def OnButtonOK(self,event):
        #查询书籍信息
        self.Start = 0
        books = self.search_book(self.bookName.GetValue(),self.Start,self.Count)
        #返回并展示书籍信息
        self.BookInfo(books)

    
    #书籍展示信息返回
    def BookInfo(self,books):
        #清空原始数据
        self.bookInfoSizer.DeleteWindows()
        self.bookInfoSizer.Clear()
        
        if books == None:
            bookInfo = u"\n网络异常╮(╯▽╰)╭"
            info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP|wx.ALIGN_CENTRE_VERTICAL,
                                     size = (400,0),
                                     pos = (5,100))
            self.bookInfoSizer.Add(info,pos=(0,0))
            info.SetForegroundColour('grey')
            font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
            info.SetFont(font)
        elif len(books) == 0:
            bookInfo = u"\n暂无结果╮(╯▽╰)╭"
            info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP|wx.ALIGN_CENTRE_VERTICAL,
                                     size = (400,50),
                                     pos = (5,100))
            self.bookInfoSizer.Add(info,pos=(0,0))
            info.SetForegroundColour('grey')
            font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
            info.SetFont(font)
        else:
            for i in range(len(books)):                
                book = Books.Books(books[i])
                bookSimple = book.simpleInfo()
                bookLong = book.longInfo()
                sb = wx.StaticBitmap(self.panel, -1, book.getImage(), pos = (50,5))
                info = wx.StaticText(self.panel, -1, bookSimple,
                                     style = wx.TE_WORDWRAP,
                                     pos = (5,100),
                                     size = (500,150))
                font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
                info.SetFont(font)
                info_long = wx.StaticText(self.panel, -1, bookLong,
                                     style = wx.TE_WORDWRAP,
                                     pos = (5,100),
                                     size = (580,200))
                font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
                info_long.SetFont(font)
                
                self.bookInfoSizer.Add(sb,pos=(2*i,0))
                self.bookInfoSizer.Add(info,pos=(2*i,1))
                self.bookInfoSizer.Add(info_long,pos=(2*i+1,0),span=(2*i+1,2))
                self.panel.Refresh()
        self.IfPage()        
        self.frame.Refresh()
        self.mainSizer.Fit(self.frame)
    
    #下一页
    def OnButtonNext(self,event):
        #查询书籍信息
        books = self.search_book(self.bookName.GetValue(),self.Start,self.Count)
        self.Start += self.Count
        #返回并展示书籍信息
        self.BookInfo(books)
    
    #上一页
    def OnButtonForward(self,event):
        #查询书籍信息
        books = self.search_book(self.bookName.GetValue(),self.Start,self.Count)
        self.Start -= self.Count      
        #返回并展示书籍信息
        self.BookInfo(books)
    
    #页码判断
    def IfPage(self):
        self.frame.Refresh()
        self.footSizer.DeleteWindows()
        self.footSizer.Clear()
        #总数为0，没有数据不展示翻页按钮
        if self.Total != 0:
            #还有后文，显示下一页按钮
            if (self.Total - self.Start)> self.Count:
                self.btnNext = wx.Button(self.panel,-1,u"下一页",pos = (200,100))
                self.Bind(wx.EVT_BUTTON, self.OnButtonNext, self.btnNext)                
                #起始不为0，显示两个按钮
                if self.Start != 0 :
                    self.btnForward = wx.Button(self.panel,-1,u"上一页",pos = (100,100))
                    self.Bind(wx.EVT_BUTTON, self.OnButtonForward, self.btnForward)
                    self.footSizer.Add(self.btnForward,0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
                #起始为0，只有下一页按钮        
                self.footSizer.Add(self.btnNext,0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
            elif self.Total > self.Count:
                self.btnForward = wx.Button(self.panel,-1,u"上一页",pos = (100,100))
                self.Bind(wx.EVT_BUTTON, self.OnButtonForward, self.btnForward)
                self.footSizer.Add(self.btnForward,0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
app = DoubanReader()
app.MainLoop()
