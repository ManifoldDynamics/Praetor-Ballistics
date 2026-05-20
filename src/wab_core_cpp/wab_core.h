#pragma once

#include <cstdint>

// Export macro for cross-platform C-API
#if defined(_WIN32) || defined(_WIN64)
    #define WAB_EXPORT __declspec(dllexport)
#else
    #define WAB_EXPORT __attribute__((visibility("default")))
#endif

extern "C" {

// Data-Oriented Design (DOD): Struct of Arrays (SoA) layout for WAB State
// This ensures contiguous memory access, crucial for SIMD/AVX vectorization.
// In C#, this will map to blittable arrays via P/Invoke.

struct WAB_State {
    // Array sizes (must be equal for all arrays)
    uint32_t count;

    // Pointers to contiguous arrays of data
    float* position_x;
    float* position_y;
    float* position_z;

    float* velocity_x;
    float* velocity_y;
    float* velocity_z;

    float* spin_rate;
    float* temperature; // T_skin
    float* mass;
    float* diameter;

    // Derived/Computed values
    float* wave_drag;
    float* c_d;         // Coefficient of Drag
};

// Weapon and Ammo parameters for Initialization
struct WeaponParams {
    float muzzle_vec_x;
    float muzzle_vec_y;
    float muzzle_vec_z;
    float bore_area;
    float barrel_len;
    float twist_rate;
};

struct AmmoParams {
    float mass;
    float w_idm_plateau; // Wilson Deflagration Matrix Plateau
};

// Core Constants
const float WAB_EFF = 0.85f; // Efficiency factor

// C-API Endpoint Declarations

// Initialize a single projectile state based on weapon/ammo params
// Note: Realistically, this would initialize a block in the SoA, but
// matching the user's screenshot signature for the initial proof of concept.
WAB_EXPORT void InitializeIDMKernel(
    const WeaponParams* wp,
    const AmmoParams* ammo,
    uint32_t index,
    WAB_State* state);

// Compute the WAB drag tensor for all active projectiles in the SoA
WAB_EXPORT void ComputeWABDragTensor(WAB_State* state);

} // extern "C"
