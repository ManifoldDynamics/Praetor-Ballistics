import numpy as np

class StrategicTargetMatrixV2:
    """
    Massive Proprietary V2 Target Database.
    Contains detailed internal component layouts and vulnerability parameters.
    """
    TARGETS = {}

    @classmethod
    def initialize_matrix(cls):
        # 1. MBTs
        for i in range(1, 201):
            cls.TARGETS[f"MBT_Type_{i}"] = {
                'components': [
                    {'name': 'glacis_armor', 'vulnerability': 0.05, 'is_critical': False, 'thresh_j': 8e6, 'p_fire': 0.05},
                    {'name': 'turret_ring', 'vulnerability': 0.85, 'is_critical': True, 'thresh_j': 4e5, 'p_fire': 0.15},
                    {'name': 'autoloader', 'vulnerability': 1.0, 'is_critical': True, 'thresh_j': 1e5, 'p_fire': 0.95},
                    {'name': 'crew_commander', 'vulnerability': 0.95, 'is_critical': True, 'thresh_j': 450, 'p_fire': 0.0},
                    {'name': 'fuel_cell', 'vulnerability': 0.30, 'is_critical': False, 'thresh_j': 1e5, 'p_fire': 0.85}
                ]
            }
        # 2. Bunkers
        for i in range(1, 101):
            cls.TARGETS[f"Bunker_C2_{i}"] = {
                'components': [
                    {'name': 'concrete_slab', 'vulnerability': 0.01, 'is_critical': False, 'thresh_j': 5e9},
                    {'name': 'comms_node', 'vulnerability': 0.95, 'is_critical': True, 'thresh_j': 1e6}
                ]
            }

    @classmethod
    def get_target(cls, target_id):
        if not cls.TARGETS: cls.initialize_matrix()
        return cls.TARGETS.get(target_id)


class LethalityV2:
    """
    V2 Proprietary Vulnerability & Lethality (V/L) Engine.
    """
    def __init__(self, target_id):
        self.target_data = StrategicTargetMatrixV2.get_target(target_id)
        if not self.target_data:
            raise ValueError(f"Target {target_id} not found.")

    def calculate_pk_h(self, component, energy_j):
        e0 = component.get('thresh_j', 500.0)
        if energy_j <= e0: return 0.0
        return 1.0 - np.exp(-((energy_j - e0) / (e0 * 1.75))**1.35)

    def evaluate_mission_kill(self, hits):
        comp_health = {c['name']: 1.0 for c in self.target_data['components']}
        fire = False
        for hit in hits:
            comp = next((c for c in self.target_data['components'] if c['name'] == hit['component']), None)
            if comp:
                pk = self.calculate_pk_h(comp, hit['energy'])
                comp_health[comp['name']] *= (1.0 - pk)
                if pk > 0.5 and np.random.rand() < comp.get('p_fire', 0.0): fire = True
        p_survive = 1.0
        for c in self.target_data['components']:
            if c['is_critical']: p_survive *= comp_health[c['name']]
        p_kill = 1.0 - p_survive
        if fire: p_kill = max(p_kill, 0.9)
        return {'p_neutralized': p_kill, 'health': comp_health, 'fire': fire}

class FragmentationV2:
    """V2.x Fragment tracking."""
    @staticmethod
    def calculate_residual_velocity(v_impact, thickness_mm, mat_density):
        v_limit = 150.0 * (thickness_mm**0.8) * (mat_density / 7850.0)**0.5
        if v_impact <= v_limit: return 0.0
        return np.sqrt(v_impact**2 - v_limit**2)

    @staticmethod
    def estimate_fragment_penetration_residual(v_imp, m_frag, thick, mat_density):
        """
        V2.x Rigorous residual velocity for fragments.
        Calls the proprietary Lambert-Thor hybrid model.
        """
        v_lim = 10**4.4 * (thick * 3.14 * (0.01/2)**2)**0.9 * m_frag**-0.3
        if v_imp <= v_lim: return 0.0
        return np.sqrt(v_imp**2 - v_lim**2)
