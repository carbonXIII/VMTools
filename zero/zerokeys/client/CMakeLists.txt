cmake_minimum_required(VERSION 3.11)

project(zerokeys)

set(CMAKE_CXX_STANDARD 17)

find_package(SDL2 REQUIRED)

add_executable(client main.cpp)
target_include_directories(client
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../third_party/asio/include)
target_link_libraries(client pthread SDL2)
