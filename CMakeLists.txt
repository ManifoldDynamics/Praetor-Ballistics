cmake_minimum_required(VERSION 3.20)
project(WAB_Engine VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF) # Strict C++20, no OS-specific compiler extensions

# Add subdirectories
add_subdirectory(src/wab_core_cpp)
