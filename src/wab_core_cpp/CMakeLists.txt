cmake_minimum_required(VERSION 3.20)
project(wab_core_cpp LANGUAGES CXX)

# We are building a shared library (DLL / SO)
add_library(wab_core_cpp SHARED wab_core.cpp)

# Position independent code is required for shared libraries
set_target_properties(wab_core_cpp PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Note: We will add SIMD flags later based on the compiler
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # For now, let's enable basic optimizations and warnings
    target_compile_options(wab_core_cpp PRIVATE -Wall -Wextra -O3)
elseif(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
    target_compile_options(wab_core_cpp PRIVATE /W4 /O2)
endif()
