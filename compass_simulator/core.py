"""
===========================================================================
Modelize the static and dynamic behaviour ok an orienteering compass in the
Earth magnetic field
Every parameters are in international system units, angles in radians
===========================================================================

"""

# 1/ Imports

import math
import copy

from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import xlrd

# 2/ Constants

MAG_PER = 1.25664e-06 # Magnetic permitivity
G = 9.81 # gravity acceleration

# 3/ Classes

class Compass:
    """
    Representing an orienteering compass
    Default is for GEONAUTE R500 compass
    
    Attributes:
    name: name of the compass
    needle_length: metters
    needle_width: metters
    needle_thickness: metters
    needle_disk_density: kg/m^3 default is PEHD 1200
    disk_radius: friction disk radius, metters
    disk_thickness: metters
    mag_rem: magnet remanent magnetic field, Tesla
    V: magnet volume, m^3
    m: magnet mass, kg 
    magnet_mom_z: inertial moment of the magnet related to its z axis, kg.m^2
    x: x offset of magnet mass center, metters
    rho: liquid volumic mass, kg/m^3
    viscosity: liquid dynamic viscosity, kg/m/s

    Properties:
    mom_z: inertial moment of the rotating assembly related to z axis
    visc_coef: viscous coeficient for the frictions between liquid and disk + 
    needle
    """

    def __init__(self,
        name="R500",
        needle_length=0.032,
        needle_width=0.008,
        needle_thickness=0.00025,
        needle_disk_density=1200,
        disk_radius=0.0115,
        disk_thickness=0.0001,
        mag_rem=1.3,
        V=6e-8,
        m=0.00045,
        magnet_mom_z=5.1e-09,
        x=-0.0005,
        rho=700,
        viscosity=1.08,
        z_h=0.004,
        z_b=0.004,
    ):
        self.name = name
        self.needle_length = needle_length
        self.needle_width = needle_width
        self.needle_thickness = needle_thickness
        self.needle_disk_density = needle_disk_density
        self.disk_radius = disk_radius
        self.disk_thickness = disk_thickness
        self.mag_rem = mag_rem
        self.V = V
        self.m = m
        self.magnet_mom_z = magnet_mom_z
        self.x = x
        self.rho = rho
        self.viscosity = viscosity
        self.z_h = z_h
        self.z_b = z_b
    
    @property
    def mom_z(self):
        """
        inertial moment of needle assembly related to z axis
        """
        disk_mom = math.pi * math.pow(self.disk_radius, 4) * \
            self.disk_thickness * self.needle_disk_density / 2
        
        needle_mom = self.needle_length * self.needle_width * \
            self.needle_thickness * self.needle_disk_density * \
            (math.pow(self.needle_length, 2) + \
            math.pow(self.needle_width, 2)) / 12
        
        mom = disk_mom + needle_mom + self.magnet_mom_z + self.m * math.pow(self.x, 2)
        #mom = 7.8e-9
        return mom

    @property
    def visc_coef(self):
        """
        inertial moment of needle assembly related to z axis
        """
        coef = self.viscosity * (1 / self.z_h + 1 / self.z_b) * (math.pi * \
            math.pow(self.disk_radius, 4) / 2 + \
            (math.pow(self.needle_length, 3) / 8 - math.pow(self.disk_radius, \
            3)) * self.needle_width / 3 + (self.needle_length / 2 - \
            self.disk_radius) * math.pow(self.needle_width, 3) / 12)
        #coef = 8e-8
        return coef


class MagneticField:
    """
    Representing the magnetic field at a given position on Earth
    Default is for Lille in France

    Attributes:
    name: name of the location
    lat: latitude
    lon: longitude
    int: Earth magnetic field intensity in Tesla
    i_deg: Magnetic field inclination in degrees, positive when pointing down

    Properties:
    i: Magnetic field inclination in radians, positive when pointing down
    """
    
    def __init__(self, name="Lille", lat=50.6333, lon=3.0667,
        intensity=4.8699e-5, i_deg=65.822):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.int = intensity
        self.i_deg = i_deg


    @property
    def i(self):
        """
        Magnetic field inclination in radians, positive when pointing down
        """
        return math.radians(self.i_deg)


