import numpy as np
from scipy.special import erfc

class DatalinkModelV2:
    """
    V2 Proprietary Datalink & Communication Engine.

    Implements:
    - Signal-to-Noise-and-Interference Ratio (SNIR) modeling.
    - Bit Error Rate (BER) for various modulations (BPSK, QAM).
    - Electronic Counter-Measures (ECM): Jamming power and effective range.
    - Link Budget: Antenna gains, Path loss (Free-space + Atmospheric).
    """
    def __init__(self, transmit_power_w=10.0, carrier_freq_hz=2.4e9):
        self.p_tx = transmit_power_w
        self.freq = carrier_freq_hz
        self.c = 3e8

    def calculate_path_loss(self, distance_m, atmospheric_extinction_db_km=0.1):
        """
        Calculates total path loss in dB.
        L = 20*log10(4*pi*d/lambda) + L_atm
        """
        wavelength = self.c / self.freq
        if distance_m < 1.0: distance_m = 1.0

        fspl = 20.0 * np.log10(4.0 * np.pi * distance_m / wavelength)
        atm_loss = (atmospheric_extinction_db_km / 1000.0) * distance_m

        return fspl + atm_loss

    def calculate_snir(self, distance_m, g_tx_db=10.0, g_rx_db=3.0, noise_floor_dbm=-100.0, jammer_params=None):
        """
        Calculates Signal-to-Noise-and-Interference Ratio at the receiver.
        """
        # Signal Power at Rx (dBm)
        p_tx_dbm = 10.0 * np.log10(self.p_tx * 1000.0)
        p_rx_dbm = p_tx_dbm + g_tx_db + g_rx_db - self.calculate_path_loss(distance_m)

        # Interference Power (Jamming)
        p_jam_w = 0.0
        if jammer_params:
            d_jam = jammer_params.get('distance_m', 5000.0)
            p_j_tx = jammer_params.get('power_w', 100.0)
            g_j_tx = jammer_params.get('gain_db', 15.0)
            l_jam = self.calculate_path_loss(d_jam)
            p_jam_dbm = 10.0 * np.log10(p_j_tx * 1000.0) + g_j_tx + g_rx_db - l_jam
            p_jam_w = 10.0**(p_jam_dbm / 10.0) / 1000.0

        p_noise_w = 10.0**(noise_floor_dbm / 10.0) / 1000.0
        p_rx_w = 10.0**(p_rx_dbm / 10.0) / 1000.0

        snir = p_rx_w / (p_noise_w + p_jam_w)
        return snir

    @staticmethod
    def calculate_ber_bpsk(snir_linear):
        """
        Calculates BER for BPSK modulation.
        BER = 0.5 * erfc(sqrt(Eb/N0))
        """
        return 0.5 * erfc(np.sqrt(snir_linear))

    def check_link_availability(self, distance_m, ber_threshold=1e-3, jammer_params=None):
        """
        Returns True if link is operational.
        """
        snir = self.calculate_snir(distance_m, jammer_params=jammer_params)
        ber = self.calculate_ber_bpsk(snir)
        return ber < ber_threshold
