#!/usr/bin/env bash

# Download the CIC-IDS-2017 dataset from @IsaiahHarvi's server
# Necessary evil to avoid git-lfs costs

IP="harvirp.ddns.net"
PORT="5000"
CSV_FILES=(
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
    "Friday-WorkingHours-Morning.pcap_ISCX.csv"
    "Monday-WorkingHours.pcap_ISCX.csv"
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv"
    "Tuesday-WorkingHours.pcap_ISCX.csv"
    "Wednesday-workingHours.pcap_ISCX.csv"
)

for FILE in "${CSV_FILES[@]}"; do
    DEST="data/CIC/${FILE}"

    if [ -f "${DEST}" ]; then
        echo "${FILE} exists, skipping..."
    else
        URL="http://${IP}:${PORT}/csv/${FILE}"
        wget --progress=bar:force:noscroll -O "${DEST}" "${URL}"

        if [ $? -eq 0 ]; then
            echo "Downloaded ${FILE}"
        else
            echo "Failed downloading ${FILE}."
            exit 1
        fi
    fi
done
