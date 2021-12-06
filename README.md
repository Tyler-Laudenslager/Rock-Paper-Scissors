# Rock-Paper-Scissors
Multiprocessing Network Game Application written in Python3

Author(s):           Tyler Laudenslager
  Major:               Computer Science
  Due:                 12/2/2021
  Course:              CSC 328
  Professor:           Dr Frye
  Assignment:          (Rock, Paper, Scissors)
  File name:           readme.txt
  Purpose:             readme file for the Rock, Paper, Scissors
                       assignment
  Language:            English (U.S.) (UTF-8)
  Documentation Website: http://www.tlauden.com:8200/final_project_328/index.html
 =======================================================================
 How to build and run the client and server: 
 Server:
 ./rps_server.py (number of rounds) (port # [optional]) &
 Examples: 
 ./rps_server.py 3 4500 &
 ./rps_server.py 1 &

 Client:
 ./rps_client.py (hostname) (port #)
 Examples:

 To connect off of kutztown servers use the following
 ./rps_client.py lauden.cloud 6600

 To run on kutztown.edu use the following
 ./rps_client.py localhost 4500
 ./rps_client.py localhost

 =======================================================================
 File/folder manifest:
 rps_client.py - Client application for the Rock, Paper, Scissors game.
                 Set up to connect to a host running rps_server_multi_fork.py.
 
 rps_server_multi_fork.py - Server application for the Rock, Paper, Scissors game.
                            Allows multiple clients to connect, and have different
							games running concurrently.
 
 rps_library.py - library code to be utilized by the client and server applications
 
 readme.txt - readme file for the Rock, Paper, Scissors assignment.
 
 =========================================================================
 
 Responsibility Matrix:
  Tyler Laudenslager: Server, library, client
  Tyler Nazzaro: Server, library, client
  Christopher Pettinari: Server, library, client
 =========================================================================
 
 Application Protocol:

 1. Client automatically sends "READY" string to server after connecting

 2. Client then sends "NICK" + input from user that defines nickname to use

 3. Client Receives "READYGO" message from server indicating the server is
   ready for the client choice.

 4. Client sends choice of 'rock', 'paper' or 'scissors to the server.

 5. Server sends back the choice of the other player, the outcome (win or lose)
   , rounds left, and the other player's nickname

 6. Go To Step 4 as long as rounds left is greater than zero.

 7. Client sends msg "OK" meaning ok I have indicated no more rounds
   where is the score?

 8. Server sends the final scores to each of the players
   Score message is "SCORE 2 STOP" format.

 9. Client exits

 The message protocol is described here
 http://www.tlauden.com:8200/final_project_328/encryption.html

 =========================================================================
 
 Assumptions:

 The client does not enter a port that is not already in use
 The computer is running the application properly
 The computer functions properly
 The server and client functions as intended
 The server is running in the background
 The user knows how to execute a linux command
 The user knows how to use a keyboard
 
 =========================================================================
 
 Discussions:

 Discussed through Microsoft Teams and exchanged files throught that. We noted when we 
 made changes to certain files. We ended up not using GitLab due to the fact that nobody
 really knew how to use it. We also thought it might be overkill for the project.

 Major problems: We could play one game of rock paper scissors but it would never exit properly so
 that we could play a second game.

 Solution: Redesign of the server to make sure sockets were closing properly and server was looping
           back to the beginning to accept new connections.

 Feature Discussion: We discussed that two players playing the rock paper scissors would be nice. We
                     concluded that it would be better if nobody had to wait for a game to end to start
                     playing the game themselves.
 
 Solution: Redesign the server to pair players up with a referee with each player being a individual
           process that communicates with pipes to the referee which is also a seperate process. This
           allows multiple people to connect and play rock paper scissors without having to worry about
           if someone else is currently playing the game.

 Feature Discussion: Had a very heated debate about which emojis to use in the message protocol.
 
 Solution: Keep it simple. We ended up with a compromise such that we used a hazard emoji instead of a flag
           because the flags we not that great to impart information. Also ending with something dramatic such
           as skull and cross bones to indicate an end to something.
 
 =========================================================================
 
 Status: 
  Server and client function to specifications.	
 
 =========================================================================