class Balance:
    """
    Computing the balance tests of the compass

    Attributes:
    comp: Compass object
    mg_fld: MagneticField object
    theta_lim: Limit angle of lateral inclination of the compass, degrees
    alpha_lim: Limit of tolerance for the angle between the needle and the 
    north when inclining the compass

    Properties:
    x_opti: optimal offset of the magnet so the compass is perfectly balanced
    for the given magnetic field.
    alpha_err: angle of the needle with north when the compass is inclined of
    theta_lim
    """

    def __init__(self, comp, mg_fld, theta_lim=40, alpha_lim=0):
        self.comp = comp
        self.mg_fld = mg_fld
        self.theta_lim = theta_lim
        self.alpha_lim = alpha_lim

    @property
    def x_opti(self):
        """
        The optimal offset of the magnet so the compass is perfectly balanced
        for the given magnetic field
        """
        return -self.comp.mag_rem * self.comp.V * self.mg_fld.int * \
            math.sin(self.mg_fld.i) / (MAG_PER * (self.comp.m - \
            self.comp.rho * self.comp.V) * G)
    
    @property
    def alpha_err(self):
        """
        Calculate the angle of the needle with north when the compass is inclined of theta_lim
        """
        return math.atan(((self.comp.rho * self.comp.V - self.comp.m) * \
            G * self.comp.x * MAG_PER / (self.comp.mag_rem * self.mg_fld.int *\
            math.cos(self.mg_fld.i)) - math.tan(self.mg_fld.i)) * \
            math.sin(math.radians(self.theta_lim)))


