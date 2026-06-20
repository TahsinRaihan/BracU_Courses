# Install script for directory: /mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-lte-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-lte-default.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-lte-default.so"
         RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/lib/libns3.40-lte-default.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-lte-default.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-lte-default.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-lte-default.so"
         OLD_RPATH "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/lib:"
         NEW_RPATH "/usr/local/lib:$ORIGIN/:$ORIGIN/../lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libns3.40-lte-default.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ns3" TYPE FILE FILES
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/emu-epc-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/cc-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/epc-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/lte-global-pathloss-database.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/lte-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/lte-hex-grid-enb-topology-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/lte-stats-calculator.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/mac-stats-calculator.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/no-backhaul-epc-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/phy-rx-stats-calculator.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/phy-stats-calculator.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/phy-tx-stats-calculator.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/point-to-point-epc-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/radio-bearer-stats-calculator.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/radio-bearer-stats-connector.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/helper/radio-environment-map-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/a2-a4-rsrq-handover-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/a3-rsrp-handover-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/component-carrier-enb.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/component-carrier-ue.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/component-carrier.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/cqa-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-enb-application.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-enb-s1-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-gtpc-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-gtpu-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-mme-application.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-pgw-application.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-s11-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-s1ap-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-sgw-application.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-tft-classifier.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-tft.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-ue-nas.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-x2-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-x2-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/epc-x2.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/eps-bearer-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/eps-bearer.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/fdbet-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/fdmt-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/fdtbfq-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/ff-mac-common.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/ff-mac-csched-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/ff-mac-sched-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-amc.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-anr-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-anr.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-as-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-asn1-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ccm-mac-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ccm-rrc-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-chunk-processor.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-common.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-control-messages.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-cmac-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-component-carrier-manager.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-cphy-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-mac.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-net-device.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-phy-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-phy.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-enb-rrc.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ffr-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ffr-distributed-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ffr-enhanced-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ffr-rrc-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ffr-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ffr-soft-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-fr-hard-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-fr-no-op-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-fr-soft-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-fr-strict-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-handover-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-handover-management-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-harq-phy.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-interference.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-mac-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-mi-error-model.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-net-device.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-pdcp-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-pdcp-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-pdcp-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-pdcp.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-phy-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-phy.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-radio-bearer-info.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-radio-bearer-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-am-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-am.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-sdu-status-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-sequence-number.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-tag.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-tm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc-um.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rlc.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rrc-header.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rrc-protocol-ideal.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rrc-protocol-real.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-rrc-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-spectrum-phy.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-spectrum-signal-parameters.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-spectrum-value-helper.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-ccm-rrc-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-cmac-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-component-carrier-manager.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-cphy-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-mac.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-net-device.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-phy-sap.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-phy.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-power-control.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-ue-rrc.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/lte-vendor-specific-parameters.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/no-op-component-carrier-manager.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/no-op-handover-algorithm.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/pf-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/pss-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/rem-spectrum-phy.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/rr-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/simple-ue-component-carrier-manager.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/tdbet-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/tdmt-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/tdtbfq-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/src/lte/model/tta-ff-mac-scheduler.h"
    "/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/build/include/ns3/lte-module.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/mnt/e/Fall 25/CSE 421- Aktd/Lab/lab 2/ns-allinone-3.40/ns-allinone-3.40/ns-3.40/cmake-cache/src/lte/examples/cmake_install.cmake")

endif()

