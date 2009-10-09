class Singleton(object):
    def __new__(type, *p, **k):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type)
            type._instance._isNew = True
        else:
            type._instance._isNew = False
        return type._instance
        
class Borg:
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
