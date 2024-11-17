import pygame as pg

#honestly one of the coolest parts of the code. event handler class that can create different kinds of events
#other objects can then subsribe to these events and seperate parts of code can publish the event
#helps with decoupling objects from one another by using this as an overlap between them




class Publisher:#publisher class
    def __init__(self) -> None:
        self.subscribers = {}#dict of subscribers

    def subscribe(self, subscriber, callback):
        #when subscribing pass in the subscriber and specify the callback. 
        #the callback is a function object that is stored as the value in the dict, with the subscriber as the key
        h = hash(str(subscriber))
        self.subscribers[h] = callback

    def unsubscribe(self, subscriber):#remove a subscriber
        self.subscribers.pop(hash(str(subscriber)))
        # print(self.subscribers)

    def publish(self, *args):#publish method. loops through all subscribers and runs the callback with args given in the parameter
        for sub in self.subscribers:
            self.subscribers[sub](*args)

#Extra Note: Most of the publishers are declared inside the class outside the constructor. This makes them static attributes
#which allows me to access them without an instance of the class



