#!/usr/bin/python3
#======================================================================
#  Author(s):           Tyler Laudenslager, Christopher Pettinari
#  Major:               Computer Science
#  Creation:            11/2/2021
#  Due:                 12/2/2021
#  Course:              CSC 328
#  Professor:           Dr Frye
#  Assignment:          Group Assignment (Rock, Paper, Scissors)
#  File name:           rps_client.py
#  Purpose:             Client application for a Rock, Paper,
#                       Scissors game
#  Language:            Python
#  Version:             per acad: Python 3.7.3
#  Compile and execute: python rps_client.py
#======================================================================
import socket as sock
import sys
import time
import rps_library as lib

#=======================================================================
#  Function name:   get_command_args
#  Description:     reads in the command line arguments, makes sure
#                   the program can use them, and then returns them
#  Parameters:      none
#  Return value(s): hostname -    hostname of the server that the
#                                 client will connect to
#                   port_number - port number of the process the client
#                                 will connect to
#=======================================================================

def get_command_args():
    """ Function name:   get_command_args

    Description:reads in the command line arguments, makes sure
    the program can use them, and then returns them

    Parameters: none

    Return value(s): 
    hostname -hostname of the server that the client will connect to
    port_number - port number of the process the client will connect to

    """
    port_number = 4500
    if len(sys.argv) > 3 or len(sys.argv) < 2:
         print(f"Usage : {sys.argv[0]} hostname [port_number]")
         sys.exit(-1)
    elif len(sys.argv) == 3:
         *_, hostname, port_number = [ x for x in sys.argv ]
    elif len(sys.argv) == 2:
         *_, hostname = [ x for x in sys.argv ]
    return hostname, int(port_number)

#=======================================================================
#  Function name:   send_nickname
#  Description:     prompts the user for a nickname, then sends
#                   that nickname to the server
#                   
#  Parameters:      player_socket - socket being used for communication
#                                   with the server
#  Return value(s): none
#=======================================================================
def send_nickname(player_socket):
    """ Function name:   send_nickname

    Description: prompts the user for a nickname, then 
    sends that nickname to the server
                   
    Parameters: player_socket - socket being used for communication 
    with the server

    Return value(s): none

    """
    ready_or_retry = None
    while True:
        try:
            nickname = input("Enter a unique nickname to use: ").replace(' ','_')
            lib.send(player_socket, 
                "NICK "+ nickname)
            #this prints if we just connected to the server
            if ready_or_retry == None:
                print("Waiting for other player to connect...")

            ready_or_retry = lib.recv(player_socket)
            if ready_or_retry == "RETRY":
                # nickname refused 
                # (happens if the other player has the same name)
                print("Nickname not unique, please enter a different one")
                continue
            else:
                #This means we are ready
                return
        except OSError as error:
            print(f"Send Error : {error}")
        except ValueError as error:
            print(f"Receive Error : {error}")

#=======================================================================
#  Function name:   rock_paper_scissors
#  Description:     Sends the user's choice of rock, paper,
#                   or scissors.  Also displays information
#                   about the current game
#                   
#  Parameters:      player_socket - socket being used for communication
#                                   with the server
#  Return value(s): none
#=======================================================================
def rock_paper_scissors(player_socket):
    """ Function name: rock_paper_scissors

    Description: Sends the user's choice of rock, paper,
    or scissors. Also displays information about the current game
                   
    Parameters: player_socket - socket being used for communication
    with the server

    Return value(s): none

    """
    rounds = 1
    while rounds > 0:
        try:
            lib.send(player_socket, 
                input("Make your choice('rock', 'paper', 'scissors'): > "))

            msg_recv = lib.recv(player_sock)
            if "invalid" in msg_recv:
                print("Invalid Choice")
                continue
            else:
                enemy_choice, outcome, rounds, enemy_nickname = msg_recv.split(" ")
                rounds = int(rounds)
                print(f"rounds left: {rounds}")
                print(f"{enemy_nickname}'s choice > {enemy_choice}")
                print(f"outcome > {outcome}")
        except OSError as error:
            print(f"Error sending : {error}")
            sys.exit(-1)

#=======================================================================
#  Function name:   print_score
#  Description:     displays the user's score, and whether
#                   or not they won the game
#                   
#  Parameters:      player_socket - socket being used for communication
#                                   with the server
#  Return value(s): stop  -         returned so the program knows
#                                   when the game is over
#=======================================================================
def print_score(player_socket):
    """ Function name:   print_score

    Description: displays the user's score, and whether or not they won the game
                   
    Parameters: player_socket - socket being used for communication with the server

    Return value(s): stop - returned so the program knows when the game is over

    """
    lib.send(player_socket, "OK")
    msg_recv = lib.recv(player_socket)
    score_msg, score_count, stop = msg_recv.split(" ")
    print(f"your score : {score_count} wins")
    return stop

if __name__ == "__main__":

    hostname, host_port_number = get_command_args()

    player_sock = sock.socket()
    #gethostbyname returns ip address : 192.168.2.3
    host_ip = sock.gethostbyname(hostname)
    host_address = (host_ip, host_port_number)
    player_sock.connect(host_address)
    try:
        lib.send(player_sock, "READY")
    except OSError as error:
        print(f"Send Error : {error}")
    #
    try:
        send_nickname(player_sock)
        #There will always be one round
        rock_paper_scissors(player_sock)
        #end_game
        stop = print_score(player_sock)
        if stop != "STOP":
           raise ValueError
    except KeyboardInterrupt as error:
        print("Force Quit...")
    except ValueError as error:
        print("Stop value error")
    finally:
        player_sock.shutdown(sock.SHUT_RDWR)
        player_sock.close()
