#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#Created by Dagger -- https://github.com/DaggerES

from CLineTester import CLineTester

if __name__ == "__main__":
    cline = "C: jjjjj.jjjj.com 22000 uuuu pppp"
    try:
        cl = CLineTester(cline)
        cl.Timeout = 10 # wait 10 seconds only for the request to return (default: 30)
        print "IP of CLine is '%s'." % (cl.Ip,)
        if cl.Test():
            # show cline with IP on success
            print "CLine '%s' is OK. Ping is %ss" % (cl.CLineIP, cl.Ping,)
    except Exception as e:
        print "CLine '%s' failed: %s" % (cline, e,)
