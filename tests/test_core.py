import compass_simulator.core as cs


class TestCompass:
    compass_default = cs.Compass()
    compass = cs.Compass(
        name="R500 no disk",
        needle_length=0.032,
        needle_width=0.008,
        needle_thickness=0.00025,
        needle_disk_density=1200,
        disk_radius=0,
        disk_thickness=0,
        mag_rem=1.3,
        V=0.00001,
        m=0.0001,
        magnet_mom_z=0,
        x=-0.5,
        rho=700,
        viscosity=0,
        z_h=0.008,
        z_b=0.008,
    )


def test_double_cylindric_magnet_default():
    """
    Testing the result of double_cylindric_magnet() with default values.
    """
    assert cs.double_cylindric_magnet() == {
        "V": 3.534291735288517e-08,
        "m": 0.0002650718801466388,
        "mom_z": 2.842619798030882e-09,
    }


def test_double_cylindric_magnet():
    """
    Testing the result of double_cylindric_magnet().
    """
    assert cs.double_cylindric_magnet(
        radius=0.0005, length=0.008, center_distance=0.0015, density=7500
    ) == {
        "V": 1.2566370614359173e-08,
        "m": 9.42477796076938e-05,
        "mom_z": 7.206028149171587e-10,
    }


def test_parallelepiped_magnet_default():
    """
    Testing the result of parallelepiped_magnet() with default values.
    """
    assert cs.parallelepiped_magnet() == {
        "V": 6.000000000000001e-08,
        "m": 0.00045000000000000004,
        "mom_z": 5.1e-09,
    }


def test_parallelepiped_magnet():
    """
    Testing the result of parallelepiped_magnet().
    """
    assert cs.parallelepiped_magnet(
        length=0.008, width=0.006, thickness=0.0015, density=7500
    ) == {
        "V": 7.200000000000001e-08,
        "m": 0.0005400000000000001,
        "mom_z": 4.500000000000001e-09,
    }
