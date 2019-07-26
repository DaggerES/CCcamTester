#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#Created by Dagger -- https://github.com/gavazquez

if __name__ == "__main__":
    import CCcamTester
    import sys

    if len(sys.argv) == 5:
        CCcamTester.TestCline("C: "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4])
    else:
    	print "Wrong format. Try '"+sys.argv[0]+" SERVER PORT USER PASSWORD'"
