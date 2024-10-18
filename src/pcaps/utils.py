"""Various tools for working with PCAP files."""

import pandas as pd


def rename_cols(self, flow_data: pd.DataFrame) -> pd.DataFrame:
    """Rename NFStream flows to match CICIDS colum names."""
    return flow_data.rename(
        columns={
            # IP and port information
            "src_ip": "Source_IP",
            "dst_ip": "Destination_IP",
            "src_port": "Source_Port",
            "dst_port": "Destination_Port",
            "protocol": "Protocol",
            # Flow duration and packet-related information
            "bidirectional_duration_ms": "Flow_Duration",
            "src2dst_packets": "Total_Fwd_Packets",
            "dst2src_packets": "Total_Backward_Packets",
            "src2dst_bytes": "Total_Length_of_Fwd_Packets",
            "dst2src_bytes": "Total_Length_of_Bwd_Packets",
            # Packet inter-arrival time (IAT) information
            "src2dst_min_piat_ms": "Fwd_IAT_Min",
            "src2dst_mean_piat_ms": "Fwd_IAT_Mean",
            "src2dst_stddev_piat_ms": "Fwd_IAT_Std",
            "src2dst_max_piat_ms": "Fwd_IAT_Max",
            "dst2src_min_piat_ms": "Bwd_IAT_Min",
            "dst2src_mean_piat_ms": "Bwd_IAT_Mean",
            "dst2src_stddev_piat_ms": "Bwd_IAT_Std",
            "dst2src_max_piat_ms": "Bwd_IAT_Max",
            "bidirectional_min_piat_ms": "Flow_IAT_Min",
            "bidirectional_mean_piat_ms": "Flow_IAT_Mean",
            "bidirectional_stddev_piat_ms": "Flow_IAT_Std",
            "bidirectional_max_piat_ms": "Flow_IAT_Max",
            # Packet size information
            "src2dst_min_ps": "Fwd_Packet_Length_Min",
            "src2dst_mean_ps": "Fwd_Packet_Length_Mean",
            "src2dst_stddev_ps": "Fwd_Packet_Length_Std",
            "src2dst_max_ps": "Fwd_Packet_Length_Max",
            "dst2src_min_ps": "Bwd_Packet_Length_Min",
            "dst2src_mean_ps": "Bwd_Packet_Length_Mean",
            "dst2src_stddev_ps": "Bwd_Packet_Length_Std",
            "dst2src_max_ps": "Bwd_Packet_Length_Max",
            "bidirectional_min_ps": "Flow_Packet_Length_Min",
            "bidirectional_mean_ps": "Flow_Packet_Length_Mean",
            "bidirectional_stddev_ps": "Flow_Packet_Length_Std",
            "bidirectional_max_ps": "Flow_Packet_Length_Max",
            # TCP flag-related fields
            "src2dst_syn_packets": "Fwd_PSH_Flags",
            "bidirectional_syn_packets": "Fwd_Syn_Flags",
            "bidirectional_ack_packets": "Fwd_Ack_Flags",
            "bidirectional_psh_packets": "Fwd_PSH_Flags",
            "bidirectional_urg_packets": "Fwd_URG_Flags",
            "bidirectional_cwr_packets": "Fwd_CWR_Flags",
            "bidirectional_ece_packets": "Fwd_ECE_Flags",
            "bidirectional_rst_packets": "Fwd_RST_Flags",
            "bidirectional_fin_packets": "Fwd_FIN_Flags",
            # ACK and other TCP packet counters
            "src2dst_ack_packets": "Fwd_Ack_Flags",
            "src2dst_psh_packets": "Fwd_PSH_Flags",
            "src2dst_rst_packets": "Fwd_RST_Flags",
            "src2dst_fin_packets": "Fwd_FIN_Flags",
            "dst2src_syn_packets": "Bwd_Syn_Flags",
            "dst2src_ack_packets": "Bwd_Ack_Flags",
            "dst2src_rst_packets": "Bwd_RST_Flags",
            "dst2src_fin_packets": "Bwd_FIN_Flags",
        }
    )
