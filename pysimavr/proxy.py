

class Proxy(object):
    _reserved = []
    def __init__(self):
        pass
    
    def __getattribute__(self, name):
        if name == 'backend' or name.startswith('_') or name  in self._reserved:
            return object.__getattribute__(self, name)
        else:
            return getattr(object.__getattribute__(self, 'backend'), name)
#    def __delattr__(self, name):
#        delattr(object.__getattribute__(self, "_obj"), name)
    def __setattr__(self, name, value):
        if name == 'backend' or name.startswith('_') or name  in self._reserved:
            object.__setattr__(self, name, value)
        else:
            setattr(object.__getattribute__(self, 'backend'), name, value)

