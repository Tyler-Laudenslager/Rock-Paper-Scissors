#!/usr/bin/python3
#Author: Tyler Laudenslager
#Major: Computer Science
#Creation Date: 11/2/2021
#Due Date: 12/2/2021
#Course: CSC328-020 Network Secure Programming
#Professor Name: Dr. Frye
#Assignment Number: final_rps_project
#Filename: rps_server.py
#Purpose: The purpose of this program is to
#provide a server that allows multiple concurrent
#games of rock paper scissors to be played with
#a vast amount of players all at the same time.
 
#Language used and version
# Python 3.7.7
#Compliation command - N?A
#Execution Command
# python3 rps_server.py number_of_rounds [port_number] &

# Resources Used:
# Python Cookbook 3rd Edition
# by David Beazley and Brian K. Jones

import socket as s
import multiprocessing as multi
import os
import sys
import rps_library as lib

def rps_player(connects_to_referee, address, client_sock):
    """
    Name: rps_player

    Purpose: This function handles the communication between
             each client for one specific user. Two rps_players 
             will communicate with one rps_referee. 

    Parameters: 
     
    connects_to_parent -> pipe connection between
                          player and referee

    address -> ip and port number in a tuple structure
   
    client_sock -> client socket object -> to send messages to
                   the client

    Return Value: N?A
    """  
    #pipe connection to the referee
    from_referee, to_referee = connects_to_referee
    print(f"Got connection from {address}")
    try:
        while True:
            ready_string = lib.recv(client_sock)
            to_referee.send(ready_string.lower())
            while True:
                nick_msg, nickname = lib.recv(client_sock).split()
                if nick_msg != "NICK":
                   print("Something wrong with nick message")
                   sys.exit(-1)
                to_referee.send(nickname.lower())
                ready_not_ready = from_referee.recv()
                if ready_not_ready == "READY":
                    msg = ready_not_ready + "GO"
                    lib.send(client_sock, msg)
                    break
                else:
                    lib.send(client_sock, ready_not_ready)
                    continue
            while True:
                player_choice = lib.recv(client_sock).lower()
                if not player_choice in ['scissors', 'rock', 'paper']:
                    lib.send(client_sock, "invalid choice")
                    continue
                to_referee.send(player_choice.lower())
                enemy_choice, result, rounds, enemy_name = from_referee.recv()
                combo_message = " ".join([enemy_choice, 
                                          result, 
                                          rounds, enemy_name])
                lib.send(client_sock, combo_message)
                if int(rounds) == 0:
                    break
            score_msg, score_amt = from_referee.recv()
            msg = " ".join([score_msg, score_amt, "STOP"])
            ok_msg = lib.recv(client_sock)
            if ok_msg == "OK":
                lib.send(client_sock, msg)
            break
    except OSError as error:
        print(error, file=sys.stderr)
    except ValueError as error:
        print(error, file=sys.stderr)
    except lib.InvalidHeader as error:
        print("Invalid Header MEssage", file=sys.stderr)
    except lib.InvalidFooter as error:
        print("Invalid Footer Message", file=sys.stderr)
    finally:
        from_referee.close()
        to_referee.close()
        client_sock.shutdown(s.SHUT_RDWR)
        client_sock.close()

def referee_decide(player1_choice, player2_choice, player_scores):
    """ Name: referee_decide

    Purpose: The referee decides who wins a single instance of rock
             paper and scissors.

    Parameters:
   
    player1_choice -> player_one's choice either rock paper or scissors
  
    player2_choice -> player_two's choice either rock paper or scissors
 
    player_scores -> dictionary where each key is a the player name in
                     which the value is the amount of wins so far

    Return Value: N?A
    """   
    #we had a debate on doing the rock paper scissors lizard spock.
    #we decided the world probably wasn't ready for it.
    if player1_choice == 'rock' and player2_choice == 'paper':
        player_scores["player2"] += 1
        return (['paper', 'lose'],['rock', 'win'])
    elif player1_choice == 'rock' and player2_choice == 'scissors':
        player_scores["player1"] += 1
        return (['scissors', 'win'],['rock', 'lose'])
    elif player1_choice == 'rock' and player2_choice == 'rock':
        return (['rock', 'draw'],['rock', 'draw'])
    elif player1_choice == 'paper' and player2_choice == 'rock':
        player_scores["player1"] += 1
        return (['rock','win'],['paper','lose'])
    elif player1_choice == 'paper' and player2_choice == 'scissors':
        player_scores["player2"] += 1
        return (['scissors', 'lose'],['paper', 'win'])
    elif player1_choice == 'paper' and player2_choice == 'paper':
        return (['paper', 'draw'], ['paper', 'draw'])
    elif player1_choice == 'scissors' and player2_choice == 'rock':
        player_scores["player2"] += 1
        return (['rock', 'lose'], ['scissors', 'win'])
    elif player1_choice == 'scissors' and player2_choice == 'paper':
        player_scores["player1"] += 1
        return (['paper', 'win'], ['scissors', 'lose'])
    elif player1_choice == 'scissors' and player2_choice == 'scissors':
        return (['scissors', 'draw'], ['scissors', 'draw'])
   

