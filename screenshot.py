#-*-coding:utf-8-*-
import win32gui
import win32ui
import win32con
import win32api

#GetDesktopWindow函数获取桌面窗口句柄
hdesktop=win32gui.GetDesktopWindow()

#分辨率适应,GetSystemMetrics函数返回以像素值为单位的WINDOWS边框的宽度和高度
#因为屏幕可以调节分辨率，物理的像素点和屏幕显示的像素点并不一定一致得到的这些数值是和分辨率相关的，不是屏幕的物理参数，故称其为虚拟的，有别于真实的硬件像素坐标

width=win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)#屏幕的长度 
height=win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)#屏幕的宽度
left=win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)#屏幕左上角X座标
top=win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)#屏幕左上角Y座标

#创建设备描述表Device Context
#设备描述表是一个定义一组图形对象及其属性、影响输出的图形方式(数据)结构。
#windows提供设备描述表，用于应用程序和物理设备之间进行交互，从而提供了应用程序设计的平台无关性.
#设备描述表又称为设备上下文，或者设备环境。
desktop_dc=win32gui.GetWindowDC(hdesktop)#得到句柄
img_dc=win32gui.CreateDCFromHandle(desktop_dc)#给当前窗口创建上下文空间 一个内存缓冲区


#创建一个内存设备描述表/创建一个与img_dc格式一样的一个内存缓冲区
mem_dc=img_dc.CreateCompatibleDC()

#创建位图对象
screenshot=win32ui.CreateBitmap()
screenshot=CreateCompatibleBitmap(img_dc,width,height)#创建与img_dc兼容 的位图
mem_dc.SelectObject(screenshot)

#截图至内存设备描述表
mem_dc.BitBlt((0,0),(width,height),img_dc,(left,top),win32con.SRCCOPY)

#将截图保存到文件中
screenshot.SaveBitmapFile(mem_dc,'c:\\users\\lenovo\\desktop\\screenshot.bmp')

#内存释放
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
