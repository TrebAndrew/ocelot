import numpy as np

class OpticsElement:
    def __init__(self, eid=None):
        self.eid = eid
        self.domain = "sf"

    def apply(self, dfl):
        pass 
     
#class FreeSpace(OpticsElement):
#    """
#    Drift element
#    """
#    def __init__(self, l=0., mx=1, my=1, eid=None):
#        OpticsElement.__init__(self, eid=eid)
#        self.l = l
#        self.mx = mx
#        self.my = my

class ThinLens(OpticsElement):
    """
    Lens element
    """

    def __init__(self, fx=np.inf, fy=np.inf, eid=None):
        OpticsElement.__init__(self, eid=eid)
        self.fx = fx
        self.fy = fy
        
class Aperture(OpticsElement):
    """
    Aperture
    """

    def __init__(self, eid=None):
        OpticsElement.__init__(self, eid=eid)
        
class ApertureRect(Aperture):
    """
    Rectangular aperture

    """

    def __init__(self, lx=np.inf, ly=np.inf, cx=0., cy=0., eid=None):
        Aperture.__init__(self, eid=eid)
        self.lx = lx
        self.ly = ly
        self.cx = cx
        self.cy = cy


class ApertureEllips(Aperture):
    """
    Elliptical Aperture
    """

    def __init__(self, ax=np.inf, ay=np.inf, cx=0., cy=0., eid=None):
        Aperture.__init__(self, eid=eid)
        self.ax = ax
        self.ay = ay
        self.cx = cx
        self.cy = cy

class OpticsMarker(OpticsElement):
    """
    Drift element
    """
    def __init__(self, eid=None):
        OpticsElement.__init__(self, eid=eid)

    def apply(self, dfl):
        pass


#class ImperfectMirror(OpticsElement):
#    def __init__(self, height_profile=None, hrms=0, lx=np.inf, ly=np.inf, angle=np.pi/2/180, plane='x', eid=None):
#        self.eid = eid
#        self.height_profile = height_profile
#        self.hrms = hrms
#        self.lx = lx
#        self.ly = ly
#        self.angle=angle
#        self.plane=plane

class HeightErrorProfile():
    """
    Drift element
    """
    def __init__(self, hrms=0, lx=1., ly=1., nx=1000, ny=1000, k_cutoff=0., psd=None, eid=None):
        self.eid = eid
        self.hrms = hrms
        self.lx = lx
        self.ly = ly
        self.nx = nx
        self.ny = ny
        self.k_cutoff = k_cutoff
        self.psd = psd
