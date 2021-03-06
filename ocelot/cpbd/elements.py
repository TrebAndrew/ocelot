"""
definition of magnetic lattice
linear dimensions in [m]
"""

from ocelot.cpbd.field_map import FieldMap
import numpy as np


class Element(object):
    """
    Element is a basic beamline building element
    Accelerator optics elements are subclasses of Element
    Arbitrary set of additional parameters can be attached if necessary
    """
    def __init__(self, eid=None):
        self.id = eid
        if eid is None:
            self.id = "ID_{0}_".format(np.random.randint(100000000))
        self.l = 0.
        self.tilt = 0.  # rad, pi/4 to turn positive quad into negative skew
        self.angle = 0.
        self.k1 = 0.
        self.k2 = 0.
        self.dx = 0.
        self.dy = 0.
        self.dtilt = 0.
        self.params = {}
    
    def __hash__(self):
        return hash(id(self))
        #return hash((self.id, self.__class__))

    def __eq__(self, other):
        try:
            #return (self.id, type) == (other.id, type)
            return id(self) == id(other)
        except:
            return False
    

# to mark locations of bpms and other diagnostics
class Monitor(Element):
        
    def __init__(self, l=0.0, eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.x_ref = 0.
        self.y_ref = 0.
        self.x = 0.
        self.y = 0.


class Marker(Element):
    def __init__(self, eid=None):
        Element.__init__(self, eid)
        self.l = 0.


class Quadrupole(Element):
    """
    quadrupole
    l - length of lens in [m],
    k1 - strength of quadrupole lens in [1/m^2],
    k2 - strength of sextupole lens in [1/m^3],
    tilt - tilt of lens in [rad].
    """
    def __init__(self, l=0., k1=0, k2=0., tilt=0., eid=None):
        #Element.__init__(self, eid)
        super(Quadrupole, self).__init__(eid=eid)
        self.l = l
        self.k1 = k1
        self.k2 = k2
        self.tilt = tilt


class Sextupole(Element):
    """
    sextupole
    l - length of lens in [m],
    k2 - strength of sextupole lens in [1/m^3].
    """
    def __init__(self, l=0., k2=0., tilt=0., eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.k2 = k2
        self.tilt = tilt


class Octupole(Element):
    """
    octupole
    k3 - strength of sextupole lens in [1/m^4],
    l - length of lens in [m].
    """
    def __init__(self, l=0., k3=0., tilt=0., eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.k3 = k3
        self.tilt = tilt


class Drift(Element):
    """
    drift - free space
    l - length of drift in [m]
    """
    def __init__(self, l=0., eid=None):
        Element.__init__(self, eid)
        self.l = l


class Bend(Element):
    """
    bending magnet
    l - length of magnet in [m],
    angle - angle of bend in [rad],
    k1 - strength of quadrupole lens in [1/m^2],
    k2 - strength of sextupole lens in [1/m^3],
    tilt - tilt of lens in [rad],
    e1 - the angle of inclination of the entrance face [rad],
    e2 - the angle of inclination of the exit face [rad].
    fint - fringe field integral
    fintx - allows (fintx > 0) to set fint at the element exit different from its entry value.
    gap - the magnet gap [m], NOTE in MAD and ELEGANT: HGAP = gap/2
    h_pole1 - the curvature (1/r) of the entrance face
    h_pole1 - the curvature (1/r) of the exit face
    """
    def __init__(self, l=0., angle=0., k1=0., k2=0., e1=0., e2=0., tilt=0.0,
                 gap=0., h_pole1=0., h_pole2=0., fint=0., fintx=None, eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.angle = angle
        self.k1 = k1
        self.k2 = k2
        self.e1 = e1
        self.e2 = e2
        self.gap = gap
        self.h_pole1 = h_pole1
        self.h_pole2 = h_pole2
        self.fint = fint
        self.fintx = fint
        if fintx is not None:
            self.fintx = fintx
        self.tilt = tilt


class Edge(Bend):
    def __init__(self, l=0., angle=0.0, k1=0., edge=0.,
                 tilt=0.0, dtilt=0.0, dx=0.0, dy=0.0,
                 h_pole=0., gap=0., fint=0., pos=1, eid=None):
        Element.__init__(self, eid)
        if l != 0.:
            self.h = angle/l
        else:
            self.h = 0
        self.l = 0.
        self.k1 = k1
        self.h_pole = h_pole
        self.gap = gap
        self.fint = fint
        self.edge = edge
        self.dx = dx
        self.dy = dy
        self.dtilt = dtilt
        self.tilt = tilt
        self.pos = pos


class SBend(Bend):
    """
    sector bending magnet,
    l - length of magnet in [m],
    angle - angle of bend in [rad],
    k1 - strength of quadrupole lens in [1/m^2],
    k2 - strength of sextupole lens in [1/m^3],
    tilt - tilt of lens in [rad],
    e1 - the angle of inclination of the entrance face [rad],
    e2 - the angle of inclination of the exit face [rad].
    fint - fringe field integral
    fintx - allows (fintx > 0) to set fint at the element exit different from its entry value.
    gap - the magnet gap [m], NOTE in MAD and ELEGANT: HGAP = gap/2
    h_pole1 - the curvature (1/r) of the entrance face
    h_pole1 - the curvature (1/r) of the exit face
    """
    def __init__(self, l=0., angle=0.0, k1=0.0, k2=0., e1=0.0, e2=0.0, tilt=0.0,
                 gap=0, h_pole1=0., h_pole2=0., fint=0., fintx=None, eid=None):

        Bend.__init__(self, l=l, angle=angle, k1=k1, k2=k2, e1=e1, e2=e2, tilt=tilt,
                      gap=gap, h_pole1=h_pole1, h_pole2=h_pole2, fint=fint, fintx=fintx, eid=eid)


class RBend(Bend):
    """
    rectangular bending magnet,
    l - length of magnet in [m],
    angle - angle of bend in [rad],
    k1 - strength of quadrupole lens in [1/m^2],
    k2 - strength of sextupole lens in [1/m^3],
    tilt - tilt of lens in [rad],
    e1 - the angle of inclination of the entrance face [rad],
    e2 - the angle of inclination of the exit face [rad].
    fint - fringe field integral
    fintx - allows (fintx > 0) to set fint at the element exit different from its entry value.
    gap - the magnet gap [m], NOTE in MAD and ELEGANT: HGAP = gap/2
    h_pole1 - the curvature (1/r) of the entrance face
    h_pole1 - the curvature (1/r) of the exit face
    """
    def __init__(self, l=0., angle=0., k1=0., k2=0., e1=None, e2=None, tilt=0.,
                 gap=0, h_pole1=0., h_pole2=0., fint=0., fintx=None, eid=None):
        if e1 is None:
            e1 = angle/2.
        else:
            e1 += angle/2.
        if e2 is None:
            e2 = angle/2.
        else:
            e2 += angle/2.

        Bend.__init__(self, l=l, angle=angle, e1=e1, e2=e2, k1=k1, k2=k2, tilt=tilt,
                      gap=gap, h_pole1=h_pole1, h_pole2=h_pole2, fint=fint, fintx=fintx, eid=eid)


class XYQuadrupole(SBend):
    """
    Quadrupole with offsets (linear element),
    l - length of magnet in [m],
    k1 - strength of quadrupole lens in [1/m^2],
    x_offs - offset in horizontal direction in [m]
    y_offs - offset in vertical direction in [m]
    tilt - tilt of lens in [rad],
    """
    def __init__(self, l=0., x_offs=0.0, y_offs=0.0, k1=0.0, tilt=0.0, eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.k1 = k1
        self.x_offs = x_offs
        self.y_offs = y_offs
        self.tilt = tilt


class Hcor(RBend):
    """
    horizontal corrector,
    l - length of magnet in [m],
    angle - angle of bend in [rad],
    """
    def __init__(self, l=0., angle=0., eid=None):
        RBend.__init__(self, l=l, angle=angle, eid=eid)
        self.l = l
        self.angle = angle
        self.tilt = 0.


class Vcor(RBend):
    """
    horizontal corrector,
    l - length of magnet in [m],
    angle - angle of bend in [rad],
    """
    def __init__(self, l=0., angle=0., eid=None):
        RBend.__init__(self, l=l, angle=angle, eid=eid)
        self.l = l
        self.angle = angle
        self.tilt = np.pi/2.


class Undulator(Element):
    """
    Undulator
    lperiod - undulator period in [m];\n
    nperiod - number of periods;\n
    Kx - undulator paramenter for vertical field; \n
    Ky - undulator parameter for horizantal field;\n
    field_file - absolute path to magnetic field data;\n
    mag_field - None by default, the magnetic field map function - (Bx, By, Bz) = f(x, y, z)
    eid - id of undulator.
    """
    def __init__(self, lperiod=0., nperiods=0, Kx=0., Ky=0., field_file=None, eid=None):
        Element.__init__(self, eid)
        self.lperiod = lperiod
        self.nperiods = nperiods
        self.l = lperiod * nperiods
        self.Kx = Kx
        self.Ky = Ky
        self.solver = "linear"    # can be "lin" is linear matrix,  "sym" - symplectic method and "rk" is Runge-Kutta
        self.phase = 0.           # phase between Bx and By + pi/4 (spiral undulator)
        
        self.ax = -1              # width of undulator, when ax is negative undulator width is infinite
                                  # I need this for analytic description of undulator
        
        self.field_file = field_file
        self.field_map = FieldMap(self.field_file)
        self.mag_field = None     # the magnetic field map function - (Bx, By, Bz) = f(x, y, z)
        self.v_angle = 0.
        self.h_angle = 0.
                            
    def validate(self):
        pass
                            
        # maybe we will do two functions
        # 1. load data and check magnetic map
        # 2. check all input data (lperiod nperiod ...). something like this we must do for all elements.

        # what do you think about ending poles? We can do several options
        # a) 1/2,-1,1,... -1,1/2
        # b) 1/2,-1,1,... -1,1,-1/2
        # c) 1/4,-3/4,1,-1... -1,3/4,-1/4   I need to check it.


class Cavity(Element):
    """
    Standing wave RF cavity
    v - voltage [GV]
    freq - frequency [Hz]
    phi - phase in [deg]
    """
    def __init__(self, l=0., v=0., phi=0., freq=0., volterr=0., eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.v = v   # in GV
        self.freq = freq   # Hz
        self.phi = phi  # in grad
        self.E = 0
        self.volterr = volterr
        self.coupler_kick = False


class TWCavity(Element):
    """
    Traveling wave cavity
    v - voltage [GV]
    freq - frequency [Hz]
    phi - phase in [deg]
    """
    def __init__(self, l=0., v=0., phi=0., freq=0., eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.v = v   # in GV
        self.freq = freq   # Hz
        self.phi = phi  # in grad
        self.E = 0
        self.coupler_kick = False


class TDCavity(Element):
    """
    Transverse deflecting cavity - by default kick in horizontal plane

    l - length [m]
    v - voltage [GV/m]
    freq - frequency [Hz]
    phi - phase in [deg]
    tilt - tilt of cavity in [rad]
    """
    def __init__(self, l=0., freq=0.0, phi=0.0, v=0., tilt=0.0, eid=None):
        Element.__init__(self, eid)
        self.l = l
        self.v = v   # in GV
        self.freq = freq   # Hz
        self.phi = phi  # in deg
        self.tilt = tilt


class Solenoid(Element):
    """
    Solenoid
    l - length in m,
    k - strength B0/(2B*rho)
    """
    def __init__(self, l=0., k=0., eid=None):
        Element.__init__(self, eid)
        self.k = k  # B0/(2B*rho)
        self.l = l


class Multipole(Element):
    """
    kn - list of strengths
    """
    def __init__(self, kn=0., eid=None):
        Element.__init__(self, eid)
        kn = np.array([kn]).flatten()
        if len(kn) < 2:
            self.kn = np.append(kn, [0.])
        else:
            self.kn = kn
        self.n = len(self.kn)
        self.l = 0.


class Matrix(Element):
    """
    Matrix element

    l = 0 - m, length of the matrix element
    r = np.zeros((6, 6)) - R - elements, first order
    t = np.zeros((6, 6, 6)) - T - elements, second order
    delta_e = 0 - GeV, energy gain along the matrix element
    """
    def __init__(self, l=0., delta_e=0, eid=None, **kwargs):
        Element.__init__(self, eid)
        self.l = l

        self.r = np.zeros((6, 6))
        self.t = np.zeros((6, 6, 6))
        # zero order elements - test mode, not implemented yet
        self.b = np.zeros((6, 1))

        for y in kwargs:
            # decode first order arguments in format RXX or rXX where X is number from 1 to 6
            if "r" in y[0].lower() and len(y) > 2:
                if "m" in y[1].lower() and len(y) == 4 and y[2:].isdigit() and (11 <= int(y[2:]) <= 66):
                    self.r[int(y[2]) - 1, int(y[3]) - 1] = float(kwargs[y])
                if len(y) == 3 and y[1:].isdigit() and (11 <= int(y[1:]) <= 66):
                    self.r[int(y[1]) - 1, int(y[2]) - 1] = float(kwargs[y])

            # decode second order arguments in format TXXX or tXXX where X is number from 1 to 6
            if "t" in y[0].lower() and len(y) == 4 and y[1:].isdigit() and (111 <= int(y[1:]) <= 666):
                self.t[int(y[1]) - 1, int(y[2]) - 1, int(y[3]) - 1] = float(kwargs[y])

            # decode zero order arguments in format BX or bX where X is number from 1 to 6
            if "b" in y[0].lower() and len(y) == 2 and y[1:].isdigit() and (1 <= int(y[1:]) <= 6):
                self.b[int(y[1]) - 1, 0] = float(kwargs[y])
        self.delta_e = delta_e


class Pulse:
    def __init__(self):
        self.kick_x = lambda tau: 0.0
        self.kick_y = lambda tau: 0.0
        self.kick_z = lambda tau: 0.0


class UnknownElement(Element):
    """
    l - length of lens in [m]
    """
    def __init__(self, l=0, kick=0, xsize=0, ysize=0, volt=0, lag=0, harmon=0, refer=0, vkick=0, hkick=0, eid=None):
        Element.__init__(self, eid)
        self.l = l


class Sequence:
    def __init__(self, l=0, refer=0):
        self.l = l


def survey(lat, ang=0.0, x0=0, z0=0):
    x = []
    z = []
    for e in lat.sequence:
        x.append(x0)
        z.append(z0)
        if e.__class__ in [Bend, SBend, RBend]:
            ang += e.angle
        x0 += e.l*np.cos(ang)
        z0 += e.l*np.sin(ang)
    return x, z, ang

if __name__ == "__main__":
    a = RBend(l=13)