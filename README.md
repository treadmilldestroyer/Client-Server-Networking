# Client to Server File Transfer System

This repository has two main files, client.py and server.py. These two files for to two different machines, one for the client and one for the server. In the client file, there are two functions, an upload function and a download function. The upload function uploads a local file from the client to the server. The download function gives a file that is store on the server to the client. 

## Instructions for Build and Use

[Software Demo](https://www.youtube.com/watch?v=ByRG5VAf7MU)

Steps to build and/or run the software:

1. The server needs to be listening for connections to devices. 
2. SSH into server.
3. Turn server on by running server.py function on the EC2 instance.
4. Turn on client by running client.py function on client device.
5. Upload and download as desired.

Instructions for using the software:

1. After you've turned on the server and it is listening for clients and the client is turned on, choose to upload or download a file.
2. Enter the file name. 
3. Rerun client.py function each time you'd like to perform a function. (Each time a connection is established, the server will disconnect from the client to be able to allow other devices or clients to connect to server.)

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.14.2
* AWS account 
* Access to AWS EC2 t3.micro instance
* Inbound rule for communication to client and SSH in terminal

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Gemini](https://gemini.google.com/u/0/app)
* [Real Python](https://realpython.com/python-sockets/)


## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] I would like to add more functions to the system. Maybe a way to "ls" the server from the client.
* [ ] Another addition I would make would be to update the communication messages to be a little more descriptive and user friendly.