#!/usr/bin/python
import sys
import termios
import time

class Serial:
    tty_name=''
    def __init__(self,t):
        self.tty_name=t
        # While PySerial would be preferable and more machine-independant,
        # it does not support echo suppression
        self.tser= open(self.tty_name, 'r+',buffering=0)
        # Config the debug serial port
        self.oldattrs = termios.tcgetattr(self.tser)
        newattrs = termios.tcgetattr(self.tser)
	newattrs[2] = newattrs[2] & ~termios.HUPCL
        newattrs[4] = termios.B9600  # ispeed
        newattrs[5] = termios.B9600  # ospeed
        newattrs[3] = newattrs[3] & ~termios.ICANON & ~termios.ECHO
        newattrs[6][termios.VMIN] = 1
        newattrs[6][termios.VTIME] = 0
        termios.tcsetattr(self.tser, termios.TCSANOW, newattrs)
        return

    def sread(self):
        result=""
        while 1:
            ch=self.tser.read(1)
            if ch and ch!="\n" and ch!="\r":
                    result +=ch
            else:
                break
        return result

    def swrite(self,str):
	self.tser.write(str)

    def sclose(self):
        # Restore previous state
        #termios.tcsetattr(self.tser, termios.TCSAFLUSH, self.oldattrs)
        self.tser.close()
        # Flush any partial buffer

#if len(sys.argv)==2:
#	tty_name=sys.argv[1] 
#else:
#	tty_name="/dev/cu.wchusbserial1410"
#f=Serial(tty_name)
#time.sleep(3)
#while 1:
#	f.swrite("\n")
#	time.sleep(0.5)
#	ch=f.sread()
#	print ch
#	time.sleep(5)
#f.sclose()
