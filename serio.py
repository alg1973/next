import termios

class Serial:
    tty_name=''
    def __init__(self,t):
        self.tty_name=t
        # While PySerial would be preferable and more machine-independant,
        # it does not support echo suppression
        self.tser= open(self.tty_name, 'r+')
        # Config the debug serial port
        self.oldattrs = termios.tcgetattr(self.tser)
        newattrs = termios.tcgetattr(self.tser)
        newattrs[4] = termios.B9600  # ispeed
        newattrs[5] = termios.B9600  # ospeed
        newattrs[3] = newattrs[3] & ~termios.ICANON & ~termios.ECHO
        newattrs[6][termios.VMIN] = 1
        newattrs[6][termios.VTIME] = 0
        termios.tcsetattr(self.tser, termios.TCSANOW, newattrs)
        return

    def sread(self):
        result=""
        while True:
            ch=self.tser.read(1)
            if ch and ch!="\n":
                if ch != "\r":
                    result +=ch
            else:
                break
        return result

    def sclose(self):
        # Restore previous state
        termios.tcsetattr(self.tser, termios.TCSAFLUSH, self.oldattrs)
        self.tser.close()
        # Flush any partial buffer

print "Start\n"
f=Serial("/dev/tty")
ch=f.sread()
print " Yes: "+ch
f.sclose()
