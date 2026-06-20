# Install script for directory: /mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "default")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-core-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-core-default.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-core-default.so"
         RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/lib/libns3.40-core-default.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-core-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-core-default.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-core-default.so"
         OLD_RPATH "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/lib:"
         NEW_RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-core-default.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ns3" TYPE FILE FILES
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/int64x64-128.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/example-as-test.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/helper/csv-reader.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/helper/event-garbage-collector.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/helper/random-variable-stream-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/abort.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/ascii-file.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/ascii-test.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/assert.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/attribute-accessor-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/attribute-construction-list.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/attribute-container.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/attribute-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/attribute.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/boolean.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/breakpoint.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/build-profile.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/calendar-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/callback.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/command-line.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/config.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/default-deleter.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/default-simulator-impl.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/deprecated.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/des-metrics.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/double.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/enum.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/event-id.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/event-impl.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/fatal-error.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/fatal-impl.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/fd-reader.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/environment-variable.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/global-value.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/hash-fnv.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/hash-function.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/hash-murmur3.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/hash.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/heap-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/int-to-type.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/int64x64-double.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/int64x64.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/integer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/length.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/list-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/log-macros-disabled.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/log-macros-enabled.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/log.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/make-event.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/map-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/math.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/names.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/node-printer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/nstime.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/object-base.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/object-factory.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/object-map.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/object-ptr-container.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/object-vector.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/object.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/pair.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/pointer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/priority-queue-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/ptr.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/random-variable-stream.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/rng-seed-manager.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/rng-stream.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/show-progress.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/simple-ref-count.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/simulation-singleton.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/simulator-impl.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/simulator.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/singleton.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/string.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/synchronizer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/system-path.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/system-wall-clock-ms.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/system-wall-clock-timestamp.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/test.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/time-printer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/timer-impl.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/timer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/trace-source-accessor.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/traced-callback.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/traced-value.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/trickle-timer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/tuple.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/type-id.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/type-name.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/type-traits.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/uinteger.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/unused.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/valgrind.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/vector.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/warnings.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/watchdog.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/realtime-simulator-impl.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/wall-clock-synchronizer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/val-array.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/core/model/matrix-array.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/include/ns3/config-store-config.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/include/ns3/core-config.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/include/ns3/core-module.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/cmake-cache/src/core/examples/cmake_install.cmake")

endif()

