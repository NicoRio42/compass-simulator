import core as cs

comp = cs.Compass()
mag_fld = cs.MagneticField()
dyn = cs.Dynamic(comp, mag_fld, exp_coef_visc=6e-3)
#dyn.rapidity()
#print(dyn.tho)
#dyn.display_rap()
dyn.stability()
print(dyn.stab_amp)
dyn.display_stab()
#print(cs.double_cylindric_magnet())
"""
print(cs.parallelepiped_magnet(
    length=0.008,
    width=0.006,
    thickness=0.0015,
    density=7500
))
"""