"""This module implements a simple listen/notify schema"""

# 20090521 
# - replaced lists by weakKeyDict, do when listener/notifier deleted from all other contexts, its reference is removed 
#   This also implies that there is no order of notifications sent, and objects can only register as listener/notifier once!

# Notes: 
# - member variables "listeners" and "notifiers" are not hidden, but should never be modified directly, so be careful! 
# - subclasses of Listener will want to override the receive_notify class.
# - Notifier/Listener subclasses __init__ method  must call Notifier/Listener.__init__(self) 

import weakref

class Notifier:
    """A notifier keeps a list of Listener instances that are to be informed of certain events.
    
       instance attributes:
        listeners       - a list of Listener instances
    """

    def __init__(self):
        self.listeners = weakref.WeakKeyDictionary()

    def add_listener(self, listener):
        """add a listener to the list (and self to listers' list)"""
        self.listeners[listener] = True
        listener.notifiers[self] = True

    def rem_listener(self, listener):
        """remove a listener from the list (and self from listers' list)"""
        del self.listeners[listener] 
        del listener.notifiers[self] 

    def send_notify(self, message):
        """send a message to all listeners"""
        for dest in self.listeners:
            dest.receive_notify(self, message)

    def __getstate__(self):
        """when pickling... do not save self.listeners"""
        dict = self.__dict__.copy()
        del dict['listeners']
        return dict

    def __setstate__(self, dict):
        """when unpickling... create new self.listeners"""
        self.__dict__ = dict
        self.listeners = weakref.WeakKeyDictionary()

class Listener:
    """A listener is notified by one or more Notifiers.
    
       instance attributes:
        notifiers           - a list of Notifier objects
    """

    def __init__(self):
        self.notifiers = weakref.WeakKeyDictionary();

    def add_notifier(self, notifier):
        """add a notifier to the list (and self to notifiers' list)"""
        self.notifiers[notifier] = True
        notifier.listeners[self] = True

    def rem_notifier(self, notifier):
        """remove a notifier from the list (and self from notifiers' list)"""
        del self.notifiers[notifier]
        del notifier.listeners[self]

    def receive_notify(self, source, message):
        """receive a message from a notifier. Implementing classes should override this."""
        print "receive_notify", self, source,message

    def __getstate__(self):
        """when pickling... do not save self.notifiers"""
        dict = self.__dict__.copy()
        del dict['notifiers']
        return dict

    def __setstate__(self, dict):
        """when unpickling... create new self.notifiers"""
        self.__dict__ = dict
        self.notifiers = weakref.WeakKeyDictionary()


