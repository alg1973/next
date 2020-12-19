#!/usr/bin/python

import time

class fterm:
    def __init__(self):
        self.term_file = './term.last'


    def get(self):
        with open(self.term_file, "r") as tf:
            (tnow, temp) = tf.readline().split()
            if int(tnow)>int(time.time()) or (int(time.time()-int(tnow))>60*10):
                return -127
            return float(temp)
        return -127.0

                
    
