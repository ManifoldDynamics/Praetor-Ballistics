import numpy as np
from ballistics.explosives import Explosive
from ballistics.lethality import FragmentationModel

def test_explosives():
    tnt = Explosive("TNT")
    comp_b = Explosive("Composition B")

    assert tnt.gurney_constant == 2440.0
    # Comp B is more powerful than TNT
    assert comp_b.gurney_constant > tnt.gurney_constant

def test_gurney_velocity():
    tnt = Explosive("TNT")

    # Example: 1kg TNT, 5kg metal casing (C/M = 0.2)
    # Cylinder geometry
    v_cyl = FragmentationModel.gurney_velocity(1.0, 5.0, tnt.gurney_constant, geometry="cylinder")

    # Sphere geometry
    v_sph = FragmentationModel.gurney_velocity(1.0, 5.0, tnt.gurney_constant, geometry="sphere")

    # Flat plate
    v_plat = FragmentationModel.gurney_velocity(1.0, 5.0, tnt.gurney_constant, geometry="flat_plate")

    assert v_cyl > 0.0
    # For a given C/M, flat plates direct more energy to the plate than spheres do to a spherical shell
    assert v_plat > v_cyl > v_sph

def test_spray_vectors():
    num_frags = 100
    blast_vel = 1000.0

    # Sphere spray
    vecs_sph = FragmentationModel.spray_vectors(num_frags, blast_vel, geometry="sphere")
    assert vecs_sph.shape == (100, 3)

    # All vectors should have exactly magnitude `blast_vel`
    speeds = np.linalg.norm(vecs_sph, axis=1)
    assert np.allclose(speeds, blast_vel)

def test_fragment_generation():
    # 10kg metal mass, 100 fragments = 0.1kg each
    props = FragmentationModel.generate_fragments(10.0, 100)

    assert props["count"] == 100
    assert np.isclose(props["mass_kg"], 0.1)
    assert props["diameter_m"] > 0.0
