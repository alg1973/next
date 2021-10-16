#!/usr/bin/python2.7
#coding=utf-8


import matplotlib.pyplot as plt
from matplotlib.dates import  DateFormatter

import datetime
import th_data
import sys



def create_img(ts, values, save_file=None):
        dates = map(datetime.datetime.fromtimestamp, ts)
        #c = '\xe2\x84\x83' #.encode(encoding='UTF-8')
        c="(c) "
        last_time = ("Temperature [Last: "+str(values[-1])+c+dates[-1].strftime("%a %d-%m-%Y %H:%M:%S")+"]")

        fig, ax = plt.subplots()
        ax.plot_date(dates, values, linestyle='dashed', linewidth = 1)
        ax.xaxis.set_major_formatter( DateFormatter('%d %H:%M') )
        # setting x and y axis range
        ax.set_xlim(dates[0], dates[-1])
        ax.set_ylim(5, 24)

        # The hour locator takes the hour or sequence of hours you want to
        # tick, not the base multiple

        #ax.xaxis.set_major_locator(DayLocator())
        #ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
        #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()

        # naming the x axis
        plt.xlabel('date')
        # naming the y axis
        plt.ylabel('T(C)')

        # giving a title to my graph
        plt.title(last_time)

        # function to show the plot

        if save_file is None:
                plt.show()
        else:
                plt.savefig(save_file)
                plt.close(fig)

def do_graph(period, save_file=None):
        term_data = th_data.th_data()
        (ts, values) = term_data.get_data(period)
        create_img(ts, values, save_file)
        
if __name__ == "__main__":
        p = 60
        save_file = None
        if len(sys.argv) == 2:
                p = int(sys.argv[1])
        elif len(sys.argv) == 3:
                save_file = sys.argv[2]
                
        do_graph(p, save_file)


