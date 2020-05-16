cmake_minimum_required(VERSION 3.11)

project(zerokeys)

find_package(SDL2 REQUIRED)

add_executable(server main.cpp)
target_include_directories(server
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../third_party/asio/include)
target_link_libraries(server pthread)
