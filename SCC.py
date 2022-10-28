import scratchattach
from random import random
from random import seed
import time



seed(time.time())


primelist = [109] # is this a security issue? yes. will anyone ever read this and will i change it? nah
users = {} # users to keep in memory for auth keys 'n stuff


session = scratchattach.login("-FreeEngines-", "thisisnotmypassword") # obviously, login lol
conn = session.connect_cloud("750457625") # init cloud connection to the project lol


client = scratchattach.CloudRequests(conn) # get a client (yeah thats needed aswell)

@client.request # listening for noumerous requests
def prime(): # returns a prime number which is essentially the prime number of the shared public key
	p = primelist[round(random()*len(primelist))-1]
	usr = str(client.get_requester())
	if usr in users:
		del users[usr]
	users[usr] = {"p": None, "g": None, "a": None, "g2": None, "g3": None, "key": None}
	print(users)
	users[usr]["p"] = p
	return p

@client.request
def g(): # returns the first g, which is the non prime part of the shared public key
	g = round(random()*2000)
	usr = str(client.get_requester())
	users[usr]["g"] = g
	return g

@client.request
def g2(garg): # asks the server to generate a private key, instantly returns the second "version" of the public key. (the client at this point should have generated a private key and sends the pow thing as the g2 argument)
	usr = str(client.get_requester())
	a = round(random()*(users[usr]["p"]-1))
	users[usr]["a"] = a
	users[usr]["g2"] = garg
	return pow(int(users[usr]["g"]), a, int(users[usr]["p"]))

@client.request
def g3(): # here, the client sends over the next veresion of g^b%p, taking this to the power of a % p will result in having a shared key (the server has to return his values for that aswell tho) 
	usr = str(client.get_requester())
	users[usr]["key"] = pow(int(users[usr]["g2"]),int(users[usr]["a"]), int(users[usr]["p"]))
	print(f"SHARED KEY IS {users[usr]['key']}")
	return 0





client.run()
