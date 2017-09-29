# CLine tester scripts
*Also called Cline, CCcline, CCcam and Camd*

Scripts for testing that a Cline works or not. This is the python part altered to my needs from 
**https://github.com/DaggerES/CLineTester**.

## Usage

Usage has changed from forked project, 
see Main.py

## Changes

* __init__.py in the folder, as I use it as a package
* Let Exceptions propagate
* Encapsulate all in a class, use Properties for result
* Get IP before connecting to CLine, testing is done when calling Test()
* Timeout is configurable by setting Timeout property (default 30s)
* Measure Ping time
* Some quick cleanups

## Thanks

Thanks go to DaggerES, which released the original version. 
