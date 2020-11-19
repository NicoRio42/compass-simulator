import core as cs

comp = cs.Compass()
mag_fld = cs.MagneticField()
dyn = cs.Dynamic(comp, mag_fld)
#dyn.rapidity()
#dyn.display_rap()
#dyn.stability()
#dyn.display_stab()
#print(cs.double_cylindric_magnet())
print(cs.parallelepiped_magnet())