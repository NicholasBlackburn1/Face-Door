
cmake_minimum_required(VERSION 3.0)

# Name of our Project
project(FaceDoor)

find_package( OpenCV REQUIRED )

MESSAGE(STATUS "Include dirs ${OpenCV_INCLUDE_DIRS}")
MESSAGE(STATUS "LINK LIBRARIES ${OpenCV_LIBS}")

add_executable(FaceDoor
  src/main.cpp)
  target_link_libraries(FaceDoor ${OpenCV_LIBS})
