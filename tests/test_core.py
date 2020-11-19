import compass_simulator.core as cs

def test_double_cylindric_magnet():
    """
    Testing the result of double_cylindric_magnet() with default values.
    """
    assert cs.double_cylindric_magnet() == {'V': 3.534291735288517e-08,
        'm': 0.0002650718801466388, 
        'mom_z': 2.842619798030882e-09
    }

def test_parallelepiped_magnet():
    """
    Testing the result of parallelepiped_magnet() with default values.
    """
    assert cs.parallelepiped_magnet() == {'V': 6.000000000000001e-08,
        'm': 0.00045000000000000004, 
        'mom_z': 5.1e-09
    }