def rps_referee(player1, player2, rounds_left):
    """
    Name: rps_referee

    Purpose: This is the main referee which handles the choices of two
             rps_players. Keeps the game stable so no arguments arise
             between the two players and returns the scores to each of
             the players respectively.

    Parameters:
 
    player1 -> pipe that connects the referee to player 1
    
    player2 -> pipe that connects the referee to player 2

    rounds_left -> how many rounds that were decided by the
                   operator of the server.

    Return Value: N?A
    """  
    #Pipes to each of the players
    from_player1, to_player1 = player1
    from_player2, to_player2 = player2
    # Get "READY" from both players
    try:
        player1_ready = from_player1.recv()
        player2_ready = from_player2.recv()
    # Get nickname from both players
        while True:
            player1_nickname = from_player1.recv()
            player2_nickname = from_player2.recv()

            if player1_nickname != player2_nickname:
                to_player1.send("READY")
                to_player2.send("READY")
                break
            else:
                to_player1.send("RETRY")
                to_player2.send("RETRY")
                continue
    except EOFError:
        raise EOFError

    # Dictionary to hold player scores
    player_scores = {"player1": 0, "player2": 0}

    while rounds_left > 0:
        rounds_left -= 1
        try:
            player1_choice = from_player1.recv()
            player2_choice = from_player2.recv()
        except EOFError:
            raise EOFError
        # referee decides who wins the round       
        player1_msg, player2_msg = referee_decide(player1_choice, 
                                                  player2_choice,
                                                  player_scores)
        #append rounds_left and the other players nickname
        player1_msg.append(str(rounds_left))
        player1_msg.append(player2_nickname)
        player2_msg.append(str(rounds_left))
        player2_msg.append(player1_nickname)
        #send each player the new message
        to_player1.send(player1_msg)
        to_player2.send(player2_msg)

    #Send scores to the players after the rounds are done
    to_player1.send(("SCORE", str(player_scores["player1"])))
    to_player2.send(("SCORE", str(player_scores["player2"])))
        
    
def rps_server(s_sock, rounds):
    """ Name: rps_server

    Purpose: provide a multi-client multiprocessing tcp server that
             handles infinite rock paper scissors games concurrently. 

    Parameters: 
    
    s_sock -> server socket that has been put in passive mode
    and bound to the local machine.

    rounds -> unsigned integer that defines how many rounds of rock
    paper are to be played.

    Return Value: N?A
    """ 
    #create a list that hold player pipes to give to referee to manage  
    player_connects = list()
    #keep track of players that connect to network
    player_count = 0
    while True:
        client_sock, client_addr = s_sock.accept()
        player_count += 1
        #create two pipes one pipe that sends messages to the player
        #the other pipe sends messages to the referee
        to_player, from_referee = multi.Pipe()
        to_referee, from_player = multi.Pipe()
        #save the pipes appropriate for the referee to use
        player_connects.append((to_player, from_player))
        pid = os.fork()
        if pid < 0:
            #fork error occurred
            sys.exit(-1)
        elif pid == 0:
            #close pipes
            to_player.close()
            from_player.close()
            #create a new player in a seperate process
            rps_player((to_referee, from_referee),
                        client_addr,
                        client_sock)
            sys.exit(0)
        else:
            #if we dont have two players we need to wait
            #for another user to connect this loops back
            #to the beginning
            if player_count != 2:
                #we need to close all unused 
                #file descriptors in the parent
                client_sock.close()
            else:
                #otherwise we create a seperate process for
                #the referee to exist in
                pid = os.fork()
                if pid < 0:
                    #error with the fork
                    sys.exit(-1)
                elif pid == 0:
                    #create a new referee that manages the
                    #last two players that connected
                    try:
                        rps_referee(player_connects[0],
                                    player_connects[1],
                                    rounds)
                    except EOFError as error:
                        print(error, file=sys.stderr)
                    finally:
                        sys.exit(0)
                else:
                    #Reset the variables and allow
                    #two more players to connect
                    #no matter how many games are
                    #currently being played
                    print("Reset..")
                    player_count = 0
                    player_connects = list()
                    continue 

def get_command_arguments():
    """ Name: get_command_arguments 

    Purpose: to get the user command line arguments
    
    Parameters: N?A
    
    Return Value: (tuple) -> rounds, port_number
    """  
    #default port number
    port_number = 4500
    #if there are two command arguments
    if len(sys.argv) == 3:
        *_, rounds, port_number = [ x for x in sys.argv ]
    #if there is one command argument
    elif len(sys.argv) == 2:
        *_, rounds = [ x for x in sys.argv ]
        if not int(rounds) > 0:
            print(f"Usage {sys.argv[0]} rounds_per_game [port_number] &")
            sys.exit(-1)
    else:
        #Otherwise print usage clause
        print(f"Usage {sys.argv[0]} rounds_per_game [port_number] &")
        sys.exit(-1)

    return rounds, port_number

# Entry point in the program. The code below will
# not execute if the program is being imported
# into another file.
if __name__ == '__main__':
    #backlog is the number of connections that should be queued.
    backlog = 10
    rounds, port_number = get_command_arguments()

    try:
        s_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        #this allows the server to use the same address again
        s_sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        s_sock.bind(('', int(port_number)))
        s_sock.listen(backlog) 
        rps_server(s_sock, int(rounds))
    except OSError as error:
        print(f"OS Error : {error}")