class Dynamic:
    """
    Class for rapidity and stability tests

    Attributes:
    comp: Compass tested
    mg_fld: Magnetic field for the test
    alpha_init_deg: Initial needle angle in degrees
    tf_rap: Final time rapidity test in seconds
    tf_stab: Final time stability test in seconds
    t_int: Integration time interval in seconds
    Y: Oscillation range in meters
    f: Oscillation frenquency in steps (double steps) per minutes
    exp_coef_mg: Ajustment coeficient to ajuste the simulation with
        experimental results
    exp_coef_visc: Ajustment coeficient to ajuste the simulation with
        experimental results
    tho_lim: Limit for tho in degrees, default 5°

    tho: Time when the angle of the needle stay under tho_lim compared to
        north, for rapidity test
    stab_amp: Amplitude of the needle oscillation for the stability test,
        calculated for the second half of the time range. Degrees
    """
    def __init__(self,
        comp,
        mg_fld,
        alpha_init_deg=90,
        tf_rap=3,
        tf_stab=5,
        t_int=0.01,
        Y=0.093,
        f=70,
        exp_coef_mg=1,
        exp_coef_visc=1,
        tho_lim=5,
    ):
        self.comp = comp
        self.mg_fld = mg_fld
        self.alpha_init_deg = alpha_init_deg
        self.tf_rap = tf_rap
        self.tf_stab = tf_stab
        self.t_int = t_int
        self.Y = Y
        self.f = f
        self.exp_coef_mg = exp_coef_mg
        self.exp_coef_visc = exp_coef_visc
        self.tho_lim = tho_lim

        self.t_rap = np.arange(0, self.tf_rap, self.t_int) # Time range for rapidity
        self.t_stab = np.arange(0, self.tf_stab, self.t_int) # Time range for stability
        self.rapidity_results = None
        self.stability_results = None
        self.stability_results_s = None
        self.rapidity_results_s = None
        self.rapidity_results_exp = None
        self.tho = None
        self.stab_amp = None
    
    @property
    def alpha_init(self):
        return math.radians(self.alpha_init_deg)

    @property
    def w(self):
        return math.pi * self.f / 60

    # Parameters for exact simulation

    @property
    def mg_trm(self):
        """
        Magnetic term of the second order equation.
        """
        return -self.exp_coef_mg * self.comp.mag_rem * self.comp.V * \
            self.mg_fld.int * math.cos(self.mg_fld.i) / (MAG_PER * \
            self.comp.mom_z)

    @property
    def visc_trm(self):
        """
        Viscous term of the second order equation.
        """
        # The following comment return a viscous term that match with the
        # experimental plot shape
        # return -6 * math.sqrt(-self.mg_trm) / 5
        return -self.exp_coef_visc * self.comp.visc_coef / self.comp.mom_z
    
    @property
    def ext_trm(self):
        """
        external excitation term of the second order equation.
        """
        return self.comp.m * self.comp.x * self.Y * math.pow((math.pi * \
            self.f / 30), 2) / self.comp.mom_z
    
    # Parameters for simplified simulation (small angles hypothesis)

    @property
    def amplification(self):
        """
        Amplification factor if small angles hypothesis (linear equation).
        """
        return 1 / (math.sqrt(math.pow(self.mg_trm * self.comp.mom_z - \
            self.comp.mom_z * math.pow(self.w, 2), 2) + \
            math.pow(self.comp.visc * self.w, 2)))
    
    @property
    def phase(self):
        """
        Phase offset if small angles hypothesis (linear equation).
        """
        return math.atan(self.comp.visc * self.w / (self.comp.mom_z * \
            math.pow(self.w, 2)) - self.mg_trm * self.comp.mom_z)
    
    def rapidity(self):
        def F(t, x):
            xdot = [[],[]]
            xdot[0] = self.mg_trm * math.sin(x[1]) + self.visc_trm * x[0]
            xdot[1] = x[0]
            return xdot
        sol = solve_ivp(fun=F, t_span=(0, self.tf_rap),
            y0=[0, self.alpha_init], t_eval=self.t_rap,
        )
        self.rapidity_results = np.degrees(sol.y[1])
        self.calculate_tho()

    def rapidity_simple(self):
        def F(t, x):
            xdot = [[],[]]
            xdot[0] = self.mg_trm * x[1] + self.visc_trm * x[0]
            xdot[1] = x[0]
            return xdot
        sol = solve_ivp(fun=F, t_span=(0, self.tf_rap),
            y0=[0, self.alpha_init], t_eval=self.t_rap,
        )
        self.rapidity_results_s = sol.y[1]
    
    def rapidity_exp(self, file_name):
        doc = xlrd.open_workbook(file_name)
        sheet_1 = doc.sheet_by_index(0)
        rows = sheet_1.nrows
        time = []
        alpha = []
        for r in range(1, rows):
            time.append(sheet_1.cell_value(rowx=r, colx=0))
            alpha.append(sheet_1.cell_value(rowx=r, colx=1))
            if abs(sheet_1.cell_value(rowx=r, colx=1)) > 5:
                self.tho = sheet_1.cell_value(rowx=r, colx=0)
        self.rapidity_results_exp = (time, alpha)
    
    def stability(self):
        def F(t, x):
            xdot = [[],[]]
            xdot[0] = self.mg_trm * math.sin(x[1]) + self.visc_trm * x[0] + \
                self.ext_trm * math.cos(x[1]) * math.sin(math.pi * self.f * \
                t / 30)
            xdot[1] = x[0]
            return xdot
        sol = solve_ivp(fun=F, t_span=(0, self.tf_stab), y0=[0, 0],
            t_eval=self.t_stab,
        )
        self.stability_results = np.degrees(sol.y[1])
        self.calculate_stab_amp()
    
    def stability_simple(self):
        def F(t, x):
            xdot = [[],[]]
            xdot[0] = self.mg_trm * x[1] + self.visc_trm * x[0] + \
                self.ext_trm * math.sin(math.pi * self.f * t / 30)
            xdot[1] = x[0]
            return xdot
        sol = solve_ivp(fun=F, t_span=(0, self.tf_stab), y0=[0, 0],
            t_eval=self.t_stab
        )
        self.stability_results_s = sol.y[1]

    def display_stab(self):
        plt.plot(self.t_stab, self.stability_results)
        #stab_sa = [(self.amplification * math.cos(self.w * t + self.phase)) for t in self.t_stab]
        #if self.stability_results_s != None:
        #plt.plot(self.t_stab, self.stability_results_s)
        plt.show()

    def display_rap(self):
        plt.plot(self.t_rap, self.rapidity_results)
        #if self.rapidity_results_s != None:
        #plt.plot(self.t_rap, self.rapidity_results_s)
        if self.rapidity_results_exp != None:
            plt.plot(self.rapidity_results_exp[0], self.rapidity_results_exp[1])
        plt.show()
    
    def calculate_tho(self):
        """
        Calculate tho 
        """
        for i in range(1, len(self.rapidity_results) - 1):
            if ((abs(self.rapidity_results[i - 1]) > self.tho_lim) and \
                (abs(self.rapidity_results[i]) < self.tho_lim)) or \
                ((abs(self.rapidity_results[i - 1]) < self.tho_lim) and \
                (abs(self.rapidity_results[i]) > self.tho_lim)):
                self.tho = self.t_rap[i]
    
    def calculate_stab_amp(self):
        """
        Calculate stab_amp
        """
        index = round(len(self.stability_results) / 2)
        second_half = self.stability_results[-index:]
        self.stab_amp = np.max(second_half) - np.min(second_half)

    
# 4/ Functions

def double_cylindric_magnet(
    radius=0.00075,
    length=0.01,
    center_distance=0.0015,
    density=7500
):
    """
    Function to get the masse, volume and inertial moment of a double
    cylindre magnet, like for GEONAUTE R900 compass. International system units
    """
    V = 2 * math.pow(radius, 2) * math.pi * length
    m = V * density
    mom_z = m * (math.pow(radius, 2) / 4 + math.pow(length, 2) / 12 + \
        math.pow(center_distance, 2))
    return {"V": V, "m": m, "mom_z": mom_z}

