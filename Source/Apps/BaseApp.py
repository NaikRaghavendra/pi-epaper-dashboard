import Geometry.Rectangle as RT
import Geometry.Point as PT


class BaseApp:
    def __init__(self, apphost,rect:RT.Rectangle, appPrio = 0):
        self.apphost = apphost
        self._rect:RT.Rectangle = rect
        self._appPrio = appPrio
