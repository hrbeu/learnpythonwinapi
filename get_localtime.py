#-*-coding:utf-8-*-
from ctypes import Structure,windll,POINTER,pointer
from ctypes.wintypes import WORD

class SYSTEMTIME(Structure):
	_fields_=[("wYear",WORD),
	("wMonth",WORD),
	("wDayofWeek",WORD),
	("wDay",WORD),
	("wHour",WORD),
	("wMinute",WORD),
	("wSecond",WORD),
	("wMilliseconds",WORD),
	]

GetLocalTime=windll.kernel32.GetLocalTime
GetLocalTime.argtypes=[POINTER(SYSTEMTIME),]
t=SYSTEMTIME()
GetLocalTime(pointer(t))
print '%04d-%02d-%02d %02d:%02d:%02d' %  (t.wYear, t.wMonth, t.wDay, 
t.wHour, t.wMinute, t.wSecond)
