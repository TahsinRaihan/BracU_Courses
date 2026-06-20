# Install script for directory: /mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-network-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-network-default.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-network-default.so"
         RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/lib/libns3.40-network-default.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-network-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-network-default.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-network-default.so"
         OLD_RPATH "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/lib:"
         NEW_RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-network-default.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ns3" TYPE FILE FILES
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/helper/application-container.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/helper/delay-jitter-estimation.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/helper/net-device-container.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/helper/node-container.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/helper/packet-socket-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/helper/simple-net-device-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/helper/trace-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/application.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/buffer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/byte-tag-list.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/channel-list.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/channel.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/chunk.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/net-device.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/nix-vector.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/node-list.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/node.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/packet-metadata.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/packet-tag-list.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/packet.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/socket-factory.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/socket.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/tag-buffer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/model/trailer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/test/header-serialization-test.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/address-utils.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/bit-deserializer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/bit-serializer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/crc32.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/data-rate.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/drop-tail-queue.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/dynamic-queue-limits.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/error-channel.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/error-model.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/ethernet-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/ethernet-trailer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/flow-id-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/generic-phy.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/inet-socket-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/inet6-socket-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/ipv4-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/ipv6-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/llc-snap-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/lollipop-counter.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/mac16-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/mac48-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/mac64-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/mac8-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/net-device-queue-interface.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/output-stream-wrapper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-burst.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-data-calculators.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-probe.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-socket-address.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-socket-client.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-socket-factory.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-socket-server.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packet-socket.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/packetbb.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/pcap-file-wrapper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/pcap-file.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/pcap-test.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/queue-fwd.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/queue-item.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/queue-limits.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/queue-size.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/queue.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/radiotap-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/sequence-number.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/simple-channel.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/simple-net-device.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/sll-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/network/utils/timestamp-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/include/ns3/network-module.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/cmake-cache/src/network/examples/cmake_install.cmake")

endif()

