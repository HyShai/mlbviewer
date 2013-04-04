#!/usr/bin/env python

import curses
import curses.textpad
import time
from mlbListWin import MLBListWin
from mlbConstants import *

class MLBHelpWin(MLBListWin):

    def __init__(self,myscr,mycfg):
        self.mycfg = mycfg
        self.data = []
        for heading in HELPFILE:
            self.data.append((heading[0],curses.A_UNDERLINE))
            for helpkeys in heading[1:]:
                for k in helpkeys:
                    helpstr="%-20s: %s" % (k, KEYBINDINGS[k])
                    self.data.append((helpstr, 0))
        # data is everything, records is only what's visible
        self.records = self.data[0:curses.LINES-4]
        self.myscr = myscr
        self.current_cursor = 0
        self.record_cursor = 0
        self.statuswin = curses.newwin(1,curses.COLS-1,curses.LINES-1,0)
        self.titlewin = curses.newwin(2,curses.COLS-1,0,0)

    def Refresh(self):
        if len(self.data) == 0:
            #status_str = "There was a parser problem with the listings page"
            #self.statuswin.addstr(0,0,status_str)
            self.titlewin.refresh()
            self.myscr.refresh()
            self.statuswin.refresh()
            #time.sleep(2)
            return

        self.myscr.clear()
        for n in range(curses.LINES-4):
            if n < len(self.records):
                #s = "%s = %s" % (self.records[n][0], self.records[n][1])
                ( s, cflags ) = self.records[n]

                padding = curses.COLS - (len(s) + 1)
                if n == self.current_cursor:
                    s += ' '*padding
            else:
                s = ' '*(curses.COLS-1)

            if n == self.current_cursor:
                cursesflags = curses.A_REVERSE|curses.A_BOLD|cflags
            else:
                if n < len(self.records):
                    cursesflags = 0|cflags
            if n < len(self.records):
                self.myscr.addstr(n+2, 0, s[:curses.COLS-1], cursesflags)
            else:
                self.myscr.addstr(n+2, 0, s)

        self.myscr.refresh()

    def titleRefresh(self,mysched):
        titlestr = "%-20s%s" % ( VERSION, URL )

        padding = curses.COLS - len(titlestr) 
        titlestr += ' '*padding
        self.titlewin.addstr(0,0,titlestr)
        self.titlewin.hline(1, 0, curses.ACS_HLINE, curses.COLS-1)
        self.titlewin.refresh()

    def statusRefresh(self):
        n = self.current_cursor

        status_str = 'Press L to return to listings...'
        debug_str = "nlines=%s, dlen=%s, rlen=%s, cc=%s, rc=%s" % \
                     ( ( curses.LINES-4), len(self.data), len(self.records),
                       self.current_cursor, self.record_cursor )

        # And write the status
        try:
            self.statuswin.addstr(0,0,status_str,curses.A_BOLD)
        except:
            raise Exception, debug_str
        self.statuswin.refresh()