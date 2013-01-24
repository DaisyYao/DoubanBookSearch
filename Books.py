# -*- coding: utf-8 -*-
'''
Created on 2013-1-20

@author: Yaojie
'''
import wx
import urllib
import os
import shutil

save_path = "image"
class Books(object):
    '''
    书籍信息对象
    '''
    def __init__(self,book = []):
        '''
        Constructor
        '''
        self.id = book["id"]
        self.title = book["title"]
        self.subtitle = book["subtitle"]
        self.origin_title = book["origin_title"]
        self.author = book["author"][0]
        self.publisher = book["publisher"]
        self.isbn = book["isbn13"]
        self.pubdate = book["pubdate"]
        self.price = book["price"]
        self.author_intro = book["author_intro"]
        self.summary = book["summary"]
        self.imageUrl = book["images"]["medium"]
        
    #书籍简单信息    
    def simpleInfo(self):
        info = ''
        if(self.subtitle) != '':
            info += u"\n别名：" + self.subtitle
        if(self.origin_title) != '':
            info += u"\n原作名：" + self.origin_title
        bookInfo = (u"标题： " + self.title + info +
                    u"\n作者： " + self.author +
                    u"\n出版社：" + self.publisher +
                    u"\nISBN：" + self.isbn +
                    u"\n出版社：" + self.publisher +
                    u"\n出版时间：" + self.pubdate +
                    u"\n定价：" + self.price)
        return bookInfo
                
    #书籍详细简介信息
    def longInfo(self):
        bookInfo = (u"\n作者简介： "+ self.author_intro +
                    u"\n内容简介： " + self.summary)
        return bookInfo
    
    #获取书籍封面
    def getImage(self):
        bImage = self.get_image(self.imageUrl,self.id)
        
        return bImage
    def get_image(self,file_url, file_name):
        #获取书籍封面，非常囧的是不知道怎么之间从接口获取信息展示，所以先下下来，再删除
        if not os.path.isdir("image"): 
            os.mkdir("image")
        filename = "image\\" + file_name +".jpg"
        urllib.urlretrieve(file_url,filename)     
        imgdata = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        bImage = wx.BitmapFromImage(imgdata)
        shutil.rmtree("image")
        return bImage
    
