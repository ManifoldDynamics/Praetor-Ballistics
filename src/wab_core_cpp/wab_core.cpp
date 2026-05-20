#include "wab_core.h"
#include <cmath>

extern "C" {

WAB_EXPORT void InitializeIDMKernel(
    const WeaponParams* wp,
    const AmmoParams* ammo,
    uint32_t index,
    WAB_State* state)
{
    if (!wp || !ammo || !state || index >= state->count) return;

    float bore_vol = wp->bore_area * wp->barrel_len;
    float deterministic_work = ammo->w_idm_plateau * bore_vol;

    // Protect against division by zero or negative sqrt
    if (ammo->mass <= 0.0f || deterministic_work < 0.0f) return;

    float exit_vel = std::sqrt((2.0f * deterministic_work * WAB_EFF) / ammo->mass);

    state->velocity_x[index] = wp->muzzle_vec_x * exit_vel;
    state->velocity_y[index] = wp->muzzle_vec_y * exit_vel;
    state->velocity_z[index] = wp->muzzle_vec_z * exit_vel;

    // Avoid division by zero
    if (wp->twist_rate != 0.0f) {
        state->spin_rate[index] = exit_vel / wp->twist_rate;
    } else {
        state->spin_rate[index] = 0.0f;
    }
}

WAB_EXPORT void ComputeWABDragTensor(WAB_State* state)
{
    if (!state) return;

    // Constants from the Continuance Tensor equation
    const float SOUND = 343.0f; // Speed of sound (m/s)
    const float M_CRIT = 0.85f;
    const float W_PSI = 1.2f;
    const float W_ALPHA = 5.0f;
    const float W_GAMMA = 0.1f;
    const float C_BASE = 0.15f;

    // Process the SoA massively in parallel (eventually SIMD)
    for (uint32_t i = 0; i < state->count; ++i) {

        float vx = state->velocity_x[i];
        float vy = state->velocity_y[i];
        float vz = state->velocity_z[i];

        float velocity_mag = std::sqrt(vx*vx + vy*vy + vz*vz);
        float mach = velocity_mag / SOUND;

        float wave_drag = W_PSI * std::tanh(W_ALPHA * (mach - M_CRIT));

        // Prevent division by zero
        float temp = state->temperature[i] > 0.01f ? state->temperature[i] : 0.01f;
        float spin = state->spin_rate[i] > 0.01f ? state->spin_rate[i] : 0.01f;

        float thermal_mod = std::exp(-W_GAMMA / (temp * spin));

        state->c_d[i] = C_BASE + (wave_drag * thermal_mod);
    }
}

} // extern "C"
