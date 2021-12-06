#!/usr/bin/python3
#***************************************************************
#* Author: Tyler Laudenslager & Tyler Nazzaro
#* Major: IT
#* Creation Date: 11/5/2021
#* Due date: 12/2/2021
#* Course: CSC 328 Section 010
#* Professor: Dr. Frye
#* Assignment: Group Assignment (Rock, Paper, Scissors)
#* File Name: rps_library.py
#* Purpose:  Common functions between both the client and server
#*           For Rock, paper, scissors
#* Language used and version: Python 3.7.3
#* How to compile and run: Python3 rps_library.py 
#**************************************************************
import socket

class InvalidHeader(Exception):
    """ Custom exception to define
        the error that will occur
        if the message does not have
        the correct header value

    """
    pass

class InvalidFooter(Exception):
    """ Custom exception to define
        the error that will occur
        if the message does not have
        the correct footer value
    
    """
    pass

def _encrypt(msg) -> str:
    """ Function Name:  encrypt

    Description:   Encrypt a message that is going to be sent

    Parameters:     str msg: The message that is to be encrypted

    Return Value:   str - The Encrypted message 

    """
    return "".join([ chr(ord(x)+3) for x in msg ])

def _decrypt(msg) -> str:
    """ Function Name:  decrypt

    Description:    Decrypt the encrypted message that was received

    Parameters:     str msg: The message that was received

    Return Value:   str - The Decrypted message 

    """
    #Decrypt the message received
    return "".join([ chr(ord(x)-3) for x in msg ])

def _get_unicode(code: str) -> chr:
    """ Function Name:  get_unicode

    Description:    Replace the numerical code for a unicode character 
                    with the actual emoji/unicode character

    Parameters:     code: code for the unicode which is a string

    Return Value:   none 

    """
    #Convert the unicode string into a character
    return chr(int(code.lstrip("U+").zfill(8), base=16))

def send(socket, msg):
    """ Function Name:  send

    Description:    Send a message to and from the client/server

    Parameters:     socket: the socket that will be sending information
                    msg: The message that is to be sent

    Return Value:   none 

    """
    try:
        #Warning Sign Emoji
        header = _get_unicode("U+26A0")
        #Skull and Crossbones Emoji
        footer = _get_unicode("U+2620")
        #Put header and footer in their respective place in the encrypted message
        emoji_msg = header + _encrypt(msg) + footer
        socket.sendall(emoji_msg.encode())
    except OSError:
        raise OSError
        
        
def recv(socket, size=1024) -> str:
    """ Function Name:  recv

    Description:    Receive a message from either the client or server

    Parameters:     socket: the socket that will be sending information
                    size: The maximum size of the message being sent in bits

    Return Value:   none 

    """
    #Try to send the message with the header and footer at their respective ends
    try:
        header, *msg, footer = socket.recv(size).decode()
    #Decrypt the  message being sent
        msg = _decrypt(msg)
        #Check if the header and footer are correct
        if header != _get_unicode("U+26A0"):
            raise InvalidHeader
        if footer != _get_unicode("U+2620"):
            raise InvalidFooter
        else:
            return msg
    # Error checking    
    except OSError:
        raise OSError
    except InvalidHeader:
        raise InvalidHeader
    except InvalidFooter:
        raise InvalidFooter
