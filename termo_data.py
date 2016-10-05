
if len(sys.argv)==2:
        tty_name=sys.argv[1]
else:
        tty_name="/dev/cu.wchusbserial1410"
f=Serial(tty_name)
time.sleep(3)
while 1:
        f.swrite("\n")
        time.sleep(0.5)
        ch=f.sread()
        print ch
        time.sleep(5)
f.sclose()


