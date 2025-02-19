/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */

// Copyright (c) 2019 Centre Tecnologic de Telecomunicacions de Catalunya (CTTC)
//
// SPDX-License-Identifier: GPL-2.0-only

/**
 * \file cttc-3gpp-channel-example.cc
 * \ingroup examples
 * \brief Channel Example
 *
 * This example describes how to setup a simulation using the 3GPP channel model
 * from TR 38.901. Topology consists by default of 2 UEs and 2 gNbs, and can be
 * configured to be either mobile or static scenario.
 *
 * The output of this example are default NR trace files that can be found in
 * the root ns-3 project folder.
 */

#include "ns3/applications-module.h"
#include "ns3/config-store.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/log.h"
#include "ns3/mobility-module.h"
#include "ns3/nr-helper.h"
#include "ns3/nr-mac-scheduler-tdma-rr.h"
#include "ns3/nr-module.h"
#include "ns3/nr-point-to-point-epc-helper.h"
#include "ns3/point-to-point-helper.h"
#include <ns3/antenna-module.h>
#include <ns3/buildings-helper.h>
#include <fstream>

using namespace ns3;
std::ofstream outputFile; // Declaração do arquivo de saída


void MonitorarPosicaoEnb(Ptr<Node> enbNode) {
    double tempo = Simulator::Now().GetSeconds();
    Vector posicao = enbNode->GetObject<MobilityModel>()->GetPosition();
    outputFile << tempo<<"s"<<",ENb," << posicao.x << "," << posicao.y << std::endl;
    Simulator::Schedule(Seconds(0.1), &MonitorarPosicaoEnb, enbNode);
}