def parallelepiped_magnet(
    length=0.01,
    width=0.006,
    thickness=0.001,
    density=7500
):
    """
    Function to get the masse, volume and inertial moment of a parallelepiped
    magnet. International system units.
    The hole for the axis is ignored.
    """
    V = length * width * thickness
    m = V * density
    mom_z = m * (math.pow(length, 2) + math.pow(width, 2)) / 12
    return {"V": V, "m": m, "mom_z": mom_z}

def compasses_from_excel(file_name):
    """
    Return a list of dictionnary containing the attributes of the compasses
    stored in the excel file.
    """
    doc = xlrd.open_workbook(file_name)
    sheet_1 = doc.sheet_by_index(0)
    cols = sheet_1.ncols
    rows = sheet_1.nrows
    compasses = []
    for c in range(3, cols):
        comp = {}
        for r in range(0, rows):
            comp[sheet_1.cell_value(rowx=r, colx=0)] = \
                sheet_1.cell_value(rowx=r, colx=c)
        compasses.append(comp)
    return compasses

def locations_from_excel(file_name):
    """
    Return a list of dictionnary containing the attributes of the locations
    stored in the excel file.
    """
    doc = xlrd.open_workbook(file_name)
    sheet_1 = doc.sheet_by_index(0)
    cols = sheet_1.ncols
    rows = sheet_1.nrows
    locations = []
    for c in range(1, cols):
        loc = {}
        for r in range(0, rows):
            loc[sheet_1.cell_value(rowx=r, colx=0)] = \
                sheet_1.cell_value(rowx=r, colx=c)
        locations.append(loc)
    return locations

def balance_map(comp, theta_lim, alpha_lim):
    """
    Draw the zone on the planisphere where the compass is acceptable, according
    to theta_lim and alpha_lim
    """
    lower_lim = []
    opti = []
    upper_lim = []
    longitudes = np.arange(-180, 0, 10)

    for lon in longitudes:
        i = True
        j = True
        k = True
        a_ant_abs = 4
        for lat in np.arange(-90, 91):
            mg = MagneticField({"name" : "map", "lon" : lon, "lat" : lat})
            b = Balance(comp, mg, theta_lim, alpha_lim)
            a_abs = abs(copy.deepcopy(b.alpha_err))
            if (i == True) and (a_ant_abs > alpha_lim) and (a_abs < alpha_lim):
                lower_lim.append(lat)
                i = False
            if (j == True) and (a_ant_abs < alpha_lim) and (a_abs > alpha_lim):
                upper_lim.append(lat)
                j = False
            if (k == True) and (a_abs > a_ant_abs):
                opti.append(lat)
                k = False
            if (i == False) and (j == False) and (k == False):
                continue
            a_ant_abs = copy.deepcopy(a_abs)
    
    world_map = mpimg.imread('images/Equirectangular_projection_SW.png')
    plt.imshow(
        world_map,
        interpolation='none',
        extent=[-180, 180, -90, 90],
        clip_on=True
    )
    plt.plot(longitudes, lower_lim, 'g-', label = "Lower limit")
    plt.plot(longitudes, upper_lim, 'r-', label = "Upper limit")
    plt.plot(longitudes, opti, 'b-', label = "Optimal balance")
    plt.title(('Acceptability zone for θ limit = ' + \
        str(math.degrees(theta_lim)) + '° and α limit = ' + \
        str(math.degrees(alpha_lim)) + '°'))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()

def iso_x_map(comp):
    """
    Draw the iso curves of x, every 0,1 mm
    """
    x_iso = np.arange(0.0008, -0.0009, -0.0001)

    # Liste of isocurves for x between -0,0008 and 0,0008
    c = [[] for i in range(17)]
    longitudes = np.arange(-180, 185, 10)

    for lon in longitudes:
        i = 0
        x_ant = 0.001
        for lat in np.arange(-90, 91):
            mg = MagneticField({"name" : "map", "lon" : lon, "lat" : lat})
            b = Balance(comp, mg)
            x = copy.deepcopy(b.x_opti)
            if i == 17:
                break
            if (x_iso[i] < x_ant) and (x_iso[i] > x):
                c[i].append(lat)
                i = i + 1
            x_ant = copy.deepcopy(x)
    
    j = 0
    for iso in c:
        world_map = mpimg.imread('images/Equirectangular_projection_SW.png')
        plt.imshow(
            world_map,
            interpolation='none',
            extent=[-180, 180, -90, 90],
            clip_on=True
        )
        plt.plot(longitudes, iso, 'r-', label = ("x = " + str(x_iso[j]) + "m"))
        j = j + 1
    plt.show()