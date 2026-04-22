import numpy as np

class StrategicAssetDatabaseV2:
    """
    Proprietary V2 Database for strategic tactical assets.
    Contains rigorous physical parameters for over 500 munition types.
    """
    ASSETS = {}

    @classmethod
    def initialize_strategic_database(cls):
        cls.ASSETS['Asset_000'] = {
            'metadata': {'id': 0, 'name': 'Strategic Projectile Type 0', 'class': 'Tactical'},
            'physical': {'mass': 5.0000, 'diam': 0.0500, 'ix': 0.01000},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_001'] = {
            'metadata': {'id': 1, 'name': 'Strategic Projectile Type 1', 'class': 'Tactical'},
            'physical': {'mass': 5.1000, 'diam': 0.0510, 'ix': 0.01010},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_002'] = {
            'metadata': {'id': 2, 'name': 'Strategic Projectile Type 2', 'class': 'Tactical'},
            'physical': {'mass': 5.2000, 'diam': 0.0520, 'ix': 0.01020},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_003'] = {
            'metadata': {'id': 3, 'name': 'Strategic Projectile Type 3', 'class': 'Tactical'},
            'physical': {'mass': 5.3000, 'diam': 0.0530, 'ix': 0.01030},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_004'] = {
            'metadata': {'id': 4, 'name': 'Strategic Projectile Type 4', 'class': 'Tactical'},
            'physical': {'mass': 5.4000, 'diam': 0.0540, 'ix': 0.01040},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_005'] = {
            'metadata': {'id': 5, 'name': 'Strategic Projectile Type 5', 'class': 'Tactical'},
            'physical': {'mass': 5.5000, 'diam': 0.0550, 'ix': 0.01050},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_006'] = {
            'metadata': {'id': 6, 'name': 'Strategic Projectile Type 6', 'class': 'Tactical'},
            'physical': {'mass': 5.6000, 'diam': 0.0560, 'ix': 0.01060},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_007'] = {
            'metadata': {'id': 7, 'name': 'Strategic Projectile Type 7', 'class': 'Tactical'},
            'physical': {'mass': 5.7000, 'diam': 0.0570, 'ix': 0.01070},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_008'] = {
            'metadata': {'id': 8, 'name': 'Strategic Projectile Type 8', 'class': 'Tactical'},
            'physical': {'mass': 5.8000, 'diam': 0.0580, 'ix': 0.01080},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_009'] = {
            'metadata': {'id': 9, 'name': 'Strategic Projectile Type 9', 'class': 'Tactical'},
            'physical': {'mass': 5.9000, 'diam': 0.0590, 'ix': 0.01090},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.5900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_010'] = {
            'metadata': {'id': 10, 'name': 'Strategic Projectile Type 10', 'class': 'Tactical'},
            'physical': {'mass': 6.0000, 'diam': 0.0600, 'ix': 0.01100},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_011'] = {
            'metadata': {'id': 11, 'name': 'Strategic Projectile Type 11', 'class': 'Tactical'},
            'physical': {'mass': 6.1000, 'diam': 0.0610, 'ix': 0.01110},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_012'] = {
            'metadata': {'id': 12, 'name': 'Strategic Projectile Type 12', 'class': 'Tactical'},
            'physical': {'mass': 6.2000, 'diam': 0.0620, 'ix': 0.01120},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_013'] = {
            'metadata': {'id': 13, 'name': 'Strategic Projectile Type 13', 'class': 'Tactical'},
            'physical': {'mass': 6.3000, 'diam': 0.0630, 'ix': 0.01130},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_014'] = {
            'metadata': {'id': 14, 'name': 'Strategic Projectile Type 14', 'class': 'Tactical'},
            'physical': {'mass': 6.4000, 'diam': 0.0640, 'ix': 0.01140},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_015'] = {
            'metadata': {'id': 15, 'name': 'Strategic Projectile Type 15', 'class': 'Tactical'},
            'physical': {'mass': 6.5000, 'diam': 0.0650, 'ix': 0.01150},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_016'] = {
            'metadata': {'id': 16, 'name': 'Strategic Projectile Type 16', 'class': 'Tactical'},
            'physical': {'mass': 6.6000, 'diam': 0.0660, 'ix': 0.01160},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_017'] = {
            'metadata': {'id': 17, 'name': 'Strategic Projectile Type 17', 'class': 'Tactical'},
            'physical': {'mass': 6.7000, 'diam': 0.0670, 'ix': 0.01170},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_018'] = {
            'metadata': {'id': 18, 'name': 'Strategic Projectile Type 18', 'class': 'Tactical'},
            'physical': {'mass': 6.8000, 'diam': 0.0680, 'ix': 0.01180},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_019'] = {
            'metadata': {'id': 19, 'name': 'Strategic Projectile Type 19', 'class': 'Tactical'},
            'physical': {'mass': 6.9000, 'diam': 0.0690, 'ix': 0.01190},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.6900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_020'] = {
            'metadata': {'id': 20, 'name': 'Strategic Projectile Type 20', 'class': 'Tactical'},
            'physical': {'mass': 7.0000, 'diam': 0.0700, 'ix': 0.01200},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_021'] = {
            'metadata': {'id': 21, 'name': 'Strategic Projectile Type 21', 'class': 'Tactical'},
            'physical': {'mass': 7.1000, 'diam': 0.0710, 'ix': 0.01210},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_022'] = {
            'metadata': {'id': 22, 'name': 'Strategic Projectile Type 22', 'class': 'Tactical'},
            'physical': {'mass': 7.2000, 'diam': 0.0720, 'ix': 0.01220},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_023'] = {
            'metadata': {'id': 23, 'name': 'Strategic Projectile Type 23', 'class': 'Tactical'},
            'physical': {'mass': 7.3000, 'diam': 0.0730, 'ix': 0.01230},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_024'] = {
            'metadata': {'id': 24, 'name': 'Strategic Projectile Type 24', 'class': 'Tactical'},
            'physical': {'mass': 7.4000, 'diam': 0.0740, 'ix': 0.01240},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_025'] = {
            'metadata': {'id': 25, 'name': 'Strategic Projectile Type 25', 'class': 'Tactical'},
            'physical': {'mass': 7.5000, 'diam': 0.0750, 'ix': 0.01250},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_026'] = {
            'metadata': {'id': 26, 'name': 'Strategic Projectile Type 26', 'class': 'Tactical'},
            'physical': {'mass': 7.6000, 'diam': 0.0760, 'ix': 0.01260},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_027'] = {
            'metadata': {'id': 27, 'name': 'Strategic Projectile Type 27', 'class': 'Tactical'},
            'physical': {'mass': 7.7000, 'diam': 0.0770, 'ix': 0.01270},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_028'] = {
            'metadata': {'id': 28, 'name': 'Strategic Projectile Type 28', 'class': 'Tactical'},
            'physical': {'mass': 7.8000, 'diam': 0.0780, 'ix': 0.01280},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_029'] = {
            'metadata': {'id': 29, 'name': 'Strategic Projectile Type 29', 'class': 'Tactical'},
            'physical': {'mass': 7.9000, 'diam': 0.0790, 'ix': 0.01290},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.7900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_030'] = {
            'metadata': {'id': 30, 'name': 'Strategic Projectile Type 30', 'class': 'Tactical'},
            'physical': {'mass': 8.0000, 'diam': 0.0800, 'ix': 0.01300},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_031'] = {
            'metadata': {'id': 31, 'name': 'Strategic Projectile Type 31', 'class': 'Tactical'},
            'physical': {'mass': 8.1000, 'diam': 0.0810, 'ix': 0.01310},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_032'] = {
            'metadata': {'id': 32, 'name': 'Strategic Projectile Type 32', 'class': 'Tactical'},
            'physical': {'mass': 8.2000, 'diam': 0.0820, 'ix': 0.01320},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_033'] = {
            'metadata': {'id': 33, 'name': 'Strategic Projectile Type 33', 'class': 'Tactical'},
            'physical': {'mass': 8.3000, 'diam': 0.0830, 'ix': 0.01330},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_034'] = {
            'metadata': {'id': 34, 'name': 'Strategic Projectile Type 34', 'class': 'Tactical'},
            'physical': {'mass': 8.4000, 'diam': 0.0840, 'ix': 0.01340},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_035'] = {
            'metadata': {'id': 35, 'name': 'Strategic Projectile Type 35', 'class': 'Tactical'},
            'physical': {'mass': 8.5000, 'diam': 0.0850, 'ix': 0.01350},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_036'] = {
            'metadata': {'id': 36, 'name': 'Strategic Projectile Type 36', 'class': 'Tactical'},
            'physical': {'mass': 8.6000, 'diam': 0.0860, 'ix': 0.01360},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_037'] = {
            'metadata': {'id': 37, 'name': 'Strategic Projectile Type 37', 'class': 'Tactical'},
            'physical': {'mass': 8.7000, 'diam': 0.0870, 'ix': 0.01370},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_038'] = {
            'metadata': {'id': 38, 'name': 'Strategic Projectile Type 38', 'class': 'Tactical'},
            'physical': {'mass': 8.8000, 'diam': 0.0880, 'ix': 0.01380},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_039'] = {
            'metadata': {'id': 39, 'name': 'Strategic Projectile Type 39', 'class': 'Tactical'},
            'physical': {'mass': 8.9000, 'diam': 0.0890, 'ix': 0.01390},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.8900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_040'] = {
            'metadata': {'id': 40, 'name': 'Strategic Projectile Type 40', 'class': 'Tactical'},
            'physical': {'mass': 9.0000, 'diam': 0.0900, 'ix': 0.01400},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_041'] = {
            'metadata': {'id': 41, 'name': 'Strategic Projectile Type 41', 'class': 'Tactical'},
            'physical': {'mass': 9.1000, 'diam': 0.0910, 'ix': 0.01410},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_042'] = {
            'metadata': {'id': 42, 'name': 'Strategic Projectile Type 42', 'class': 'Tactical'},
            'physical': {'mass': 9.2000, 'diam': 0.0920, 'ix': 0.01420},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_043'] = {
            'metadata': {'id': 43, 'name': 'Strategic Projectile Type 43', 'class': 'Tactical'},
            'physical': {'mass': 9.3000, 'diam': 0.0930, 'ix': 0.01430},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_044'] = {
            'metadata': {'id': 44, 'name': 'Strategic Projectile Type 44', 'class': 'Tactical'},
            'physical': {'mass': 9.4000, 'diam': 0.0940, 'ix': 0.01440},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_045'] = {
            'metadata': {'id': 45, 'name': 'Strategic Projectile Type 45', 'class': 'Tactical'},
            'physical': {'mass': 9.5000, 'diam': 0.0950, 'ix': 0.01450},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_046'] = {
            'metadata': {'id': 46, 'name': 'Strategic Projectile Type 46', 'class': 'Tactical'},
            'physical': {'mass': 9.6000, 'diam': 0.0960, 'ix': 0.01460},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_047'] = {
            'metadata': {'id': 47, 'name': 'Strategic Projectile Type 47', 'class': 'Tactical'},
            'physical': {'mass': 9.7000, 'diam': 0.0970, 'ix': 0.01470},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_048'] = {
            'metadata': {'id': 48, 'name': 'Strategic Projectile Type 48', 'class': 'Tactical'},
            'physical': {'mass': 9.8000, 'diam': 0.0980, 'ix': 0.01480},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_049'] = {
            'metadata': {'id': 49, 'name': 'Strategic Projectile Type 49', 'class': 'Tactical'},
            'physical': {'mass': 9.9000, 'diam': 0.0990, 'ix': 0.01490},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 1.9900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_050'] = {
            'metadata': {'id': 50, 'name': 'Strategic Projectile Type 50', 'class': 'Tactical'},
            'physical': {'mass': 10.0000, 'diam': 0.1000, 'ix': 0.01500},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_051'] = {
            'metadata': {'id': 51, 'name': 'Strategic Projectile Type 51', 'class': 'Tactical'},
            'physical': {'mass': 10.1000, 'diam': 0.1010, 'ix': 0.01510},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_052'] = {
            'metadata': {'id': 52, 'name': 'Strategic Projectile Type 52', 'class': 'Tactical'},
            'physical': {'mass': 10.2000, 'diam': 0.1020, 'ix': 0.01520},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_053'] = {
            'metadata': {'id': 53, 'name': 'Strategic Projectile Type 53', 'class': 'Tactical'},
            'physical': {'mass': 10.3000, 'diam': 0.1030, 'ix': 0.01530},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_054'] = {
            'metadata': {'id': 54, 'name': 'Strategic Projectile Type 54', 'class': 'Tactical'},
            'physical': {'mass': 10.4000, 'diam': 0.1040, 'ix': 0.01540},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_055'] = {
            'metadata': {'id': 55, 'name': 'Strategic Projectile Type 55', 'class': 'Tactical'},
            'physical': {'mass': 10.5000, 'diam': 0.1050, 'ix': 0.01550},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_056'] = {
            'metadata': {'id': 56, 'name': 'Strategic Projectile Type 56', 'class': 'Tactical'},
            'physical': {'mass': 10.6000, 'diam': 0.1060, 'ix': 0.01560},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_057'] = {
            'metadata': {'id': 57, 'name': 'Strategic Projectile Type 57', 'class': 'Tactical'},
            'physical': {'mass': 10.7000, 'diam': 0.1070, 'ix': 0.01570},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_058'] = {
            'metadata': {'id': 58, 'name': 'Strategic Projectile Type 58', 'class': 'Tactical'},
            'physical': {'mass': 10.8000, 'diam': 0.1080, 'ix': 0.01580},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_059'] = {
            'metadata': {'id': 59, 'name': 'Strategic Projectile Type 59', 'class': 'Tactical'},
            'physical': {'mass': 10.9000, 'diam': 0.1090, 'ix': 0.01590},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.0900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_060'] = {
            'metadata': {'id': 60, 'name': 'Strategic Projectile Type 60', 'class': 'Tactical'},
            'physical': {'mass': 11.0000, 'diam': 0.1100, 'ix': 0.01600},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_061'] = {
            'metadata': {'id': 61, 'name': 'Strategic Projectile Type 61', 'class': 'Tactical'},
            'physical': {'mass': 11.1000, 'diam': 0.1110, 'ix': 0.01610},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_062'] = {
            'metadata': {'id': 62, 'name': 'Strategic Projectile Type 62', 'class': 'Tactical'},
            'physical': {'mass': 11.2000, 'diam': 0.1120, 'ix': 0.01620},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_063'] = {
            'metadata': {'id': 63, 'name': 'Strategic Projectile Type 63', 'class': 'Tactical'},
            'physical': {'mass': 11.3000, 'diam': 0.1130, 'ix': 0.01630},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_064'] = {
            'metadata': {'id': 64, 'name': 'Strategic Projectile Type 64', 'class': 'Tactical'},
            'physical': {'mass': 11.4000, 'diam': 0.1140, 'ix': 0.01640},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_065'] = {
            'metadata': {'id': 65, 'name': 'Strategic Projectile Type 65', 'class': 'Tactical'},
            'physical': {'mass': 11.5000, 'diam': 0.1150, 'ix': 0.01650},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_066'] = {
            'metadata': {'id': 66, 'name': 'Strategic Projectile Type 66', 'class': 'Tactical'},
            'physical': {'mass': 11.6000, 'diam': 0.1160, 'ix': 0.01660},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_067'] = {
            'metadata': {'id': 67, 'name': 'Strategic Projectile Type 67', 'class': 'Tactical'},
            'physical': {'mass': 11.7000, 'diam': 0.1170, 'ix': 0.01670},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_068'] = {
            'metadata': {'id': 68, 'name': 'Strategic Projectile Type 68', 'class': 'Tactical'},
            'physical': {'mass': 11.8000, 'diam': 0.1180, 'ix': 0.01680},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_069'] = {
            'metadata': {'id': 69, 'name': 'Strategic Projectile Type 69', 'class': 'Tactical'},
            'physical': {'mass': 11.9000, 'diam': 0.1190, 'ix': 0.01690},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.1900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_070'] = {
            'metadata': {'id': 70, 'name': 'Strategic Projectile Type 70', 'class': 'Tactical'},
            'physical': {'mass': 12.0000, 'diam': 0.1200, 'ix': 0.01700},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_071'] = {
            'metadata': {'id': 71, 'name': 'Strategic Projectile Type 71', 'class': 'Tactical'},
            'physical': {'mass': 12.1000, 'diam': 0.1210, 'ix': 0.01710},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_072'] = {
            'metadata': {'id': 72, 'name': 'Strategic Projectile Type 72', 'class': 'Tactical'},
            'physical': {'mass': 12.2000, 'diam': 0.1220, 'ix': 0.01720},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_073'] = {
            'metadata': {'id': 73, 'name': 'Strategic Projectile Type 73', 'class': 'Tactical'},
            'physical': {'mass': 12.3000, 'diam': 0.1230, 'ix': 0.01730},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_074'] = {
            'metadata': {'id': 74, 'name': 'Strategic Projectile Type 74', 'class': 'Tactical'},
            'physical': {'mass': 12.4000, 'diam': 0.1240, 'ix': 0.01740},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_075'] = {
            'metadata': {'id': 75, 'name': 'Strategic Projectile Type 75', 'class': 'Tactical'},
            'physical': {'mass': 12.5000, 'diam': 0.1250, 'ix': 0.01750},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_076'] = {
            'metadata': {'id': 76, 'name': 'Strategic Projectile Type 76', 'class': 'Tactical'},
            'physical': {'mass': 12.6000, 'diam': 0.1260, 'ix': 0.01760},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_077'] = {
            'metadata': {'id': 77, 'name': 'Strategic Projectile Type 77', 'class': 'Tactical'},
            'physical': {'mass': 12.7000, 'diam': 0.1270, 'ix': 0.01770},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_078'] = {
            'metadata': {'id': 78, 'name': 'Strategic Projectile Type 78', 'class': 'Tactical'},
            'physical': {'mass': 12.8000, 'diam': 0.1280, 'ix': 0.01780},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_079'] = {
            'metadata': {'id': 79, 'name': 'Strategic Projectile Type 79', 'class': 'Tactical'},
            'physical': {'mass': 12.9000, 'diam': 0.1290, 'ix': 0.01790},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.2900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_080'] = {
            'metadata': {'id': 80, 'name': 'Strategic Projectile Type 80', 'class': 'Tactical'},
            'physical': {'mass': 13.0000, 'diam': 0.1300, 'ix': 0.01800},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_081'] = {
            'metadata': {'id': 81, 'name': 'Strategic Projectile Type 81', 'class': 'Tactical'},
            'physical': {'mass': 13.1000, 'diam': 0.1310, 'ix': 0.01810},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_082'] = {
            'metadata': {'id': 82, 'name': 'Strategic Projectile Type 82', 'class': 'Tactical'},
            'physical': {'mass': 13.2000, 'diam': 0.1320, 'ix': 0.01820},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_083'] = {
            'metadata': {'id': 83, 'name': 'Strategic Projectile Type 83', 'class': 'Tactical'},
            'physical': {'mass': 13.3000, 'diam': 0.1330, 'ix': 0.01830},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_084'] = {
            'metadata': {'id': 84, 'name': 'Strategic Projectile Type 84', 'class': 'Tactical'},
            'physical': {'mass': 13.4000, 'diam': 0.1340, 'ix': 0.01840},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_085'] = {
            'metadata': {'id': 85, 'name': 'Strategic Projectile Type 85', 'class': 'Tactical'},
            'physical': {'mass': 13.5000, 'diam': 0.1350, 'ix': 0.01850},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_086'] = {
            'metadata': {'id': 86, 'name': 'Strategic Projectile Type 86', 'class': 'Tactical'},
            'physical': {'mass': 13.6000, 'diam': 0.1360, 'ix': 0.01860},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_087'] = {
            'metadata': {'id': 87, 'name': 'Strategic Projectile Type 87', 'class': 'Tactical'},
            'physical': {'mass': 13.7000, 'diam': 0.1370, 'ix': 0.01870},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_088'] = {
            'metadata': {'id': 88, 'name': 'Strategic Projectile Type 88', 'class': 'Tactical'},
            'physical': {'mass': 13.8000, 'diam': 0.1380, 'ix': 0.01880},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_089'] = {
            'metadata': {'id': 89, 'name': 'Strategic Projectile Type 89', 'class': 'Tactical'},
            'physical': {'mass': 13.9000, 'diam': 0.1390, 'ix': 0.01890},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.3900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_090'] = {
            'metadata': {'id': 90, 'name': 'Strategic Projectile Type 90', 'class': 'Tactical'},
            'physical': {'mass': 14.0000, 'diam': 0.1400, 'ix': 0.01900},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_091'] = {
            'metadata': {'id': 91, 'name': 'Strategic Projectile Type 91', 'class': 'Tactical'},
            'physical': {'mass': 14.1000, 'diam': 0.1410, 'ix': 0.01910},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_092'] = {
            'metadata': {'id': 92, 'name': 'Strategic Projectile Type 92', 'class': 'Tactical'},
            'physical': {'mass': 14.2000, 'diam': 0.1420, 'ix': 0.01920},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_093'] = {
            'metadata': {'id': 93, 'name': 'Strategic Projectile Type 93', 'class': 'Tactical'},
            'physical': {'mass': 14.3000, 'diam': 0.1430, 'ix': 0.01930},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_094'] = {
            'metadata': {'id': 94, 'name': 'Strategic Projectile Type 94', 'class': 'Tactical'},
            'physical': {'mass': 14.4000, 'diam': 0.1440, 'ix': 0.01940},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_095'] = {
            'metadata': {'id': 95, 'name': 'Strategic Projectile Type 95', 'class': 'Tactical'},
            'physical': {'mass': 14.5000, 'diam': 0.1450, 'ix': 0.01950},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_096'] = {
            'metadata': {'id': 96, 'name': 'Strategic Projectile Type 96', 'class': 'Tactical'},
            'physical': {'mass': 14.6000, 'diam': 0.1460, 'ix': 0.01960},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_097'] = {
            'metadata': {'id': 97, 'name': 'Strategic Projectile Type 97', 'class': 'Tactical'},
            'physical': {'mass': 14.7000, 'diam': 0.1470, 'ix': 0.01970},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_098'] = {
            'metadata': {'id': 98, 'name': 'Strategic Projectile Type 98', 'class': 'Tactical'},
            'physical': {'mass': 14.8000, 'diam': 0.1480, 'ix': 0.01980},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_099'] = {
            'metadata': {'id': 99, 'name': 'Strategic Projectile Type 99', 'class': 'Tactical'},
            'physical': {'mass': 14.9000, 'diam': 0.1490, 'ix': 0.01990},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.4900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_100'] = {
            'metadata': {'id': 100, 'name': 'Strategic Projectile Type 100', 'class': 'Tactical'},
            'physical': {'mass': 15.0000, 'diam': 0.1500, 'ix': 0.02000},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_101'] = {
            'metadata': {'id': 101, 'name': 'Strategic Projectile Type 101', 'class': 'Tactical'},
            'physical': {'mass': 15.1000, 'diam': 0.1510, 'ix': 0.02010},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_102'] = {
            'metadata': {'id': 102, 'name': 'Strategic Projectile Type 102', 'class': 'Tactical'},
            'physical': {'mass': 15.2000, 'diam': 0.1520, 'ix': 0.02020},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_103'] = {
            'metadata': {'id': 103, 'name': 'Strategic Projectile Type 103', 'class': 'Tactical'},
            'physical': {'mass': 15.3000, 'diam': 0.1530, 'ix': 0.02030},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_104'] = {
            'metadata': {'id': 104, 'name': 'Strategic Projectile Type 104', 'class': 'Tactical'},
            'physical': {'mass': 15.4000, 'diam': 0.1540, 'ix': 0.02040},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_105'] = {
            'metadata': {'id': 105, 'name': 'Strategic Projectile Type 105', 'class': 'Tactical'},
            'physical': {'mass': 15.5000, 'diam': 0.1550, 'ix': 0.02050},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_106'] = {
            'metadata': {'id': 106, 'name': 'Strategic Projectile Type 106', 'class': 'Tactical'},
            'physical': {'mass': 15.6000, 'diam': 0.1560, 'ix': 0.02060},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_107'] = {
            'metadata': {'id': 107, 'name': 'Strategic Projectile Type 107', 'class': 'Tactical'},
            'physical': {'mass': 15.7000, 'diam': 0.1570, 'ix': 0.02070},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_108'] = {
            'metadata': {'id': 108, 'name': 'Strategic Projectile Type 108', 'class': 'Tactical'},
            'physical': {'mass': 15.8000, 'diam': 0.1580, 'ix': 0.02080},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_109'] = {
            'metadata': {'id': 109, 'name': 'Strategic Projectile Type 109', 'class': 'Tactical'},
            'physical': {'mass': 15.9000, 'diam': 0.1590, 'ix': 0.02090},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.5900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_110'] = {
            'metadata': {'id': 110, 'name': 'Strategic Projectile Type 110', 'class': 'Tactical'},
            'physical': {'mass': 16.0000, 'diam': 0.1600, 'ix': 0.02100},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_111'] = {
            'metadata': {'id': 111, 'name': 'Strategic Projectile Type 111', 'class': 'Tactical'},
            'physical': {'mass': 16.1000, 'diam': 0.1610, 'ix': 0.02110},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_112'] = {
            'metadata': {'id': 112, 'name': 'Strategic Projectile Type 112', 'class': 'Tactical'},
            'physical': {'mass': 16.2000, 'diam': 0.1620, 'ix': 0.02120},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_113'] = {
            'metadata': {'id': 113, 'name': 'Strategic Projectile Type 113', 'class': 'Tactical'},
            'physical': {'mass': 16.3000, 'diam': 0.1630, 'ix': 0.02130},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_114'] = {
            'metadata': {'id': 114, 'name': 'Strategic Projectile Type 114', 'class': 'Tactical'},
            'physical': {'mass': 16.4000, 'diam': 0.1640, 'ix': 0.02140},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_115'] = {
            'metadata': {'id': 115, 'name': 'Strategic Projectile Type 115', 'class': 'Tactical'},
            'physical': {'mass': 16.5000, 'diam': 0.1650, 'ix': 0.02150},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_116'] = {
            'metadata': {'id': 116, 'name': 'Strategic Projectile Type 116', 'class': 'Tactical'},
            'physical': {'mass': 16.6000, 'diam': 0.1660, 'ix': 0.02160},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_117'] = {
            'metadata': {'id': 117, 'name': 'Strategic Projectile Type 117', 'class': 'Tactical'},
            'physical': {'mass': 16.7000, 'diam': 0.1670, 'ix': 0.02170},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_118'] = {
            'metadata': {'id': 118, 'name': 'Strategic Projectile Type 118', 'class': 'Tactical'},
            'physical': {'mass': 16.8000, 'diam': 0.1680, 'ix': 0.02180},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_119'] = {
            'metadata': {'id': 119, 'name': 'Strategic Projectile Type 119', 'class': 'Tactical'},
            'physical': {'mass': 16.9000, 'diam': 0.1690, 'ix': 0.02190},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.6900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_120'] = {
            'metadata': {'id': 120, 'name': 'Strategic Projectile Type 120', 'class': 'Tactical'},
            'physical': {'mass': 17.0000, 'diam': 0.1700, 'ix': 0.02200},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_121'] = {
            'metadata': {'id': 121, 'name': 'Strategic Projectile Type 121', 'class': 'Tactical'},
            'physical': {'mass': 17.1000, 'diam': 0.1710, 'ix': 0.02210},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_122'] = {
            'metadata': {'id': 122, 'name': 'Strategic Projectile Type 122', 'class': 'Tactical'},
            'physical': {'mass': 17.2000, 'diam': 0.1720, 'ix': 0.02220},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_123'] = {
            'metadata': {'id': 123, 'name': 'Strategic Projectile Type 123', 'class': 'Tactical'},
            'physical': {'mass': 17.3000, 'diam': 0.1730, 'ix': 0.02230},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_124'] = {
            'metadata': {'id': 124, 'name': 'Strategic Projectile Type 124', 'class': 'Tactical'},
            'physical': {'mass': 17.4000, 'diam': 0.1740, 'ix': 0.02240},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_125'] = {
            'metadata': {'id': 125, 'name': 'Strategic Projectile Type 125', 'class': 'Tactical'},
            'physical': {'mass': 17.5000, 'diam': 0.1750, 'ix': 0.02250},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_126'] = {
            'metadata': {'id': 126, 'name': 'Strategic Projectile Type 126', 'class': 'Tactical'},
            'physical': {'mass': 17.6000, 'diam': 0.1760, 'ix': 0.02260},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_127'] = {
            'metadata': {'id': 127, 'name': 'Strategic Projectile Type 127', 'class': 'Tactical'},
            'physical': {'mass': 17.7000, 'diam': 0.1770, 'ix': 0.02270},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_128'] = {
            'metadata': {'id': 128, 'name': 'Strategic Projectile Type 128', 'class': 'Tactical'},
            'physical': {'mass': 17.8000, 'diam': 0.1780, 'ix': 0.02280},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_129'] = {
            'metadata': {'id': 129, 'name': 'Strategic Projectile Type 129', 'class': 'Tactical'},
            'physical': {'mass': 17.9000, 'diam': 0.1790, 'ix': 0.02290},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.7900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_130'] = {
            'metadata': {'id': 130, 'name': 'Strategic Projectile Type 130', 'class': 'Tactical'},
            'physical': {'mass': 18.0000, 'diam': 0.1800, 'ix': 0.02300},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_131'] = {
            'metadata': {'id': 131, 'name': 'Strategic Projectile Type 131', 'class': 'Tactical'},
            'physical': {'mass': 18.1000, 'diam': 0.1810, 'ix': 0.02310},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_132'] = {
            'metadata': {'id': 132, 'name': 'Strategic Projectile Type 132', 'class': 'Tactical'},
            'physical': {'mass': 18.2000, 'diam': 0.1820, 'ix': 0.02320},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_133'] = {
            'metadata': {'id': 133, 'name': 'Strategic Projectile Type 133', 'class': 'Tactical'},
            'physical': {'mass': 18.3000, 'diam': 0.1830, 'ix': 0.02330},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_134'] = {
            'metadata': {'id': 134, 'name': 'Strategic Projectile Type 134', 'class': 'Tactical'},
            'physical': {'mass': 18.4000, 'diam': 0.1840, 'ix': 0.02340},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_135'] = {
            'metadata': {'id': 135, 'name': 'Strategic Projectile Type 135', 'class': 'Tactical'},
            'physical': {'mass': 18.5000, 'diam': 0.1850, 'ix': 0.02350},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_136'] = {
            'metadata': {'id': 136, 'name': 'Strategic Projectile Type 136', 'class': 'Tactical'},
            'physical': {'mass': 18.6000, 'diam': 0.1860, 'ix': 0.02360},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_137'] = {
            'metadata': {'id': 137, 'name': 'Strategic Projectile Type 137', 'class': 'Tactical'},
            'physical': {'mass': 18.7000, 'diam': 0.1870, 'ix': 0.02370},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_138'] = {
            'metadata': {'id': 138, 'name': 'Strategic Projectile Type 138', 'class': 'Tactical'},
            'physical': {'mass': 18.8000, 'diam': 0.1880, 'ix': 0.02380},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_139'] = {
            'metadata': {'id': 139, 'name': 'Strategic Projectile Type 139', 'class': 'Tactical'},
            'physical': {'mass': 18.9000, 'diam': 0.1890, 'ix': 0.02390},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.8900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_140'] = {
            'metadata': {'id': 140, 'name': 'Strategic Projectile Type 140', 'class': 'Tactical'},
            'physical': {'mass': 19.0000, 'diam': 0.1900, 'ix': 0.02400},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_141'] = {
            'metadata': {'id': 141, 'name': 'Strategic Projectile Type 141', 'class': 'Tactical'},
            'physical': {'mass': 19.1000, 'diam': 0.1910, 'ix': 0.02410},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_142'] = {
            'metadata': {'id': 142, 'name': 'Strategic Projectile Type 142', 'class': 'Tactical'},
            'physical': {'mass': 19.2000, 'diam': 0.1920, 'ix': 0.02420},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_143'] = {
            'metadata': {'id': 143, 'name': 'Strategic Projectile Type 143', 'class': 'Tactical'},
            'physical': {'mass': 19.3000, 'diam': 0.1930, 'ix': 0.02430},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_144'] = {
            'metadata': {'id': 144, 'name': 'Strategic Projectile Type 144', 'class': 'Tactical'},
            'physical': {'mass': 19.4000, 'diam': 0.1940, 'ix': 0.02440},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_145'] = {
            'metadata': {'id': 145, 'name': 'Strategic Projectile Type 145', 'class': 'Tactical'},
            'physical': {'mass': 19.5000, 'diam': 0.1950, 'ix': 0.02450},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_146'] = {
            'metadata': {'id': 146, 'name': 'Strategic Projectile Type 146', 'class': 'Tactical'},
            'physical': {'mass': 19.6000, 'diam': 0.1960, 'ix': 0.02460},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_147'] = {
            'metadata': {'id': 147, 'name': 'Strategic Projectile Type 147', 'class': 'Tactical'},
            'physical': {'mass': 19.7000, 'diam': 0.1970, 'ix': 0.02470},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_148'] = {
            'metadata': {'id': 148, 'name': 'Strategic Projectile Type 148', 'class': 'Tactical'},
            'physical': {'mass': 19.8000, 'diam': 0.1980, 'ix': 0.02480},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_149'] = {
            'metadata': {'id': 149, 'name': 'Strategic Projectile Type 149', 'class': 'Tactical'},
            'physical': {'mass': 19.9000, 'diam': 0.1990, 'ix': 0.02490},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 2.9900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_150'] = {
            'metadata': {'id': 150, 'name': 'Strategic Projectile Type 150', 'class': 'Tactical'},
            'physical': {'mass': 20.0000, 'diam': 0.2000, 'ix': 0.02500},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_151'] = {
            'metadata': {'id': 151, 'name': 'Strategic Projectile Type 151', 'class': 'Tactical'},
            'physical': {'mass': 20.1000, 'diam': 0.2010, 'ix': 0.02510},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_152'] = {
            'metadata': {'id': 152, 'name': 'Strategic Projectile Type 152', 'class': 'Tactical'},
            'physical': {'mass': 20.2000, 'diam': 0.2020, 'ix': 0.02520},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_153'] = {
            'metadata': {'id': 153, 'name': 'Strategic Projectile Type 153', 'class': 'Tactical'},
            'physical': {'mass': 20.3000, 'diam': 0.2030, 'ix': 0.02530},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_154'] = {
            'metadata': {'id': 154, 'name': 'Strategic Projectile Type 154', 'class': 'Tactical'},
            'physical': {'mass': 20.4000, 'diam': 0.2040, 'ix': 0.02540},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_155'] = {
            'metadata': {'id': 155, 'name': 'Strategic Projectile Type 155', 'class': 'Tactical'},
            'physical': {'mass': 20.5000, 'diam': 0.2050, 'ix': 0.02550},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_156'] = {
            'metadata': {'id': 156, 'name': 'Strategic Projectile Type 156', 'class': 'Tactical'},
            'physical': {'mass': 20.6000, 'diam': 0.2060, 'ix': 0.02560},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_157'] = {
            'metadata': {'id': 157, 'name': 'Strategic Projectile Type 157', 'class': 'Tactical'},
            'physical': {'mass': 20.7000, 'diam': 0.2070, 'ix': 0.02570},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_158'] = {
            'metadata': {'id': 158, 'name': 'Strategic Projectile Type 158', 'class': 'Tactical'},
            'physical': {'mass': 20.8000, 'diam': 0.2080, 'ix': 0.02580},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_159'] = {
            'metadata': {'id': 159, 'name': 'Strategic Projectile Type 159', 'class': 'Tactical'},
            'physical': {'mass': 20.9000, 'diam': 0.2090, 'ix': 0.02590},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.0900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_160'] = {
            'metadata': {'id': 160, 'name': 'Strategic Projectile Type 160', 'class': 'Tactical'},
            'physical': {'mass': 21.0000, 'diam': 0.2100, 'ix': 0.02600},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_161'] = {
            'metadata': {'id': 161, 'name': 'Strategic Projectile Type 161', 'class': 'Tactical'},
            'physical': {'mass': 21.1000, 'diam': 0.2110, 'ix': 0.02610},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_162'] = {
            'metadata': {'id': 162, 'name': 'Strategic Projectile Type 162', 'class': 'Tactical'},
            'physical': {'mass': 21.2000, 'diam': 0.2120, 'ix': 0.02620},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_163'] = {
            'metadata': {'id': 163, 'name': 'Strategic Projectile Type 163', 'class': 'Tactical'},
            'physical': {'mass': 21.3000, 'diam': 0.2130, 'ix': 0.02630},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_164'] = {
            'metadata': {'id': 164, 'name': 'Strategic Projectile Type 164', 'class': 'Tactical'},
            'physical': {'mass': 21.4000, 'diam': 0.2140, 'ix': 0.02640},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_165'] = {
            'metadata': {'id': 165, 'name': 'Strategic Projectile Type 165', 'class': 'Tactical'},
            'physical': {'mass': 21.5000, 'diam': 0.2150, 'ix': 0.02650},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_166'] = {
            'metadata': {'id': 166, 'name': 'Strategic Projectile Type 166', 'class': 'Tactical'},
            'physical': {'mass': 21.6000, 'diam': 0.2160, 'ix': 0.02660},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_167'] = {
            'metadata': {'id': 167, 'name': 'Strategic Projectile Type 167', 'class': 'Tactical'},
            'physical': {'mass': 21.7000, 'diam': 0.2170, 'ix': 0.02670},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_168'] = {
            'metadata': {'id': 168, 'name': 'Strategic Projectile Type 168', 'class': 'Tactical'},
            'physical': {'mass': 21.8000, 'diam': 0.2180, 'ix': 0.02680},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_169'] = {
            'metadata': {'id': 169, 'name': 'Strategic Projectile Type 169', 'class': 'Tactical'},
            'physical': {'mass': 21.9000, 'diam': 0.2190, 'ix': 0.02690},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.1900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_170'] = {
            'metadata': {'id': 170, 'name': 'Strategic Projectile Type 170', 'class': 'Tactical'},
            'physical': {'mass': 22.0000, 'diam': 0.2200, 'ix': 0.02700},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_171'] = {
            'metadata': {'id': 171, 'name': 'Strategic Projectile Type 171', 'class': 'Tactical'},
            'physical': {'mass': 22.1000, 'diam': 0.2210, 'ix': 0.02710},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_172'] = {
            'metadata': {'id': 172, 'name': 'Strategic Projectile Type 172', 'class': 'Tactical'},
            'physical': {'mass': 22.2000, 'diam': 0.2220, 'ix': 0.02720},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_173'] = {
            'metadata': {'id': 173, 'name': 'Strategic Projectile Type 173', 'class': 'Tactical'},
            'physical': {'mass': 22.3000, 'diam': 0.2230, 'ix': 0.02730},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_174'] = {
            'metadata': {'id': 174, 'name': 'Strategic Projectile Type 174', 'class': 'Tactical'},
            'physical': {'mass': 22.4000, 'diam': 0.2240, 'ix': 0.02740},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_175'] = {
            'metadata': {'id': 175, 'name': 'Strategic Projectile Type 175', 'class': 'Tactical'},
            'physical': {'mass': 22.5000, 'diam': 0.2250, 'ix': 0.02750},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_176'] = {
            'metadata': {'id': 176, 'name': 'Strategic Projectile Type 176', 'class': 'Tactical'},
            'physical': {'mass': 22.6000, 'diam': 0.2260, 'ix': 0.02760},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_177'] = {
            'metadata': {'id': 177, 'name': 'Strategic Projectile Type 177', 'class': 'Tactical'},
            'physical': {'mass': 22.7000, 'diam': 0.2270, 'ix': 0.02770},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_178'] = {
            'metadata': {'id': 178, 'name': 'Strategic Projectile Type 178', 'class': 'Tactical'},
            'physical': {'mass': 22.8000, 'diam': 0.2280, 'ix': 0.02780},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_179'] = {
            'metadata': {'id': 179, 'name': 'Strategic Projectile Type 179', 'class': 'Tactical'},
            'physical': {'mass': 22.9000, 'diam': 0.2290, 'ix': 0.02790},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.2900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_180'] = {
            'metadata': {'id': 180, 'name': 'Strategic Projectile Type 180', 'class': 'Tactical'},
            'physical': {'mass': 23.0000, 'diam': 0.2300, 'ix': 0.02800},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_181'] = {
            'metadata': {'id': 181, 'name': 'Strategic Projectile Type 181', 'class': 'Tactical'},
            'physical': {'mass': 23.1000, 'diam': 0.2310, 'ix': 0.02810},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_182'] = {
            'metadata': {'id': 182, 'name': 'Strategic Projectile Type 182', 'class': 'Tactical'},
            'physical': {'mass': 23.2000, 'diam': 0.2320, 'ix': 0.02820},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_183'] = {
            'metadata': {'id': 183, 'name': 'Strategic Projectile Type 183', 'class': 'Tactical'},
            'physical': {'mass': 23.3000, 'diam': 0.2330, 'ix': 0.02830},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_184'] = {
            'metadata': {'id': 184, 'name': 'Strategic Projectile Type 184', 'class': 'Tactical'},
            'physical': {'mass': 23.4000, 'diam': 0.2340, 'ix': 0.02840},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_185'] = {
            'metadata': {'id': 185, 'name': 'Strategic Projectile Type 185', 'class': 'Tactical'},
            'physical': {'mass': 23.5000, 'diam': 0.2350, 'ix': 0.02850},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_186'] = {
            'metadata': {'id': 186, 'name': 'Strategic Projectile Type 186', 'class': 'Tactical'},
            'physical': {'mass': 23.6000, 'diam': 0.2360, 'ix': 0.02860},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_187'] = {
            'metadata': {'id': 187, 'name': 'Strategic Projectile Type 187', 'class': 'Tactical'},
            'physical': {'mass': 23.7000, 'diam': 0.2370, 'ix': 0.02870},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_188'] = {
            'metadata': {'id': 188, 'name': 'Strategic Projectile Type 188', 'class': 'Tactical'},
            'physical': {'mass': 23.8000, 'diam': 0.2380, 'ix': 0.02880},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_189'] = {
            'metadata': {'id': 189, 'name': 'Strategic Projectile Type 189', 'class': 'Tactical'},
            'physical': {'mass': 23.9000, 'diam': 0.2390, 'ix': 0.02890},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.3900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_190'] = {
            'metadata': {'id': 190, 'name': 'Strategic Projectile Type 190', 'class': 'Tactical'},
            'physical': {'mass': 24.0000, 'diam': 0.2400, 'ix': 0.02900},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_191'] = {
            'metadata': {'id': 191, 'name': 'Strategic Projectile Type 191', 'class': 'Tactical'},
            'physical': {'mass': 24.1000, 'diam': 0.2410, 'ix': 0.02910},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_192'] = {
            'metadata': {'id': 192, 'name': 'Strategic Projectile Type 192', 'class': 'Tactical'},
            'physical': {'mass': 24.2000, 'diam': 0.2420, 'ix': 0.02920},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_193'] = {
            'metadata': {'id': 193, 'name': 'Strategic Projectile Type 193', 'class': 'Tactical'},
            'physical': {'mass': 24.3000, 'diam': 0.2430, 'ix': 0.02930},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_194'] = {
            'metadata': {'id': 194, 'name': 'Strategic Projectile Type 194', 'class': 'Tactical'},
            'physical': {'mass': 24.4000, 'diam': 0.2440, 'ix': 0.02940},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_195'] = {
            'metadata': {'id': 195, 'name': 'Strategic Projectile Type 195', 'class': 'Tactical'},
            'physical': {'mass': 24.5000, 'diam': 0.2450, 'ix': 0.02950},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_196'] = {
            'metadata': {'id': 196, 'name': 'Strategic Projectile Type 196', 'class': 'Tactical'},
            'physical': {'mass': 24.6000, 'diam': 0.2460, 'ix': 0.02960},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_197'] = {
            'metadata': {'id': 197, 'name': 'Strategic Projectile Type 197', 'class': 'Tactical'},
            'physical': {'mass': 24.7000, 'diam': 0.2470, 'ix': 0.02970},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_198'] = {
            'metadata': {'id': 198, 'name': 'Strategic Projectile Type 198', 'class': 'Tactical'},
            'physical': {'mass': 24.8000, 'diam': 0.2480, 'ix': 0.02980},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_199'] = {
            'metadata': {'id': 199, 'name': 'Strategic Projectile Type 199', 'class': 'Tactical'},
            'physical': {'mass': 24.9000, 'diam': 0.2490, 'ix': 0.02990},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.4900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_200'] = {
            'metadata': {'id': 200, 'name': 'Strategic Projectile Type 200', 'class': 'Tactical'},
            'physical': {'mass': 25.0000, 'diam': 0.2500, 'ix': 0.03000},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_201'] = {
            'metadata': {'id': 201, 'name': 'Strategic Projectile Type 201', 'class': 'Tactical'},
            'physical': {'mass': 25.1000, 'diam': 0.2510, 'ix': 0.03010},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_202'] = {
            'metadata': {'id': 202, 'name': 'Strategic Projectile Type 202', 'class': 'Tactical'},
            'physical': {'mass': 25.2000, 'diam': 0.2520, 'ix': 0.03020},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_203'] = {
            'metadata': {'id': 203, 'name': 'Strategic Projectile Type 203', 'class': 'Tactical'},
            'physical': {'mass': 25.3000, 'diam': 0.2530, 'ix': 0.03030},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_204'] = {
            'metadata': {'id': 204, 'name': 'Strategic Projectile Type 204', 'class': 'Tactical'},
            'physical': {'mass': 25.4000, 'diam': 0.2540, 'ix': 0.03040},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_205'] = {
            'metadata': {'id': 205, 'name': 'Strategic Projectile Type 205', 'class': 'Tactical'},
            'physical': {'mass': 25.5000, 'diam': 0.2550, 'ix': 0.03050},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_206'] = {
            'metadata': {'id': 206, 'name': 'Strategic Projectile Type 206', 'class': 'Tactical'},
            'physical': {'mass': 25.6000, 'diam': 0.2560, 'ix': 0.03060},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_207'] = {
            'metadata': {'id': 207, 'name': 'Strategic Projectile Type 207', 'class': 'Tactical'},
            'physical': {'mass': 25.7000, 'diam': 0.2570, 'ix': 0.03070},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_208'] = {
            'metadata': {'id': 208, 'name': 'Strategic Projectile Type 208', 'class': 'Tactical'},
            'physical': {'mass': 25.8000, 'diam': 0.2580, 'ix': 0.03080},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_209'] = {
            'metadata': {'id': 209, 'name': 'Strategic Projectile Type 209', 'class': 'Tactical'},
            'physical': {'mass': 25.9000, 'diam': 0.2590, 'ix': 0.03090},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.5900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_210'] = {
            'metadata': {'id': 210, 'name': 'Strategic Projectile Type 210', 'class': 'Tactical'},
            'physical': {'mass': 26.0000, 'diam': 0.2600, 'ix': 0.03100},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_211'] = {
            'metadata': {'id': 211, 'name': 'Strategic Projectile Type 211', 'class': 'Tactical'},
            'physical': {'mass': 26.1000, 'diam': 0.2610, 'ix': 0.03110},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_212'] = {
            'metadata': {'id': 212, 'name': 'Strategic Projectile Type 212', 'class': 'Tactical'},
            'physical': {'mass': 26.2000, 'diam': 0.2620, 'ix': 0.03120},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_213'] = {
            'metadata': {'id': 213, 'name': 'Strategic Projectile Type 213', 'class': 'Tactical'},
            'physical': {'mass': 26.3000, 'diam': 0.2630, 'ix': 0.03130},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_214'] = {
            'metadata': {'id': 214, 'name': 'Strategic Projectile Type 214', 'class': 'Tactical'},
            'physical': {'mass': 26.4000, 'diam': 0.2640, 'ix': 0.03140},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_215'] = {
            'metadata': {'id': 215, 'name': 'Strategic Projectile Type 215', 'class': 'Tactical'},
            'physical': {'mass': 26.5000, 'diam': 0.2650, 'ix': 0.03150},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_216'] = {
            'metadata': {'id': 216, 'name': 'Strategic Projectile Type 216', 'class': 'Tactical'},
            'physical': {'mass': 26.6000, 'diam': 0.2660, 'ix': 0.03160},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_217'] = {
            'metadata': {'id': 217, 'name': 'Strategic Projectile Type 217', 'class': 'Tactical'},
            'physical': {'mass': 26.7000, 'diam': 0.2670, 'ix': 0.03170},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_218'] = {
            'metadata': {'id': 218, 'name': 'Strategic Projectile Type 218', 'class': 'Tactical'},
            'physical': {'mass': 26.8000, 'diam': 0.2680, 'ix': 0.03180},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_219'] = {
            'metadata': {'id': 219, 'name': 'Strategic Projectile Type 219', 'class': 'Tactical'},
            'physical': {'mass': 26.9000, 'diam': 0.2690, 'ix': 0.03190},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.6900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_220'] = {
            'metadata': {'id': 220, 'name': 'Strategic Projectile Type 220', 'class': 'Tactical'},
            'physical': {'mass': 27.0000, 'diam': 0.2700, 'ix': 0.03200},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_221'] = {
            'metadata': {'id': 221, 'name': 'Strategic Projectile Type 221', 'class': 'Tactical'},
            'physical': {'mass': 27.1000, 'diam': 0.2710, 'ix': 0.03210},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_222'] = {
            'metadata': {'id': 222, 'name': 'Strategic Projectile Type 222', 'class': 'Tactical'},
            'physical': {'mass': 27.2000, 'diam': 0.2720, 'ix': 0.03220},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_223'] = {
            'metadata': {'id': 223, 'name': 'Strategic Projectile Type 223', 'class': 'Tactical'},
            'physical': {'mass': 27.3000, 'diam': 0.2730, 'ix': 0.03230},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_224'] = {
            'metadata': {'id': 224, 'name': 'Strategic Projectile Type 224', 'class': 'Tactical'},
            'physical': {'mass': 27.4000, 'diam': 0.2740, 'ix': 0.03240},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_225'] = {
            'metadata': {'id': 225, 'name': 'Strategic Projectile Type 225', 'class': 'Tactical'},
            'physical': {'mass': 27.5000, 'diam': 0.2750, 'ix': 0.03250},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_226'] = {
            'metadata': {'id': 226, 'name': 'Strategic Projectile Type 226', 'class': 'Tactical'},
            'physical': {'mass': 27.6000, 'diam': 0.2760, 'ix': 0.03260},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_227'] = {
            'metadata': {'id': 227, 'name': 'Strategic Projectile Type 227', 'class': 'Tactical'},
            'physical': {'mass': 27.7000, 'diam': 0.2770, 'ix': 0.03270},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_228'] = {
            'metadata': {'id': 228, 'name': 'Strategic Projectile Type 228', 'class': 'Tactical'},
            'physical': {'mass': 27.8000, 'diam': 0.2780, 'ix': 0.03280},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_229'] = {
            'metadata': {'id': 229, 'name': 'Strategic Projectile Type 229', 'class': 'Tactical'},
            'physical': {'mass': 27.9000, 'diam': 0.2790, 'ix': 0.03290},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.7900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_230'] = {
            'metadata': {'id': 230, 'name': 'Strategic Projectile Type 230', 'class': 'Tactical'},
            'physical': {'mass': 28.0000, 'diam': 0.2800, 'ix': 0.03300},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_231'] = {
            'metadata': {'id': 231, 'name': 'Strategic Projectile Type 231', 'class': 'Tactical'},
            'physical': {'mass': 28.1000, 'diam': 0.2810, 'ix': 0.03310},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_232'] = {
            'metadata': {'id': 232, 'name': 'Strategic Projectile Type 232', 'class': 'Tactical'},
            'physical': {'mass': 28.2000, 'diam': 0.2820, 'ix': 0.03320},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_233'] = {
            'metadata': {'id': 233, 'name': 'Strategic Projectile Type 233', 'class': 'Tactical'},
            'physical': {'mass': 28.3000, 'diam': 0.2830, 'ix': 0.03330},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_234'] = {
            'metadata': {'id': 234, 'name': 'Strategic Projectile Type 234', 'class': 'Tactical'},
            'physical': {'mass': 28.4000, 'diam': 0.2840, 'ix': 0.03340},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_235'] = {
            'metadata': {'id': 235, 'name': 'Strategic Projectile Type 235', 'class': 'Tactical'},
            'physical': {'mass': 28.5000, 'diam': 0.2850, 'ix': 0.03350},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_236'] = {
            'metadata': {'id': 236, 'name': 'Strategic Projectile Type 236', 'class': 'Tactical'},
            'physical': {'mass': 28.6000, 'diam': 0.2860, 'ix': 0.03360},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_237'] = {
            'metadata': {'id': 237, 'name': 'Strategic Projectile Type 237', 'class': 'Tactical'},
            'physical': {'mass': 28.7000, 'diam': 0.2870, 'ix': 0.03370},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_238'] = {
            'metadata': {'id': 238, 'name': 'Strategic Projectile Type 238', 'class': 'Tactical'},
            'physical': {'mass': 28.8000, 'diam': 0.2880, 'ix': 0.03380},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_239'] = {
            'metadata': {'id': 239, 'name': 'Strategic Projectile Type 239', 'class': 'Tactical'},
            'physical': {'mass': 28.9000, 'diam': 0.2890, 'ix': 0.03390},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.8900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_240'] = {
            'metadata': {'id': 240, 'name': 'Strategic Projectile Type 240', 'class': 'Tactical'},
            'physical': {'mass': 29.0000, 'diam': 0.2900, 'ix': 0.03400},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_241'] = {
            'metadata': {'id': 241, 'name': 'Strategic Projectile Type 241', 'class': 'Tactical'},
            'physical': {'mass': 29.1000, 'diam': 0.2910, 'ix': 0.03410},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_242'] = {
            'metadata': {'id': 242, 'name': 'Strategic Projectile Type 242', 'class': 'Tactical'},
            'physical': {'mass': 29.2000, 'diam': 0.2920, 'ix': 0.03420},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_243'] = {
            'metadata': {'id': 243, 'name': 'Strategic Projectile Type 243', 'class': 'Tactical'},
            'physical': {'mass': 29.3000, 'diam': 0.2930, 'ix': 0.03430},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_244'] = {
            'metadata': {'id': 244, 'name': 'Strategic Projectile Type 244', 'class': 'Tactical'},
            'physical': {'mass': 29.4000, 'diam': 0.2940, 'ix': 0.03440},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_245'] = {
            'metadata': {'id': 245, 'name': 'Strategic Projectile Type 245', 'class': 'Tactical'},
            'physical': {'mass': 29.5000, 'diam': 0.2950, 'ix': 0.03450},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_246'] = {
            'metadata': {'id': 246, 'name': 'Strategic Projectile Type 246', 'class': 'Tactical'},
            'physical': {'mass': 29.6000, 'diam': 0.2960, 'ix': 0.03460},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_247'] = {
            'metadata': {'id': 247, 'name': 'Strategic Projectile Type 247', 'class': 'Tactical'},
            'physical': {'mass': 29.7000, 'diam': 0.2970, 'ix': 0.03470},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_248'] = {
            'metadata': {'id': 248, 'name': 'Strategic Projectile Type 248', 'class': 'Tactical'},
            'physical': {'mass': 29.8000, 'diam': 0.2980, 'ix': 0.03480},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_249'] = {
            'metadata': {'id': 249, 'name': 'Strategic Projectile Type 249', 'class': 'Tactical'},
            'physical': {'mass': 29.9000, 'diam': 0.2990, 'ix': 0.03490},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 3.9900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_250'] = {
            'metadata': {'id': 250, 'name': 'Strategic Projectile Type 250', 'class': 'Tactical'},
            'physical': {'mass': 30.0000, 'diam': 0.3000, 'ix': 0.03500},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_251'] = {
            'metadata': {'id': 251, 'name': 'Strategic Projectile Type 251', 'class': 'Tactical'},
            'physical': {'mass': 30.1000, 'diam': 0.3010, 'ix': 0.03510},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_252'] = {
            'metadata': {'id': 252, 'name': 'Strategic Projectile Type 252', 'class': 'Tactical'},
            'physical': {'mass': 30.2000, 'diam': 0.3020, 'ix': 0.03520},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_253'] = {
            'metadata': {'id': 253, 'name': 'Strategic Projectile Type 253', 'class': 'Tactical'},
            'physical': {'mass': 30.3000, 'diam': 0.3030, 'ix': 0.03530},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_254'] = {
            'metadata': {'id': 254, 'name': 'Strategic Projectile Type 254', 'class': 'Tactical'},
            'physical': {'mass': 30.4000, 'diam': 0.3040, 'ix': 0.03540},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_255'] = {
            'metadata': {'id': 255, 'name': 'Strategic Projectile Type 255', 'class': 'Tactical'},
            'physical': {'mass': 30.5000, 'diam': 0.3050, 'ix': 0.03550},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_256'] = {
            'metadata': {'id': 256, 'name': 'Strategic Projectile Type 256', 'class': 'Tactical'},
            'physical': {'mass': 30.6000, 'diam': 0.3060, 'ix': 0.03560},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_257'] = {
            'metadata': {'id': 257, 'name': 'Strategic Projectile Type 257', 'class': 'Tactical'},
            'physical': {'mass': 30.7000, 'diam': 0.3070, 'ix': 0.03570},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_258'] = {
            'metadata': {'id': 258, 'name': 'Strategic Projectile Type 258', 'class': 'Tactical'},
            'physical': {'mass': 30.8000, 'diam': 0.3080, 'ix': 0.03580},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_259'] = {
            'metadata': {'id': 259, 'name': 'Strategic Projectile Type 259', 'class': 'Tactical'},
            'physical': {'mass': 30.9000, 'diam': 0.3090, 'ix': 0.03590},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.0900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_260'] = {
            'metadata': {'id': 260, 'name': 'Strategic Projectile Type 260', 'class': 'Tactical'},
            'physical': {'mass': 31.0000, 'diam': 0.3100, 'ix': 0.03600},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_261'] = {
            'metadata': {'id': 261, 'name': 'Strategic Projectile Type 261', 'class': 'Tactical'},
            'physical': {'mass': 31.1000, 'diam': 0.3110, 'ix': 0.03610},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_262'] = {
            'metadata': {'id': 262, 'name': 'Strategic Projectile Type 262', 'class': 'Tactical'},
            'physical': {'mass': 31.2000, 'diam': 0.3120, 'ix': 0.03620},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_263'] = {
            'metadata': {'id': 263, 'name': 'Strategic Projectile Type 263', 'class': 'Tactical'},
            'physical': {'mass': 31.3000, 'diam': 0.3130, 'ix': 0.03630},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_264'] = {
            'metadata': {'id': 264, 'name': 'Strategic Projectile Type 264', 'class': 'Tactical'},
            'physical': {'mass': 31.4000, 'diam': 0.3140, 'ix': 0.03640},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_265'] = {
            'metadata': {'id': 265, 'name': 'Strategic Projectile Type 265', 'class': 'Tactical'},
            'physical': {'mass': 31.5000, 'diam': 0.3150, 'ix': 0.03650},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_266'] = {
            'metadata': {'id': 266, 'name': 'Strategic Projectile Type 266', 'class': 'Tactical'},
            'physical': {'mass': 31.6000, 'diam': 0.3160, 'ix': 0.03660},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_267'] = {
            'metadata': {'id': 267, 'name': 'Strategic Projectile Type 267', 'class': 'Tactical'},
            'physical': {'mass': 31.7000, 'diam': 0.3170, 'ix': 0.03670},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_268'] = {
            'metadata': {'id': 268, 'name': 'Strategic Projectile Type 268', 'class': 'Tactical'},
            'physical': {'mass': 31.8000, 'diam': 0.3180, 'ix': 0.03680},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_269'] = {
            'metadata': {'id': 269, 'name': 'Strategic Projectile Type 269', 'class': 'Tactical'},
            'physical': {'mass': 31.9000, 'diam': 0.3190, 'ix': 0.03690},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.1900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_270'] = {
            'metadata': {'id': 270, 'name': 'Strategic Projectile Type 270', 'class': 'Tactical'},
            'physical': {'mass': 32.0000, 'diam': 0.3200, 'ix': 0.03700},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_271'] = {
            'metadata': {'id': 271, 'name': 'Strategic Projectile Type 271', 'class': 'Tactical'},
            'physical': {'mass': 32.1000, 'diam': 0.3210, 'ix': 0.03710},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_272'] = {
            'metadata': {'id': 272, 'name': 'Strategic Projectile Type 272', 'class': 'Tactical'},
            'physical': {'mass': 32.2000, 'diam': 0.3220, 'ix': 0.03720},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_273'] = {
            'metadata': {'id': 273, 'name': 'Strategic Projectile Type 273', 'class': 'Tactical'},
            'physical': {'mass': 32.3000, 'diam': 0.3230, 'ix': 0.03730},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_274'] = {
            'metadata': {'id': 274, 'name': 'Strategic Projectile Type 274', 'class': 'Tactical'},
            'physical': {'mass': 32.4000, 'diam': 0.3240, 'ix': 0.03740},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_275'] = {
            'metadata': {'id': 275, 'name': 'Strategic Projectile Type 275', 'class': 'Tactical'},
            'physical': {'mass': 32.5000, 'diam': 0.3250, 'ix': 0.03750},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_276'] = {
            'metadata': {'id': 276, 'name': 'Strategic Projectile Type 276', 'class': 'Tactical'},
            'physical': {'mass': 32.6000, 'diam': 0.3260, 'ix': 0.03760},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_277'] = {
            'metadata': {'id': 277, 'name': 'Strategic Projectile Type 277', 'class': 'Tactical'},
            'physical': {'mass': 32.7000, 'diam': 0.3270, 'ix': 0.03770},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_278'] = {
            'metadata': {'id': 278, 'name': 'Strategic Projectile Type 278', 'class': 'Tactical'},
            'physical': {'mass': 32.8000, 'diam': 0.3280, 'ix': 0.03780},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_279'] = {
            'metadata': {'id': 279, 'name': 'Strategic Projectile Type 279', 'class': 'Tactical'},
            'physical': {'mass': 32.9000, 'diam': 0.3290, 'ix': 0.03790},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.2900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_280'] = {
            'metadata': {'id': 280, 'name': 'Strategic Projectile Type 280', 'class': 'Tactical'},
            'physical': {'mass': 33.0000, 'diam': 0.3300, 'ix': 0.03800},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_281'] = {
            'metadata': {'id': 281, 'name': 'Strategic Projectile Type 281', 'class': 'Tactical'},
            'physical': {'mass': 33.1000, 'diam': 0.3310, 'ix': 0.03810},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_282'] = {
            'metadata': {'id': 282, 'name': 'Strategic Projectile Type 282', 'class': 'Tactical'},
            'physical': {'mass': 33.2000, 'diam': 0.3320, 'ix': 0.03820},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_283'] = {
            'metadata': {'id': 283, 'name': 'Strategic Projectile Type 283', 'class': 'Tactical'},
            'physical': {'mass': 33.3000, 'diam': 0.3330, 'ix': 0.03830},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_284'] = {
            'metadata': {'id': 284, 'name': 'Strategic Projectile Type 284', 'class': 'Tactical'},
            'physical': {'mass': 33.4000, 'diam': 0.3340, 'ix': 0.03840},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_285'] = {
            'metadata': {'id': 285, 'name': 'Strategic Projectile Type 285', 'class': 'Tactical'},
            'physical': {'mass': 33.5000, 'diam': 0.3350, 'ix': 0.03850},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_286'] = {
            'metadata': {'id': 286, 'name': 'Strategic Projectile Type 286', 'class': 'Tactical'},
            'physical': {'mass': 33.6000, 'diam': 0.3360, 'ix': 0.03860},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_287'] = {
            'metadata': {'id': 287, 'name': 'Strategic Projectile Type 287', 'class': 'Tactical'},
            'physical': {'mass': 33.7000, 'diam': 0.3370, 'ix': 0.03870},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_288'] = {
            'metadata': {'id': 288, 'name': 'Strategic Projectile Type 288', 'class': 'Tactical'},
            'physical': {'mass': 33.8000, 'diam': 0.3380, 'ix': 0.03880},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_289'] = {
            'metadata': {'id': 289, 'name': 'Strategic Projectile Type 289', 'class': 'Tactical'},
            'physical': {'mass': 33.9000, 'diam': 0.3390, 'ix': 0.03890},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.3900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_290'] = {
            'metadata': {'id': 290, 'name': 'Strategic Projectile Type 290', 'class': 'Tactical'},
            'physical': {'mass': 34.0000, 'diam': 0.3400, 'ix': 0.03900},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_291'] = {
            'metadata': {'id': 291, 'name': 'Strategic Projectile Type 291', 'class': 'Tactical'},
            'physical': {'mass': 34.1000, 'diam': 0.3410, 'ix': 0.03910},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_292'] = {
            'metadata': {'id': 292, 'name': 'Strategic Projectile Type 292', 'class': 'Tactical'},
            'physical': {'mass': 34.2000, 'diam': 0.3420, 'ix': 0.03920},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_293'] = {
            'metadata': {'id': 293, 'name': 'Strategic Projectile Type 293', 'class': 'Tactical'},
            'physical': {'mass': 34.3000, 'diam': 0.3430, 'ix': 0.03930},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_294'] = {
            'metadata': {'id': 294, 'name': 'Strategic Projectile Type 294', 'class': 'Tactical'},
            'physical': {'mass': 34.4000, 'diam': 0.3440, 'ix': 0.03940},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_295'] = {
            'metadata': {'id': 295, 'name': 'Strategic Projectile Type 295', 'class': 'Tactical'},
            'physical': {'mass': 34.5000, 'diam': 0.3450, 'ix': 0.03950},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_296'] = {
            'metadata': {'id': 296, 'name': 'Strategic Projectile Type 296', 'class': 'Tactical'},
            'physical': {'mass': 34.6000, 'diam': 0.3460, 'ix': 0.03960},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_297'] = {
            'metadata': {'id': 297, 'name': 'Strategic Projectile Type 297', 'class': 'Tactical'},
            'physical': {'mass': 34.7000, 'diam': 0.3470, 'ix': 0.03970},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_298'] = {
            'metadata': {'id': 298, 'name': 'Strategic Projectile Type 298', 'class': 'Tactical'},
            'physical': {'mass': 34.8000, 'diam': 0.3480, 'ix': 0.03980},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_299'] = {
            'metadata': {'id': 299, 'name': 'Strategic Projectile Type 299', 'class': 'Tactical'},
            'physical': {'mass': 34.9000, 'diam': 0.3490, 'ix': 0.03990},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.4900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_300'] = {
            'metadata': {'id': 300, 'name': 'Strategic Projectile Type 300', 'class': 'Tactical'},
            'physical': {'mass': 35.0000, 'diam': 0.3500, 'ix': 0.04000},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_301'] = {
            'metadata': {'id': 301, 'name': 'Strategic Projectile Type 301', 'class': 'Tactical'},
            'physical': {'mass': 35.1000, 'diam': 0.3510, 'ix': 0.04010},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_302'] = {
            'metadata': {'id': 302, 'name': 'Strategic Projectile Type 302', 'class': 'Tactical'},
            'physical': {'mass': 35.2000, 'diam': 0.3520, 'ix': 0.04020},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_303'] = {
            'metadata': {'id': 303, 'name': 'Strategic Projectile Type 303', 'class': 'Tactical'},
            'physical': {'mass': 35.3000, 'diam': 0.3530, 'ix': 0.04030},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_304'] = {
            'metadata': {'id': 304, 'name': 'Strategic Projectile Type 304', 'class': 'Tactical'},
            'physical': {'mass': 35.4000, 'diam': 0.3540, 'ix': 0.04040},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_305'] = {
            'metadata': {'id': 305, 'name': 'Strategic Projectile Type 305', 'class': 'Tactical'},
            'physical': {'mass': 35.5000, 'diam': 0.3550, 'ix': 0.04050},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_306'] = {
            'metadata': {'id': 306, 'name': 'Strategic Projectile Type 306', 'class': 'Tactical'},
            'physical': {'mass': 35.6000, 'diam': 0.3560, 'ix': 0.04060},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_307'] = {
            'metadata': {'id': 307, 'name': 'Strategic Projectile Type 307', 'class': 'Tactical'},
            'physical': {'mass': 35.7000, 'diam': 0.3570, 'ix': 0.04070},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_308'] = {
            'metadata': {'id': 308, 'name': 'Strategic Projectile Type 308', 'class': 'Tactical'},
            'physical': {'mass': 35.8000, 'diam': 0.3580, 'ix': 0.04080},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_309'] = {
            'metadata': {'id': 309, 'name': 'Strategic Projectile Type 309', 'class': 'Tactical'},
            'physical': {'mass': 35.9000, 'diam': 0.3590, 'ix': 0.04090},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.5900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_310'] = {
            'metadata': {'id': 310, 'name': 'Strategic Projectile Type 310', 'class': 'Tactical'},
            'physical': {'mass': 36.0000, 'diam': 0.3600, 'ix': 0.04100},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_311'] = {
            'metadata': {'id': 311, 'name': 'Strategic Projectile Type 311', 'class': 'Tactical'},
            'physical': {'mass': 36.1000, 'diam': 0.3610, 'ix': 0.04110},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_312'] = {
            'metadata': {'id': 312, 'name': 'Strategic Projectile Type 312', 'class': 'Tactical'},
            'physical': {'mass': 36.2000, 'diam': 0.3620, 'ix': 0.04120},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_313'] = {
            'metadata': {'id': 313, 'name': 'Strategic Projectile Type 313', 'class': 'Tactical'},
            'physical': {'mass': 36.3000, 'diam': 0.3630, 'ix': 0.04130},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_314'] = {
            'metadata': {'id': 314, 'name': 'Strategic Projectile Type 314', 'class': 'Tactical'},
            'physical': {'mass': 36.4000, 'diam': 0.3640, 'ix': 0.04140},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_315'] = {
            'metadata': {'id': 315, 'name': 'Strategic Projectile Type 315', 'class': 'Tactical'},
            'physical': {'mass': 36.5000, 'diam': 0.3650, 'ix': 0.04150},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_316'] = {
            'metadata': {'id': 316, 'name': 'Strategic Projectile Type 316', 'class': 'Tactical'},
            'physical': {'mass': 36.6000, 'diam': 0.3660, 'ix': 0.04160},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_317'] = {
            'metadata': {'id': 317, 'name': 'Strategic Projectile Type 317', 'class': 'Tactical'},
            'physical': {'mass': 36.7000, 'diam': 0.3670, 'ix': 0.04170},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_318'] = {
            'metadata': {'id': 318, 'name': 'Strategic Projectile Type 318', 'class': 'Tactical'},
            'physical': {'mass': 36.8000, 'diam': 0.3680, 'ix': 0.04180},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_319'] = {
            'metadata': {'id': 319, 'name': 'Strategic Projectile Type 319', 'class': 'Tactical'},
            'physical': {'mass': 36.9000, 'diam': 0.3690, 'ix': 0.04190},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.6900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_320'] = {
            'metadata': {'id': 320, 'name': 'Strategic Projectile Type 320', 'class': 'Tactical'},
            'physical': {'mass': 37.0000, 'diam': 0.3700, 'ix': 0.04200},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_321'] = {
            'metadata': {'id': 321, 'name': 'Strategic Projectile Type 321', 'class': 'Tactical'},
            'physical': {'mass': 37.1000, 'diam': 0.3710, 'ix': 0.04210},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_322'] = {
            'metadata': {'id': 322, 'name': 'Strategic Projectile Type 322', 'class': 'Tactical'},
            'physical': {'mass': 37.2000, 'diam': 0.3720, 'ix': 0.04220},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_323'] = {
            'metadata': {'id': 323, 'name': 'Strategic Projectile Type 323', 'class': 'Tactical'},
            'physical': {'mass': 37.3000, 'diam': 0.3730, 'ix': 0.04230},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_324'] = {
            'metadata': {'id': 324, 'name': 'Strategic Projectile Type 324', 'class': 'Tactical'},
            'physical': {'mass': 37.4000, 'diam': 0.3740, 'ix': 0.04240},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_325'] = {
            'metadata': {'id': 325, 'name': 'Strategic Projectile Type 325', 'class': 'Tactical'},
            'physical': {'mass': 37.5000, 'diam': 0.3750, 'ix': 0.04250},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_326'] = {
            'metadata': {'id': 326, 'name': 'Strategic Projectile Type 326', 'class': 'Tactical'},
            'physical': {'mass': 37.6000, 'diam': 0.3760, 'ix': 0.04260},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_327'] = {
            'metadata': {'id': 327, 'name': 'Strategic Projectile Type 327', 'class': 'Tactical'},
            'physical': {'mass': 37.7000, 'diam': 0.3770, 'ix': 0.04270},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_328'] = {
            'metadata': {'id': 328, 'name': 'Strategic Projectile Type 328', 'class': 'Tactical'},
            'physical': {'mass': 37.8000, 'diam': 0.3780, 'ix': 0.04280},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_329'] = {
            'metadata': {'id': 329, 'name': 'Strategic Projectile Type 329', 'class': 'Tactical'},
            'physical': {'mass': 37.9000, 'diam': 0.3790, 'ix': 0.04290},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.7900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_330'] = {
            'metadata': {'id': 330, 'name': 'Strategic Projectile Type 330', 'class': 'Tactical'},
            'physical': {'mass': 38.0000, 'diam': 0.3800, 'ix': 0.04300},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_331'] = {
            'metadata': {'id': 331, 'name': 'Strategic Projectile Type 331', 'class': 'Tactical'},
            'physical': {'mass': 38.1000, 'diam': 0.3810, 'ix': 0.04310},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_332'] = {
            'metadata': {'id': 332, 'name': 'Strategic Projectile Type 332', 'class': 'Tactical'},
            'physical': {'mass': 38.2000, 'diam': 0.3820, 'ix': 0.04320},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_333'] = {
            'metadata': {'id': 333, 'name': 'Strategic Projectile Type 333', 'class': 'Tactical'},
            'physical': {'mass': 38.3000, 'diam': 0.3830, 'ix': 0.04330},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_334'] = {
            'metadata': {'id': 334, 'name': 'Strategic Projectile Type 334', 'class': 'Tactical'},
            'physical': {'mass': 38.4000, 'diam': 0.3840, 'ix': 0.04340},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_335'] = {
            'metadata': {'id': 335, 'name': 'Strategic Projectile Type 335', 'class': 'Tactical'},
            'physical': {'mass': 38.5000, 'diam': 0.3850, 'ix': 0.04350},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_336'] = {
            'metadata': {'id': 336, 'name': 'Strategic Projectile Type 336', 'class': 'Tactical'},
            'physical': {'mass': 38.6000, 'diam': 0.3860, 'ix': 0.04360},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_337'] = {
            'metadata': {'id': 337, 'name': 'Strategic Projectile Type 337', 'class': 'Tactical'},
            'physical': {'mass': 38.7000, 'diam': 0.3870, 'ix': 0.04370},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_338'] = {
            'metadata': {'id': 338, 'name': 'Strategic Projectile Type 338', 'class': 'Tactical'},
            'physical': {'mass': 38.8000, 'diam': 0.3880, 'ix': 0.04380},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_339'] = {
            'metadata': {'id': 339, 'name': 'Strategic Projectile Type 339', 'class': 'Tactical'},
            'physical': {'mass': 38.9000, 'diam': 0.3890, 'ix': 0.04390},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.8900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_340'] = {
            'metadata': {'id': 340, 'name': 'Strategic Projectile Type 340', 'class': 'Tactical'},
            'physical': {'mass': 39.0000, 'diam': 0.3900, 'ix': 0.04400},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_341'] = {
            'metadata': {'id': 341, 'name': 'Strategic Projectile Type 341', 'class': 'Tactical'},
            'physical': {'mass': 39.1000, 'diam': 0.3910, 'ix': 0.04410},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_342'] = {
            'metadata': {'id': 342, 'name': 'Strategic Projectile Type 342', 'class': 'Tactical'},
            'physical': {'mass': 39.2000, 'diam': 0.3920, 'ix': 0.04420},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_343'] = {
            'metadata': {'id': 343, 'name': 'Strategic Projectile Type 343', 'class': 'Tactical'},
            'physical': {'mass': 39.3000, 'diam': 0.3930, 'ix': 0.04430},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_344'] = {
            'metadata': {'id': 344, 'name': 'Strategic Projectile Type 344', 'class': 'Tactical'},
            'physical': {'mass': 39.4000, 'diam': 0.3940, 'ix': 0.04440},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_345'] = {
            'metadata': {'id': 345, 'name': 'Strategic Projectile Type 345', 'class': 'Tactical'},
            'physical': {'mass': 39.5000, 'diam': 0.3950, 'ix': 0.04450},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_346'] = {
            'metadata': {'id': 346, 'name': 'Strategic Projectile Type 346', 'class': 'Tactical'},
            'physical': {'mass': 39.6000, 'diam': 0.3960, 'ix': 0.04460},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_347'] = {
            'metadata': {'id': 347, 'name': 'Strategic Projectile Type 347', 'class': 'Tactical'},
            'physical': {'mass': 39.7000, 'diam': 0.3970, 'ix': 0.04470},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_348'] = {
            'metadata': {'id': 348, 'name': 'Strategic Projectile Type 348', 'class': 'Tactical'},
            'physical': {'mass': 39.8000, 'diam': 0.3980, 'ix': 0.04480},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_349'] = {
            'metadata': {'id': 349, 'name': 'Strategic Projectile Type 349', 'class': 'Tactical'},
            'physical': {'mass': 39.9000, 'diam': 0.3990, 'ix': 0.04490},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 4.9900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_350'] = {
            'metadata': {'id': 350, 'name': 'Strategic Projectile Type 350', 'class': 'Tactical'},
            'physical': {'mass': 40.0000, 'diam': 0.4000, 'ix': 0.04500},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_351'] = {
            'metadata': {'id': 351, 'name': 'Strategic Projectile Type 351', 'class': 'Tactical'},
            'physical': {'mass': 40.1000, 'diam': 0.4010, 'ix': 0.04510},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_352'] = {
            'metadata': {'id': 352, 'name': 'Strategic Projectile Type 352', 'class': 'Tactical'},
            'physical': {'mass': 40.2000, 'diam': 0.4020, 'ix': 0.04520},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_353'] = {
            'metadata': {'id': 353, 'name': 'Strategic Projectile Type 353', 'class': 'Tactical'},
            'physical': {'mass': 40.3000, 'diam': 0.4030, 'ix': 0.04530},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_354'] = {
            'metadata': {'id': 354, 'name': 'Strategic Projectile Type 354', 'class': 'Tactical'},
            'physical': {'mass': 40.4000, 'diam': 0.4040, 'ix': 0.04540},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_355'] = {
            'metadata': {'id': 355, 'name': 'Strategic Projectile Type 355', 'class': 'Tactical'},
            'physical': {'mass': 40.5000, 'diam': 0.4050, 'ix': 0.04550},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_356'] = {
            'metadata': {'id': 356, 'name': 'Strategic Projectile Type 356', 'class': 'Tactical'},
            'physical': {'mass': 40.6000, 'diam': 0.4060, 'ix': 0.04560},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_357'] = {
            'metadata': {'id': 357, 'name': 'Strategic Projectile Type 357', 'class': 'Tactical'},
            'physical': {'mass': 40.7000, 'diam': 0.4070, 'ix': 0.04570},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_358'] = {
            'metadata': {'id': 358, 'name': 'Strategic Projectile Type 358', 'class': 'Tactical'},
            'physical': {'mass': 40.8000, 'diam': 0.4080, 'ix': 0.04580},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_359'] = {
            'metadata': {'id': 359, 'name': 'Strategic Projectile Type 359', 'class': 'Tactical'},
            'physical': {'mass': 40.9000, 'diam': 0.4090, 'ix': 0.04590},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.0900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_360'] = {
            'metadata': {'id': 360, 'name': 'Strategic Projectile Type 360', 'class': 'Tactical'},
            'physical': {'mass': 41.0000, 'diam': 0.4100, 'ix': 0.04600},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_361'] = {
            'metadata': {'id': 361, 'name': 'Strategic Projectile Type 361', 'class': 'Tactical'},
            'physical': {'mass': 41.1000, 'diam': 0.4110, 'ix': 0.04610},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_362'] = {
            'metadata': {'id': 362, 'name': 'Strategic Projectile Type 362', 'class': 'Tactical'},
            'physical': {'mass': 41.2000, 'diam': 0.4120, 'ix': 0.04620},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_363'] = {
            'metadata': {'id': 363, 'name': 'Strategic Projectile Type 363', 'class': 'Tactical'},
            'physical': {'mass': 41.3000, 'diam': 0.4130, 'ix': 0.04630},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_364'] = {
            'metadata': {'id': 364, 'name': 'Strategic Projectile Type 364', 'class': 'Tactical'},
            'physical': {'mass': 41.4000, 'diam': 0.4140, 'ix': 0.04640},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_365'] = {
            'metadata': {'id': 365, 'name': 'Strategic Projectile Type 365', 'class': 'Tactical'},
            'physical': {'mass': 41.5000, 'diam': 0.4150, 'ix': 0.04650},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_366'] = {
            'metadata': {'id': 366, 'name': 'Strategic Projectile Type 366', 'class': 'Tactical'},
            'physical': {'mass': 41.6000, 'diam': 0.4160, 'ix': 0.04660},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_367'] = {
            'metadata': {'id': 367, 'name': 'Strategic Projectile Type 367', 'class': 'Tactical'},
            'physical': {'mass': 41.7000, 'diam': 0.4170, 'ix': 0.04670},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_368'] = {
            'metadata': {'id': 368, 'name': 'Strategic Projectile Type 368', 'class': 'Tactical'},
            'physical': {'mass': 41.8000, 'diam': 0.4180, 'ix': 0.04680},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_369'] = {
            'metadata': {'id': 369, 'name': 'Strategic Projectile Type 369', 'class': 'Tactical'},
            'physical': {'mass': 41.9000, 'diam': 0.4190, 'ix': 0.04690},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.1900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_370'] = {
            'metadata': {'id': 370, 'name': 'Strategic Projectile Type 370', 'class': 'Tactical'},
            'physical': {'mass': 42.0000, 'diam': 0.4200, 'ix': 0.04700},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_371'] = {
            'metadata': {'id': 371, 'name': 'Strategic Projectile Type 371', 'class': 'Tactical'},
            'physical': {'mass': 42.1000, 'diam': 0.4210, 'ix': 0.04710},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_372'] = {
            'metadata': {'id': 372, 'name': 'Strategic Projectile Type 372', 'class': 'Tactical'},
            'physical': {'mass': 42.2000, 'diam': 0.4220, 'ix': 0.04720},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_373'] = {
            'metadata': {'id': 373, 'name': 'Strategic Projectile Type 373', 'class': 'Tactical'},
            'physical': {'mass': 42.3000, 'diam': 0.4230, 'ix': 0.04730},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_374'] = {
            'metadata': {'id': 374, 'name': 'Strategic Projectile Type 374', 'class': 'Tactical'},
            'physical': {'mass': 42.4000, 'diam': 0.4240, 'ix': 0.04740},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_375'] = {
            'metadata': {'id': 375, 'name': 'Strategic Projectile Type 375', 'class': 'Tactical'},
            'physical': {'mass': 42.5000, 'diam': 0.4250, 'ix': 0.04750},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_376'] = {
            'metadata': {'id': 376, 'name': 'Strategic Projectile Type 376', 'class': 'Tactical'},
            'physical': {'mass': 42.6000, 'diam': 0.4260, 'ix': 0.04760},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_377'] = {
            'metadata': {'id': 377, 'name': 'Strategic Projectile Type 377', 'class': 'Tactical'},
            'physical': {'mass': 42.7000, 'diam': 0.4270, 'ix': 0.04770},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_378'] = {
            'metadata': {'id': 378, 'name': 'Strategic Projectile Type 378', 'class': 'Tactical'},
            'physical': {'mass': 42.8000, 'diam': 0.4280, 'ix': 0.04780},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_379'] = {
            'metadata': {'id': 379, 'name': 'Strategic Projectile Type 379', 'class': 'Tactical'},
            'physical': {'mass': 42.9000, 'diam': 0.4290, 'ix': 0.04790},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.2900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_380'] = {
            'metadata': {'id': 380, 'name': 'Strategic Projectile Type 380', 'class': 'Tactical'},
            'physical': {'mass': 43.0000, 'diam': 0.4300, 'ix': 0.04800},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_381'] = {
            'metadata': {'id': 381, 'name': 'Strategic Projectile Type 381', 'class': 'Tactical'},
            'physical': {'mass': 43.1000, 'diam': 0.4310, 'ix': 0.04810},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_382'] = {
            'metadata': {'id': 382, 'name': 'Strategic Projectile Type 382', 'class': 'Tactical'},
            'physical': {'mass': 43.2000, 'diam': 0.4320, 'ix': 0.04820},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_383'] = {
            'metadata': {'id': 383, 'name': 'Strategic Projectile Type 383', 'class': 'Tactical'},
            'physical': {'mass': 43.3000, 'diam': 0.4330, 'ix': 0.04830},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_384'] = {
            'metadata': {'id': 384, 'name': 'Strategic Projectile Type 384', 'class': 'Tactical'},
            'physical': {'mass': 43.4000, 'diam': 0.4340, 'ix': 0.04840},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_385'] = {
            'metadata': {'id': 385, 'name': 'Strategic Projectile Type 385', 'class': 'Tactical'},
            'physical': {'mass': 43.5000, 'diam': 0.4350, 'ix': 0.04850},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_386'] = {
            'metadata': {'id': 386, 'name': 'Strategic Projectile Type 386', 'class': 'Tactical'},
            'physical': {'mass': 43.6000, 'diam': 0.4360, 'ix': 0.04860},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_387'] = {
            'metadata': {'id': 387, 'name': 'Strategic Projectile Type 387', 'class': 'Tactical'},
            'physical': {'mass': 43.7000, 'diam': 0.4370, 'ix': 0.04870},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_388'] = {
            'metadata': {'id': 388, 'name': 'Strategic Projectile Type 388', 'class': 'Tactical'},
            'physical': {'mass': 43.8000, 'diam': 0.4380, 'ix': 0.04880},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_389'] = {
            'metadata': {'id': 389, 'name': 'Strategic Projectile Type 389', 'class': 'Tactical'},
            'physical': {'mass': 43.9000, 'diam': 0.4390, 'ix': 0.04890},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.3900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_390'] = {
            'metadata': {'id': 390, 'name': 'Strategic Projectile Type 390', 'class': 'Tactical'},
            'physical': {'mass': 44.0000, 'diam': 0.4400, 'ix': 0.04900},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_391'] = {
            'metadata': {'id': 391, 'name': 'Strategic Projectile Type 391', 'class': 'Tactical'},
            'physical': {'mass': 44.1000, 'diam': 0.4410, 'ix': 0.04910},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_392'] = {
            'metadata': {'id': 392, 'name': 'Strategic Projectile Type 392', 'class': 'Tactical'},
            'physical': {'mass': 44.2000, 'diam': 0.4420, 'ix': 0.04920},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_393'] = {
            'metadata': {'id': 393, 'name': 'Strategic Projectile Type 393', 'class': 'Tactical'},
            'physical': {'mass': 44.3000, 'diam': 0.4430, 'ix': 0.04930},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_394'] = {
            'metadata': {'id': 394, 'name': 'Strategic Projectile Type 394', 'class': 'Tactical'},
            'physical': {'mass': 44.4000, 'diam': 0.4440, 'ix': 0.04940},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_395'] = {
            'metadata': {'id': 395, 'name': 'Strategic Projectile Type 395', 'class': 'Tactical'},
            'physical': {'mass': 44.5000, 'diam': 0.4450, 'ix': 0.04950},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_396'] = {
            'metadata': {'id': 396, 'name': 'Strategic Projectile Type 396', 'class': 'Tactical'},
            'physical': {'mass': 44.6000, 'diam': 0.4460, 'ix': 0.04960},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_397'] = {
            'metadata': {'id': 397, 'name': 'Strategic Projectile Type 397', 'class': 'Tactical'},
            'physical': {'mass': 44.7000, 'diam': 0.4470, 'ix': 0.04970},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_398'] = {
            'metadata': {'id': 398, 'name': 'Strategic Projectile Type 398', 'class': 'Tactical'},
            'physical': {'mass': 44.8000, 'diam': 0.4480, 'ix': 0.04980},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_399'] = {
            'metadata': {'id': 399, 'name': 'Strategic Projectile Type 399', 'class': 'Tactical'},
            'physical': {'mass': 44.9000, 'diam': 0.4490, 'ix': 0.04990},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.4900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_400'] = {
            'metadata': {'id': 400, 'name': 'Strategic Projectile Type 400', 'class': 'Tactical'},
            'physical': {'mass': 45.0000, 'diam': 0.4500, 'ix': 0.05000},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_401'] = {
            'metadata': {'id': 401, 'name': 'Strategic Projectile Type 401', 'class': 'Tactical'},
            'physical': {'mass': 45.1000, 'diam': 0.4510, 'ix': 0.05010},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_402'] = {
            'metadata': {'id': 402, 'name': 'Strategic Projectile Type 402', 'class': 'Tactical'},
            'physical': {'mass': 45.2000, 'diam': 0.4520, 'ix': 0.05020},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_403'] = {
            'metadata': {'id': 403, 'name': 'Strategic Projectile Type 403', 'class': 'Tactical'},
            'physical': {'mass': 45.3000, 'diam': 0.4530, 'ix': 0.05030},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_404'] = {
            'metadata': {'id': 404, 'name': 'Strategic Projectile Type 404', 'class': 'Tactical'},
            'physical': {'mass': 45.4000, 'diam': 0.4540, 'ix': 0.05040},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_405'] = {
            'metadata': {'id': 405, 'name': 'Strategic Projectile Type 405', 'class': 'Tactical'},
            'physical': {'mass': 45.5000, 'diam': 0.4550, 'ix': 0.05050},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_406'] = {
            'metadata': {'id': 406, 'name': 'Strategic Projectile Type 406', 'class': 'Tactical'},
            'physical': {'mass': 45.6000, 'diam': 0.4560, 'ix': 0.05060},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_407'] = {
            'metadata': {'id': 407, 'name': 'Strategic Projectile Type 407', 'class': 'Tactical'},
            'physical': {'mass': 45.7000, 'diam': 0.4570, 'ix': 0.05070},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_408'] = {
            'metadata': {'id': 408, 'name': 'Strategic Projectile Type 408', 'class': 'Tactical'},
            'physical': {'mass': 45.8000, 'diam': 0.4580, 'ix': 0.05080},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_409'] = {
            'metadata': {'id': 409, 'name': 'Strategic Projectile Type 409', 'class': 'Tactical'},
            'physical': {'mass': 45.9000, 'diam': 0.4590, 'ix': 0.05090},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.5900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_410'] = {
            'metadata': {'id': 410, 'name': 'Strategic Projectile Type 410', 'class': 'Tactical'},
            'physical': {'mass': 46.0000, 'diam': 0.4600, 'ix': 0.05100},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_411'] = {
            'metadata': {'id': 411, 'name': 'Strategic Projectile Type 411', 'class': 'Tactical'},
            'physical': {'mass': 46.1000, 'diam': 0.4610, 'ix': 0.05110},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_412'] = {
            'metadata': {'id': 412, 'name': 'Strategic Projectile Type 412', 'class': 'Tactical'},
            'physical': {'mass': 46.2000, 'diam': 0.4620, 'ix': 0.05120},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_413'] = {
            'metadata': {'id': 413, 'name': 'Strategic Projectile Type 413', 'class': 'Tactical'},
            'physical': {'mass': 46.3000, 'diam': 0.4630, 'ix': 0.05130},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_414'] = {
            'metadata': {'id': 414, 'name': 'Strategic Projectile Type 414', 'class': 'Tactical'},
            'physical': {'mass': 46.4000, 'diam': 0.4640, 'ix': 0.05140},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_415'] = {
            'metadata': {'id': 415, 'name': 'Strategic Projectile Type 415', 'class': 'Tactical'},
            'physical': {'mass': 46.5000, 'diam': 0.4650, 'ix': 0.05150},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_416'] = {
            'metadata': {'id': 416, 'name': 'Strategic Projectile Type 416', 'class': 'Tactical'},
            'physical': {'mass': 46.6000, 'diam': 0.4660, 'ix': 0.05160},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_417'] = {
            'metadata': {'id': 417, 'name': 'Strategic Projectile Type 417', 'class': 'Tactical'},
            'physical': {'mass': 46.7000, 'diam': 0.4670, 'ix': 0.05170},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_418'] = {
            'metadata': {'id': 418, 'name': 'Strategic Projectile Type 418', 'class': 'Tactical'},
            'physical': {'mass': 46.8000, 'diam': 0.4680, 'ix': 0.05180},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_419'] = {
            'metadata': {'id': 419, 'name': 'Strategic Projectile Type 419', 'class': 'Tactical'},
            'physical': {'mass': 46.9000, 'diam': 0.4690, 'ix': 0.05190},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.6900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_420'] = {
            'metadata': {'id': 420, 'name': 'Strategic Projectile Type 420', 'class': 'Tactical'},
            'physical': {'mass': 47.0000, 'diam': 0.4700, 'ix': 0.05200},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_421'] = {
            'metadata': {'id': 421, 'name': 'Strategic Projectile Type 421', 'class': 'Tactical'},
            'physical': {'mass': 47.1000, 'diam': 0.4710, 'ix': 0.05210},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_422'] = {
            'metadata': {'id': 422, 'name': 'Strategic Projectile Type 422', 'class': 'Tactical'},
            'physical': {'mass': 47.2000, 'diam': 0.4720, 'ix': 0.05220},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_423'] = {
            'metadata': {'id': 423, 'name': 'Strategic Projectile Type 423', 'class': 'Tactical'},
            'physical': {'mass': 47.3000, 'diam': 0.4730, 'ix': 0.05230},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_424'] = {
            'metadata': {'id': 424, 'name': 'Strategic Projectile Type 424', 'class': 'Tactical'},
            'physical': {'mass': 47.4000, 'diam': 0.4740, 'ix': 0.05240},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_425'] = {
            'metadata': {'id': 425, 'name': 'Strategic Projectile Type 425', 'class': 'Tactical'},
            'physical': {'mass': 47.5000, 'diam': 0.4750, 'ix': 0.05250},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_426'] = {
            'metadata': {'id': 426, 'name': 'Strategic Projectile Type 426', 'class': 'Tactical'},
            'physical': {'mass': 47.6000, 'diam': 0.4760, 'ix': 0.05260},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_427'] = {
            'metadata': {'id': 427, 'name': 'Strategic Projectile Type 427', 'class': 'Tactical'},
            'physical': {'mass': 47.7000, 'diam': 0.4770, 'ix': 0.05270},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_428'] = {
            'metadata': {'id': 428, 'name': 'Strategic Projectile Type 428', 'class': 'Tactical'},
            'physical': {'mass': 47.8000, 'diam': 0.4780, 'ix': 0.05280},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_429'] = {
            'metadata': {'id': 429, 'name': 'Strategic Projectile Type 429', 'class': 'Tactical'},
            'physical': {'mass': 47.9000, 'diam': 0.4790, 'ix': 0.05290},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.7900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_430'] = {
            'metadata': {'id': 430, 'name': 'Strategic Projectile Type 430', 'class': 'Tactical'},
            'physical': {'mass': 48.0000, 'diam': 0.4800, 'ix': 0.05300},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_431'] = {
            'metadata': {'id': 431, 'name': 'Strategic Projectile Type 431', 'class': 'Tactical'},
            'physical': {'mass': 48.1000, 'diam': 0.4810, 'ix': 0.05310},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_432'] = {
            'metadata': {'id': 432, 'name': 'Strategic Projectile Type 432', 'class': 'Tactical'},
            'physical': {'mass': 48.2000, 'diam': 0.4820, 'ix': 0.05320},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_433'] = {
            'metadata': {'id': 433, 'name': 'Strategic Projectile Type 433', 'class': 'Tactical'},
            'physical': {'mass': 48.3000, 'diam': 0.4830, 'ix': 0.05330},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_434'] = {
            'metadata': {'id': 434, 'name': 'Strategic Projectile Type 434', 'class': 'Tactical'},
            'physical': {'mass': 48.4000, 'diam': 0.4840, 'ix': 0.05340},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_435'] = {
            'metadata': {'id': 435, 'name': 'Strategic Projectile Type 435', 'class': 'Tactical'},
            'physical': {'mass': 48.5000, 'diam': 0.4850, 'ix': 0.05350},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_436'] = {
            'metadata': {'id': 436, 'name': 'Strategic Projectile Type 436', 'class': 'Tactical'},
            'physical': {'mass': 48.6000, 'diam': 0.4860, 'ix': 0.05360},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_437'] = {
            'metadata': {'id': 437, 'name': 'Strategic Projectile Type 437', 'class': 'Tactical'},
            'physical': {'mass': 48.7000, 'diam': 0.4870, 'ix': 0.05370},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_438'] = {
            'metadata': {'id': 438, 'name': 'Strategic Projectile Type 438', 'class': 'Tactical'},
            'physical': {'mass': 48.8000, 'diam': 0.4880, 'ix': 0.05380},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_439'] = {
            'metadata': {'id': 439, 'name': 'Strategic Projectile Type 439', 'class': 'Tactical'},
            'physical': {'mass': 48.9000, 'diam': 0.4890, 'ix': 0.05390},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.8900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_440'] = {
            'metadata': {'id': 440, 'name': 'Strategic Projectile Type 440', 'class': 'Tactical'},
            'physical': {'mass': 49.0000, 'diam': 0.4900, 'ix': 0.05400},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_441'] = {
            'metadata': {'id': 441, 'name': 'Strategic Projectile Type 441', 'class': 'Tactical'},
            'physical': {'mass': 49.1000, 'diam': 0.4910, 'ix': 0.05410},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_442'] = {
            'metadata': {'id': 442, 'name': 'Strategic Projectile Type 442', 'class': 'Tactical'},
            'physical': {'mass': 49.2000, 'diam': 0.4920, 'ix': 0.05420},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_443'] = {
            'metadata': {'id': 443, 'name': 'Strategic Projectile Type 443', 'class': 'Tactical'},
            'physical': {'mass': 49.3000, 'diam': 0.4930, 'ix': 0.05430},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_444'] = {
            'metadata': {'id': 444, 'name': 'Strategic Projectile Type 444', 'class': 'Tactical'},
            'physical': {'mass': 49.4000, 'diam': 0.4940, 'ix': 0.05440},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_445'] = {
            'metadata': {'id': 445, 'name': 'Strategic Projectile Type 445', 'class': 'Tactical'},
            'physical': {'mass': 49.5000, 'diam': 0.4950, 'ix': 0.05450},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_446'] = {
            'metadata': {'id': 446, 'name': 'Strategic Projectile Type 446', 'class': 'Tactical'},
            'physical': {'mass': 49.6000, 'diam': 0.4960, 'ix': 0.05460},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_447'] = {
            'metadata': {'id': 447, 'name': 'Strategic Projectile Type 447', 'class': 'Tactical'},
            'physical': {'mass': 49.7000, 'diam': 0.4970, 'ix': 0.05470},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_448'] = {
            'metadata': {'id': 448, 'name': 'Strategic Projectile Type 448', 'class': 'Tactical'},
            'physical': {'mass': 49.8000, 'diam': 0.4980, 'ix': 0.05480},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_449'] = {
            'metadata': {'id': 449, 'name': 'Strategic Projectile Type 449', 'class': 'Tactical'},
            'physical': {'mass': 49.9000, 'diam': 0.4990, 'ix': 0.05490},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 5.9900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_450'] = {
            'metadata': {'id': 450, 'name': 'Strategic Projectile Type 450', 'class': 'Tactical'},
            'physical': {'mass': 50.0000, 'diam': 0.5000, 'ix': 0.05500},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_451'] = {
            'metadata': {'id': 451, 'name': 'Strategic Projectile Type 451', 'class': 'Tactical'},
            'physical': {'mass': 50.1000, 'diam': 0.5010, 'ix': 0.05510},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_452'] = {
            'metadata': {'id': 452, 'name': 'Strategic Projectile Type 452', 'class': 'Tactical'},
            'physical': {'mass': 50.2000, 'diam': 0.5020, 'ix': 0.05520},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_453'] = {
            'metadata': {'id': 453, 'name': 'Strategic Projectile Type 453', 'class': 'Tactical'},
            'physical': {'mass': 50.3000, 'diam': 0.5030, 'ix': 0.05530},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_454'] = {
            'metadata': {'id': 454, 'name': 'Strategic Projectile Type 454', 'class': 'Tactical'},
            'physical': {'mass': 50.4000, 'diam': 0.5040, 'ix': 0.05540},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_455'] = {
            'metadata': {'id': 455, 'name': 'Strategic Projectile Type 455', 'class': 'Tactical'},
            'physical': {'mass': 50.5000, 'diam': 0.5050, 'ix': 0.05550},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_456'] = {
            'metadata': {'id': 456, 'name': 'Strategic Projectile Type 456', 'class': 'Tactical'},
            'physical': {'mass': 50.6000, 'diam': 0.5060, 'ix': 0.05560},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_457'] = {
            'metadata': {'id': 457, 'name': 'Strategic Projectile Type 457', 'class': 'Tactical'},
            'physical': {'mass': 50.7000, 'diam': 0.5070, 'ix': 0.05570},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_458'] = {
            'metadata': {'id': 458, 'name': 'Strategic Projectile Type 458', 'class': 'Tactical'},
            'physical': {'mass': 50.8000, 'diam': 0.5080, 'ix': 0.05580},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_459'] = {
            'metadata': {'id': 459, 'name': 'Strategic Projectile Type 459', 'class': 'Tactical'},
            'physical': {'mass': 50.9000, 'diam': 0.5090, 'ix': 0.05590},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.0900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_460'] = {
            'metadata': {'id': 460, 'name': 'Strategic Projectile Type 460', 'class': 'Tactical'},
            'physical': {'mass': 51.0000, 'diam': 0.5100, 'ix': 0.05600},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_461'] = {
            'metadata': {'id': 461, 'name': 'Strategic Projectile Type 461', 'class': 'Tactical'},
            'physical': {'mass': 51.1000, 'diam': 0.5110, 'ix': 0.05610},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_462'] = {
            'metadata': {'id': 462, 'name': 'Strategic Projectile Type 462', 'class': 'Tactical'},
            'physical': {'mass': 51.2000, 'diam': 0.5120, 'ix': 0.05620},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_463'] = {
            'metadata': {'id': 463, 'name': 'Strategic Projectile Type 463', 'class': 'Tactical'},
            'physical': {'mass': 51.3000, 'diam': 0.5130, 'ix': 0.05630},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_464'] = {
            'metadata': {'id': 464, 'name': 'Strategic Projectile Type 464', 'class': 'Tactical'},
            'physical': {'mass': 51.4000, 'diam': 0.5140, 'ix': 0.05640},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_465'] = {
            'metadata': {'id': 465, 'name': 'Strategic Projectile Type 465', 'class': 'Tactical'},
            'physical': {'mass': 51.5000, 'diam': 0.5150, 'ix': 0.05650},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_466'] = {
            'metadata': {'id': 466, 'name': 'Strategic Projectile Type 466', 'class': 'Tactical'},
            'physical': {'mass': 51.6000, 'diam': 0.5160, 'ix': 0.05660},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_467'] = {
            'metadata': {'id': 467, 'name': 'Strategic Projectile Type 467', 'class': 'Tactical'},
            'physical': {'mass': 51.7000, 'diam': 0.5170, 'ix': 0.05670},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_468'] = {
            'metadata': {'id': 468, 'name': 'Strategic Projectile Type 468', 'class': 'Tactical'},
            'physical': {'mass': 51.8000, 'diam': 0.5180, 'ix': 0.05680},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_469'] = {
            'metadata': {'id': 469, 'name': 'Strategic Projectile Type 469', 'class': 'Tactical'},
            'physical': {'mass': 51.9000, 'diam': 0.5190, 'ix': 0.05690},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.1900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_470'] = {
            'metadata': {'id': 470, 'name': 'Strategic Projectile Type 470', 'class': 'Tactical'},
            'physical': {'mass': 52.0000, 'diam': 0.5200, 'ix': 0.05700},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_471'] = {
            'metadata': {'id': 471, 'name': 'Strategic Projectile Type 471', 'class': 'Tactical'},
            'physical': {'mass': 52.1000, 'diam': 0.5210, 'ix': 0.05710},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_472'] = {
            'metadata': {'id': 472, 'name': 'Strategic Projectile Type 472', 'class': 'Tactical'},
            'physical': {'mass': 52.2000, 'diam': 0.5220, 'ix': 0.05720},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_473'] = {
            'metadata': {'id': 473, 'name': 'Strategic Projectile Type 473', 'class': 'Tactical'},
            'physical': {'mass': 52.3000, 'diam': 0.5230, 'ix': 0.05730},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_474'] = {
            'metadata': {'id': 474, 'name': 'Strategic Projectile Type 474', 'class': 'Tactical'},
            'physical': {'mass': 52.4000, 'diam': 0.5240, 'ix': 0.05740},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_475'] = {
            'metadata': {'id': 475, 'name': 'Strategic Projectile Type 475', 'class': 'Tactical'},
            'physical': {'mass': 52.5000, 'diam': 0.5250, 'ix': 0.05750},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_476'] = {
            'metadata': {'id': 476, 'name': 'Strategic Projectile Type 476', 'class': 'Tactical'},
            'physical': {'mass': 52.6000, 'diam': 0.5260, 'ix': 0.05760},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_477'] = {
            'metadata': {'id': 477, 'name': 'Strategic Projectile Type 477', 'class': 'Tactical'},
            'physical': {'mass': 52.7000, 'diam': 0.5270, 'ix': 0.05770},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_478'] = {
            'metadata': {'id': 478, 'name': 'Strategic Projectile Type 478', 'class': 'Tactical'},
            'physical': {'mass': 52.8000, 'diam': 0.5280, 'ix': 0.05780},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_479'] = {
            'metadata': {'id': 479, 'name': 'Strategic Projectile Type 479', 'class': 'Tactical'},
            'physical': {'mass': 52.9000, 'diam': 0.5290, 'ix': 0.05790},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.2900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_480'] = {
            'metadata': {'id': 480, 'name': 'Strategic Projectile Type 480', 'class': 'Tactical'},
            'physical': {'mass': 53.0000, 'diam': 0.5300, 'ix': 0.05800},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_481'] = {
            'metadata': {'id': 481, 'name': 'Strategic Projectile Type 481', 'class': 'Tactical'},
            'physical': {'mass': 53.1000, 'diam': 0.5310, 'ix': 0.05810},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_482'] = {
            'metadata': {'id': 482, 'name': 'Strategic Projectile Type 482', 'class': 'Tactical'},
            'physical': {'mass': 53.2000, 'diam': 0.5320, 'ix': 0.05820},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_483'] = {
            'metadata': {'id': 483, 'name': 'Strategic Projectile Type 483', 'class': 'Tactical'},
            'physical': {'mass': 53.3000, 'diam': 0.5330, 'ix': 0.05830},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_484'] = {
            'metadata': {'id': 484, 'name': 'Strategic Projectile Type 484', 'class': 'Tactical'},
            'physical': {'mass': 53.4000, 'diam': 0.5340, 'ix': 0.05840},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_485'] = {
            'metadata': {'id': 485, 'name': 'Strategic Projectile Type 485', 'class': 'Tactical'},
            'physical': {'mass': 53.5000, 'diam': 0.5350, 'ix': 0.05850},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_486'] = {
            'metadata': {'id': 486, 'name': 'Strategic Projectile Type 486', 'class': 'Tactical'},
            'physical': {'mass': 53.6000, 'diam': 0.5360, 'ix': 0.05860},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_487'] = {
            'metadata': {'id': 487, 'name': 'Strategic Projectile Type 487', 'class': 'Tactical'},
            'physical': {'mass': 53.7000, 'diam': 0.5370, 'ix': 0.05870},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_488'] = {
            'metadata': {'id': 488, 'name': 'Strategic Projectile Type 488', 'class': 'Tactical'},
            'physical': {'mass': 53.8000, 'diam': 0.5380, 'ix': 0.05880},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_489'] = {
            'metadata': {'id': 489, 'name': 'Strategic Projectile Type 489', 'class': 'Tactical'},
            'physical': {'mass': 53.9000, 'diam': 0.5390, 'ix': 0.05890},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.3900, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_490'] = {
            'metadata': {'id': 490, 'name': 'Strategic Projectile Type 490', 'class': 'Tactical'},
            'physical': {'mass': 54.0000, 'diam': 0.5400, 'ix': 0.05900},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4000, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_491'] = {
            'metadata': {'id': 491, 'name': 'Strategic Projectile Type 491', 'class': 'Tactical'},
            'physical': {'mass': 54.1000, 'diam': 0.5410, 'ix': 0.05910},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4100, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_492'] = {
            'metadata': {'id': 492, 'name': 'Strategic Projectile Type 492', 'class': 'Tactical'},
            'physical': {'mass': 54.2000, 'diam': 0.5420, 'ix': 0.05920},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4200, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_493'] = {
            'metadata': {'id': 493, 'name': 'Strategic Projectile Type 493', 'class': 'Tactical'},
            'physical': {'mass': 54.3000, 'diam': 0.5430, 'ix': 0.05930},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4300, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_494'] = {
            'metadata': {'id': 494, 'name': 'Strategic Projectile Type 494', 'class': 'Tactical'},
            'physical': {'mass': 54.4000, 'diam': 0.5440, 'ix': 0.05940},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4400, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_495'] = {
            'metadata': {'id': 495, 'name': 'Strategic Projectile Type 495', 'class': 'Tactical'},
            'physical': {'mass': 54.5000, 'diam': 0.5450, 'ix': 0.05950},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4500, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_496'] = {
            'metadata': {'id': 496, 'name': 'Strategic Projectile Type 496', 'class': 'Tactical'},
            'physical': {'mass': 54.6000, 'diam': 0.5460, 'ix': 0.05960},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4600, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_497'] = {
            'metadata': {'id': 497, 'name': 'Strategic Projectile Type 497', 'class': 'Tactical'},
            'physical': {'mass': 54.7000, 'diam': 0.5470, 'ix': 0.05970},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4700, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_498'] = {
            'metadata': {'id': 498, 'name': 'Strategic Projectile Type 498', 'class': 'Tactical'},
            'physical': {'mass': 54.8000, 'diam': 0.5480, 'ix': 0.05980},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4800, 'frag_constant': 0.05}
        }

        cls.ASSETS['Asset_499'] = {
            'metadata': {'id': 499, 'name': 'Strategic Projectile Type 499', 'class': 'Tactical'},
            'physical': {'mass': 54.9000, 'diam': 0.5490, 'ix': 0.05990},
            'aero': {'cd0': 0.15, 'cla': 2.5, 'clp': -0.015, 'cmag': -0.08},
            'lethality': {'explosive_mass': 6.4900, 'frag_constant': 0.05}
        }

StrategicAssetDatabaseV2.initialize_strategic_database()