int
main(int argc, char* argv[])
{      
Time::SetResolution(Time::NS);


    outputFile.open("waypoint_positions.txt");
    if (!outputFile.is_open()) {
        NS_LOG_UNCOND("Erro ao abrir o arquivo de saída.");
        return 1;
    }
    double frequency = 3.5e9;      // central frequency
    double bandwidth = 200e6;     // bandwidth    // whether to enable mobility
    double simTime = 100;           // in second
    bool logging = true; // whether to enable logging from the simulation, another option is by                  // exporting the NS_LOG environment variable
    double hBS = 25;          // base station antenna height in meters
    double hUT = 1.5;
              // user antenna height in meters
    double txPower = 40; // txPower
    enum BandwidthPartInfo::Scenario scenarioEnum = BandwidthPartInfo::UMa;
    CommandLine cmd(__FILE__);
    cmd.AddValue("frequency", "The central carrier frequency in Hz.", frequency);
    cmd.AddValue("logging","If set to 0, log components will be disabled.", logging);
    cmd.Parse(argc, argv);

    // enable logging
    if (logging)
    {
        LogComponentEnable ("ThreeGppSpectrumPropagationLossModel", LOG_LEVEL_ALL);
        LogComponentEnable("ThreeGppPropagationLossModel", LOG_LEVEL_ALL);
        // LogComponentEnable ("ThreeGppChannelModel", LOG_LEVEL_ALL);
        // LogComponentEnable ("ChannelConditionModel", LOG_LEVEL_ALL);
        //LogComponentEnable ("UdpClient", LOG_LEVEL_INFO);
        //LogComponentEnable ("UdpServer", LOG_LEVEL_INFO);
        // LogComponentEnable ("LteRlcUm", LOG_LEVEL_LOGIC);
        // LogComponentEnable ("LtePdcp", LOG_LEVEL_INFO);
    }

    /*
     * Default values for the simulation. We are progressively removing all
     * the instances of SetDefault, but we need it for legacy code (LTE)
     */

    Config::SetDefault("ns3::LteRlcUm::MaxTxBufferSize", UintegerValue(999999999));
    
        scenarioEnum = BandwidthPartInfo::UMa;

    // create base stations and mobile terminals
    NodeContainer enbNodes;
    NodeContainer ueNodes;
    enbNodes.Create(4);
    ueNodes.Create(20);

    Ptr<ListPositionAllocator> enbPositionAlloc = CreateObject<ListPositionAllocator>();
    
    MobilityHelper enbMobility;
    enbMobility.SetMobilityModel("ns3::WaypointMobilityModel");
    enbMobility.Install(enbNodes);

    Ptr<WaypointMobilityModel> mob0 = enbNodes.Get(0)->GetObject<WaypointMobilityModel>();
    mob0->AddWaypoint(Waypoint(Seconds(0),Vector(0,50,hBS)));
    mob0->AddWaypoint(Waypoint(Seconds(100),Vector(95.5,247.6,hBS)));

    Ptr<WaypointMobilityModel> mob1 = enbNodes.Get(1)->GetObject<WaypointMobilityModel>();
    mob1->AddWaypoint(Waypoint(Seconds(0),Vector(0,500,hBS)));
    mob1->AddWaypoint(Waypoint(Seconds(100),Vector(144,346,hBS)));

    
    Ptr<WaypointMobilityModel> mob2 = enbNodes.Get(2)->GetObject<WaypointMobilityModel>();
    mob2->AddWaypoint(Waypoint(Seconds(0),Vector(500,500,hBS)));
    mob2->AddWaypoint(Waypoint(Seconds(100),Vector(372.4,275.4,hBS)));

    Ptr<WaypointMobilityModel> mob3 = enbNodes.Get(3)->GetObject<WaypointMobilityModel>();
    mob3->AddWaypoint(Waypoint(Seconds(0),Vector(500,50,hBS)));
    mob3->AddWaypoint(Waypoint(Seconds(100),Vector(388,181,hBS)));

    // position the mobile terminals and enable the mobility
    MobilityHelper uemobility;
    uemobility.SetMobilityModel("ns3::ConstantVelocityMobilityModel");
    uemobility.Install(ueNodes);

        ueNodes.Get(0)->GetObject<MobilityModel>()->SetPosition(
            Vector(294.07,428.81, hUT)); // (x, y, z) in m
        ueNodes.Get(0)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(1)->GetObject<MobilityModel>()->SetPosition(
            Vector(448.86,474.89, hUT)); // (x, y, z) in m
        ueNodes.Get(1)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(2)->GetObject<MobilityModel>()->SetPosition(
            Vector(445.77,280.84, hUT)); // (x, y, z) in m
        ueNodes.Get(2)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(3)->GetObject<MobilityModel>()->SetPosition(
            Vector(407.92,89.39, hUT)); // (x, y, z) in m
        ueNodes.Get(3)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(4)->GetObject<MobilityModel>()->SetPosition(
            Vector(17.94,385.13, hUT)); // (x, y, z) in m
        ueNodes.Get(4)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(5)->GetObject<MobilityModel>()->SetPosition(
            Vector(345.88,246.19, hUT)); // (x, y, z) in m
        ueNodes.Get(5)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(6)->GetObject<MobilityModel>()->SetPosition(
            Vector(189.34,315.63, hUT)); // (x, y, z) in m
        ueNodes.Get(6)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(7)->GetObject<MobilityModel>()->SetPosition(
            Vector(259.26,419.75, hUT)); // (x, y, z) in m
        ueNodes.Get(7)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(8)->GetObject<MobilityModel>()->SetPosition(
            Vector(328.98,230.52, hUT)); // (x, y, z) in m
        ueNodes.Get(8)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(9)->GetObject<MobilityModel>()->SetPosition(
            Vector(96.93,248.97, hUT)); // (x, y, z) in m
        ueNodes.Get(9)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis
            
        ueNodes.Get(10)->GetObject<MobilityModel>()->SetPosition(
            Vector(136.16,339.71, hUT)); // (x, y, z) in m
        ueNodes.Get(10)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis
    
        ueNodes.Get(11)->GetObject<MobilityModel>()->SetPosition(
            Vector(359.3,325.39,hUT)); // (x, y, z) in m
        ueNodes.Get(11)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(12)->GetObject<MobilityModel>()->SetPosition(
            Vector(391.5,134.4, hUT)); // (x, y, z) in m
        ueNodes.Get(12)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(13)->GetObject<MobilityModel>()->SetPosition(
            Vector(425.16,33.66, hUT)); // (x, y, z) in m
        ueNodes.Get(13)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(14)->GetObject<MobilityModel>()->SetPosition(
            Vector(387.62,385.72, hUT)); // (x, y, z) in m
        ueNodes.Get(14)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(15)->GetObject<MobilityModel>()->SetPosition(
            Vector(18.33,240.49, hUT)); // (x, y, z) in m
        ueNodes.Get(15)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(16)->GetObject<MobilityModel>()->SetPosition(
            Vector(58.35,164.6, hUT)); // (x, y, z) in m
        ueNodes.Get(16)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(17)->GetObject<MobilityModel>()->SetPosition(
            Vector(375.64,255.32, hUT)); // (x, y, z) in m
        ueNodes.Get(17)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(18)->GetObject<MobilityModel>()->SetPosition(
            Vector(119.61,131.81, hUT)); // (x, y, z) in m
        ueNodes.Get(18)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

        ueNodes.Get(19)->GetObject<MobilityModel>()->SetPosition(
            Vector(127.4,155.26, hUT)); // (x, y, z) in m
        ueNodes.Get(19)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(
            Vector(0, 0, 0)); // move UE1 along the y axis

    Ptr<NrPointToPointEpcHelper> epcHelper = CreateObject<NrPointToPointEpcHelper>();
    Ptr<IdealBeamformingHelper> idealBeamformingHelper = CreateObject<IdealBeamformingHelper>();
    Ptr<NrHelper> nrHelper = CreateObject<NrHelper>();
    nrHelper->SetBeamformingHelper(idealBeamformingHelper);
    nrHelper->SetEpcHelper(epcHelper);

    /*
     * Spectrum configuration. We create a single operational band and configure the scenario.
     */
    BandwidthPartInfoPtrVector allBwps;
    CcBwpCreator ccBwpCreator;
    const uint8_t numCcPerBand = 1; // in this example we have a single band, and that band is
                                    // composed of a single component carrier

    /* Create the configuration for the CcBwpHelper. SimpleOperationBandConf creates
     * a single BWP per CC and a single BWP in CC.
     *
     * Hence, the configured spectrum is:
     *
     * |---------------Band---------------|
     * |---------------CC-----------------|
     * |---------------BWP----------------|
     */
    CcBwpCreator::SimpleOperationBandConf bandConf(frequency,
                                                   bandwidth,
                                                   numCcPerBand,
                                                   scenarioEnum);
    OperationBandInfo band = ccBwpCreator.CreateOperationBandContiguousCc(bandConf);
    // Initialize channel and pathloss, plus other things inside band.
    nrHelper->InitializeOperationBand(&band);
    allBwps = CcBwpCreator::GetAllBwps({band});

    // Configure ideal beamforming method
    idealBeamformingHelper->SetAttribute("BeamformingMethod",
                                         TypeIdValue(DirectPathBeamforming::GetTypeId()));

    // Configure scheduler
    nrHelper->SetSchedulerTypeId(NrMacSchedulerTdmaRR::GetTypeId());

    // Antennas for the UEs
    nrHelper->SetUeAntennaAttribute("NumRows", UintegerValue(4));
    nrHelper->SetUeAntennaAttribute("NumColumns", UintegerValue(4));
    nrHelper->SetUeAntennaAttribute("AntennaElement",
                                    PointerValue(CreateObject<IsotropicAntennaModel>()));

    // Antennas for the gNbs
    nrHelper->SetGnbAntennaAttribute("NumRows", UintegerValue(8));
    nrHelper->SetGnbAntennaAttribute("NumColumns", UintegerValue(8));
    nrHelper->SetGnbAntennaAttribute("AntennaElement",
                                     PointerValue(CreateObject<IsotropicAntennaModel>()));

    // install nr net devices
    NetDeviceContainer enbNetDev = nrHelper->InstallGnbDevice(enbNodes, allBwps);
    NetDeviceContainer ueNetDev = nrHelper->InstallUeDevice(ueNodes, allBwps);

    int64_t randomStream = 1;
    randomStream += nrHelper->AssignStreams(enbNetDev, randomStream);
    randomStream += nrHelper->AssignStreams(ueNetDev, randomStream);

    for (uint32_t i = 0; i < enbNetDev.GetN(); ++i)
    {
    nrHelper->GetGnbPhy(enbNetDev.Get(i), 0)->SetTxPower(txPower);
    }
    // When all the configuration is done, explicitly call UpdateConfig ()
    for (auto it = enbNetDev.Begin(); it != enbNetDev.End(); ++it)
    {
        DynamicCast<NrGnbNetDevice>(*it)->UpdateConfig();
    }

    for (auto it = ueNetDev.Begin(); it != ueNetDev.End(); ++it)
    {
        DynamicCast<NrUeNetDevice>(*it)->UpdateConfig();
    }

    // create the internet and install the IP stack on the UEs
    // get SGW/PGW and create a single RemoteHost
    Ptr<Node> pgw = epcHelper->GetPgwNode();
    NodeContainer remoteHostContainer;
    remoteHostContainer.Create(1);
    Ptr<Node> remoteHost = remoteHostContainer.Get(0);
    InternetStackHelper internet;
    internet.Install(remoteHostContainer);

    // connect a remoteHost to pgw. Setup routing too
    PointToPointHelper p2ph;
    p2ph.SetDeviceAttribute("DataRate", DataRateValue(DataRate("100Gb/s")));
    p2ph.SetDeviceAttribute("Mtu", UintegerValue(2500));
    p2ph.SetChannelAttribute("Delay", TimeValue(Seconds(0.010)));
    NetDeviceContainer internetDevices = p2ph.Install(pgw, remoteHost);

    Ipv4AddressHelper ipv4h;
    ipv4h.SetBase("1.0.0.0", "255.0.0.0");
    Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign(internetDevices);
    Ipv4StaticRoutingHelper ipv4RoutingHelper;

    Ptr<Ipv4StaticRouting> remoteHostStaticRouting =
        ipv4RoutingHelper.GetStaticRouting(remoteHost->GetObject<Ipv4>());
    remoteHostStaticRouting->AddNetworkRouteTo(Ipv4Address("7.0.0.0"), Ipv4Mask("255.0.0.0"), 1);
    internet.Install(ueNodes);

    Ipv4InterfaceContainer ueIpIface;
    ueIpIface = epcHelper->AssignUeIpv4Address(NetDeviceContainer(ueNetDev));

    // assign IP address to UEs, and install UDP downlink applications
    uint16_t dlPort = 1234;
    ApplicationContainer clientApps;
    ApplicationContainer serverApps;
    bool ueAsServer = false;
    Ipv4Address serverIp;


    for (uint32_t u = 0; u < ueNodes.GetN(); ++u)
    {
        Ptr<Node> ueNode = ueNodes.Get(u);
        // Set the default gateway for the UE
        Ptr<Ipv4StaticRouting> ueStaticRouting =
            ipv4RoutingHelper.GetStaticRouting(ueNode->GetObject<Ipv4>());
        ueStaticRouting->SetDefaultRoute(epcHelper->GetUeDefaultGatewayAddress(), 1);

        if (ueAsServer)
        {
        serverIp = ueIpIface.GetAddress(0);
        }else{
        serverIp = internetIpIfaces.GetAddress(1);
        }

        std::cout << "Server IP: " << serverIp << std::endl;
        
        UdpServerHelper dlPacketSinkHelper(dlPort);
        serverApps.Add(dlPacketSinkHelper.Install(ueNodes.Get(u)));

        UdpClientHelper dlClient(ueIpIface.GetAddress(u), dlPort);
        dlClient.SetAttribute("Interval", TimeValue(MicroSeconds(10)));
        dlClient.SetAttribute("PacketSize", UintegerValue(1500));
        dlClient.SetAttribute ("MaxPackets", UintegerValue(1000));
        clientApps.Add(dlClient.Install(remoteHost));
    }

    // attach UEs to the closest eNB

    nrHelper->AttachToEnb(ueNetDev.Get(15), enbNetDev.Get(0));//20,4
    nrHelper->AttachToEnb(ueNetDev.Get(16), enbNetDev.Get(0));//19,5
    nrHelper->AttachToEnb(ueNetDev.Get(19), enbNetDev.Get(0));//21,5
    nrHelper->AttachToEnb(ueNetDev.Get(18), enbNetDev.Get(0));//18.87,3.05
    nrHelper->AttachToEnb(ueNetDev.Get(9), enbNetDev.Get(0));//21,3

    nrHelper->AttachToEnb(ueNetDev.Get(2), enbNetDev.Get(3));//-19,3
    nrHelper->AttachToEnb(ueNetDev.Get(17), enbNetDev.Get(3));//-20,4
    nrHelper->AttachToEnb(ueNetDev.Get(5), enbNetDev.Get(3));//-21,3
    nrHelper->AttachToEnb(ueNetDev.Get(8), enbNetDev.Get(3));//-19,5
    nrHelper->AttachToEnb(ueNetDev.Get(12), enbNetDev.Get(3));//-21,5
    nrHelper->AttachToEnb(ueNetDev.Get(3), enbNetDev.Get(3));//20,4
    nrHelper->AttachToEnb(ueNetDev.Get(13), enbNetDev.Get(3));//20,4

    nrHelper->AttachToEnb(ueNetDev.Get(4), enbNetDev.Get(1));//21,5
    nrHelper->AttachToEnb(ueNetDev.Get(10), enbNetDev.Get(1));//18.87,3.05
    nrHelper->AttachToEnb(ueNetDev.Get(6), enbNetDev.Get(1));//21,3

    nrHelper->AttachToEnb(ueNetDev.Get(0), enbNetDev.Get(2));//20,4
    nrHelper->AttachToEnb(ueNetDev.Get(1), enbNetDev.Get(2));//19,5
    nrHelper->AttachToEnb(ueNetDev.Get(7), enbNetDev.Get(2));//21,5
    nrHelper->AttachToEnb(ueNetDev.Get(14), enbNetDev.Get(2));//18.87,3.05
    nrHelper->AttachToEnb(ueNetDev.Get(11), enbNetDev.Get(2));//21,3

  

    // start server and client apps
    serverApps.Start(Seconds(1));
    clientApps.Start(Seconds(1));

    // enable the traces provided by the nr module
    nrHelper->EnableTraces();

    MonitorarPosicaoEnb(enbNodes.Get(0));
    MonitorarPosicaoEnb(enbNodes.Get(1));
    MonitorarPosicaoEnb(enbNodes.Get(2));
    MonitorarPosicaoEnb(enbNodes.Get(3));
    Simulator::Stop(Seconds(simTime));
    Simulator::Run();
}