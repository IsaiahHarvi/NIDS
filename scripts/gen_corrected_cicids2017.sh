timewindow=0.000500

# Add original pcaps to data/Original_CICIDS2017_pcap

ls data/Original_CICIDS2017_pcap/*.pcap | while read line; do editcap -w $timewindow $line data/CICIDS2017_pcap/$(basename $line | sed 's/\.pcap/_corrected.pcap/'); done
