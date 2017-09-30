#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#Created by Dagger -- https://github.com/DaggerES

import CriptoBlock
import socket, re, array, time

regExpr = re.compile('[C]:\s*(\S+)+\s+(\d*)\s+(\S+)\s+([\w.-]+)')

recvblock = CriptoBlock.CryptographicBlock()
sendblock = CriptoBlock.CryptographicBlock()

class CLineTester(object):
    def __init__(self, cline):
        super(self.__class__, self).__init__()
        self._success = False
        self._timeout = 30
        match = regExpr.search(cline)
        if match is None:
            self._success = False
            raise Exception("No valid CLine")
        self._cline = cline
        self._readMatch(*match.groups())
        self._ip = socket.gethostbyname(self._host)
        self._heloBytes = None
        self._ping = None

    def _readMatch(self, host, port, username, password):
        self._host = str(host)
        self._port = int(port)
        self._username = str(username)
        self._password = str(password)

    @property
    def Timeout(self):
        return self._timeout
    @Timeout.setter
    def Timeout(self, value):
        if type(value) is not int:
            raise Exception("Timeout in seconds needs to be an int.")
        self._timeout = value
    @property
    def Success(self):
        return self._success
    @property
    def CLine(self):
        return self._cline
    @property
    def CLineIP(self):
        return "C: %s %s %s %s" % (self.Ip, self.Port, self.Username, self.Password)
    @property
    def Ip(self):
        return self._ip
    @property
    def Host(self):
        return self._host
    @property
    def Port(self):
        return self._port
    @property
    def Username(self):
        return self._username
    @property
    def Password(self):
        return self._password
    @property
    def HeloBytes(self):
        return self._heloBytes
    @property
    def Ping(self):
        return self._ping

    def Test(self):
        self._success = False
        startTime = time.time()
        try:
            testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
            testSocket.settimeout(self._timeout)
            testSocket.connect((self.Ip, self.Port))
            self._doHanshake(testSocket) #Do handshake with the server

            try:
                sendcount = self._sendMessage(self._getPaddedUsername(), len(self._getPaddedUsername()), testSocket) #Send the username
                sendblock.Encrypt(self._getPaddedPassword(), len(self._getPaddedPassword())) #We encript the password
                #But we send "CCCam" with the password encripted CriptoBlock
                cccamArray = self._getCcam()
                sendcount = self._sendMessage(cccamArray, len(cccamArray), testSocket)
                receivedBytes = bytearray(20)
                recvCount = testSocket.recv_into(receivedBytes, 20)

                if recvCount > 0:
                    recvblock.Decrypt(receivedBytes, 20)
                    if (receivedBytes.decode("ascii").rstrip('\0') == "CCcam"):
                        self._success = True
                    else:
                        raise Exception("Wrong ACK received")
                else:
                    raise Exception("Bad username/password")
            except:
                raise
        except:
            raise
        finally:
            self._ping = time.time() - startTime
            testSocket.close()
        return self.Success

    def _getPaddedUsername(self):
        if not hasattr(self, '_paddedUsername'):
            #We create an array of 20 bytes with the username in it as bytes and padded with 0 behind
            #Like: [23,33,64,13,0,0,0,0,0,0,0...]
            userBytes = array.array("B", self.Username)
            userByteArray = self._fillArray(bytearray(20), userBytes)
            self._paddedUsername = userByteArray
        return self._paddedUsername

    def _getPaddedPassword(self):
        if not hasattr(self, '_paddedPassword'):
            # We create an array of with the password in it as bytes
            # Like: [23,33,64,13,48,78,45]
            passwordBytes = array.array("B", self.Password)
            passwordByteArray = self._fillArray(bytearray(len(self.Password)), passwordBytes)
            self._paddedPassword = passwordByteArray
        return self._paddedPassword

    def _getCcam(self):
        #We create an array of 6 bytes with the "CCcam\0" in it as bytes
        cccamBytes = array.array("B", "CCcam")
        cccamByteArray = self._fillArray(bytearray(6), cccamBytes)
        return cccamByteArray

    def _doHanshake(self, socket):
        import hashlib, array, CriptoBlock

        random = bytearray(16)
        socket.recv_into(random, 16) #Receive first 16 "Hello" random bytes
        self._heloBytes = random

        random = CriptoBlock.Xor(random); #Do a Xor with "CCcam" string to the hello bytes

        sha1 = hashlib.sha1()
        sha1.update(random)
        sha1digest = array.array('B', sha1.digest()) #Create a sha1 hash with the xor hello bytes
        sha1hash = self._fillArray(bytearray(20), sha1digest)

        recvblock.Init(sha1hash, 20) #initialize the receive handler
        recvblock.Decrypt(random, 16)

        sendblock.Init(random, 16) #initialize the send handler
        sendblock.Decrypt(sha1hash, 20)

        rcount = self._sendMessage(sha1hash, 20, socket) #Send the a crypted sha1hash!

    def _sendMessage(self, data, len, socket):
        buffer = self._fillArray(bytearray(len), data)
        sendblock.Encrypt(buffer, len)
        rcount = socket.send(buffer)
        return rcount

    def _fillArray(self, array, source):
        if len(source) <= len(array):
            for i in range(0, len(source)):
                array[i] = source[i]
        else:
            for i in range(0, len(array)):
                array[i] = source[i]
        return array
