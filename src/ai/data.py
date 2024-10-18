import os

import pandas as pd
from icecream import ic
from nfstream import NFStreamer

from pcaps.utils import rename_cols


def main():
    for pcap_path in os.listdir("data/CICIDS2017_pcap"):
        if pcap_path.endswith(".pcap"):
            process_pcap(f"data/CICIDS2017_pcap/{pcap_path}")

def process_pcap(pcap_path: str) -> None:
    pcap_name = pcap_path.split("/")[-1].split(".")[0]
    flows = pd.DataFrame(
        NFStreamer(source=pcap_path, statistical_analysis=True).to_pandas()
        # TODO: consider enabling decode_tunnels
    )

    renamed_flows: pd.DataFrame = rename_cols(flows)
    renamed_flows.to_csv(f"data/CIC_NFlows/{pcap_name}.csv", index=False)
    ic(f"Saved {pcap_name}.csv")

if __name__ == "__main__":
    main()
