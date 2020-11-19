import compass_simulator as cs

comp = cs.Compass()
mag_fld = cs.MagneticField()
dyn = cs.Dynamic(comp, mag_fld)
#dyn.rapidity()
#dyn.display_rap()
dyn.stability()
dyn.display_stab()