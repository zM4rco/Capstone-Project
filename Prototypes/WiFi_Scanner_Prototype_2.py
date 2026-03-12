import subprocess
import re
import time
import threading


def get_wifi_networks_rssi():
    # Run the netsh command to list visible Wi-Fi networks
    result = subprocess.run(["netsh", "wlan", "show", "network", "mode=Bssid"], capture_output=True, text=True)
    # print("Netsh Command Output:\n", result.stdout) testing purpose delete the hashtag if needed

    # Expressions to match only SSIDs and RSSI values correctly
    ssid_pattern = re.compile(r"SSID\s+\d+\s*:\s*([^\n]+)")  # Match SSIDs (network names)
    # Ignore the mandarin first, my system language is mandarin, so I have to add this in, in order to test the code
    rssi_pattern = re.compile(r"(\u4fe1\u53f7|Signal)\s*:\s*(\d+)%")

    # Extract SSIDs and RSSI
    ssids = ssid_pattern.findall(result.stdout)
    rssi_matches = rssi_pattern.findall(result.stdout)  # Extract using the refined pattern

    # Convert extracted RSSI matches to a simple list of values
    rssi_values = [int(match[1]) for match in rssi_matches]

    # Print the extracted values
    print("\nExtracted SSIDs:", ssids)
    print("Extracted RSSI Values (%):", rssi_values)

    # Remove unwanted entries (such as BSSIDs or other strings) from the SSIDs list
    ssids = [ssid for ssid in ssids if not re.match(r"([0-9a-f]{2}:){5}[0-9a-f]{2}", ssid.lower())]

    # Print output to verify after cleanup
    print("Filtered SSIDs:", ssids)

    # Create a dictionary to group multiple RSSI values per SSID
    ssid_to_rssi = {}
    ssid_index = 0  # Tracks the SSID index
    rssi_index = 0  # Tracks the RSSI index

    # Traverse through SSIDs and assign corresponding RSSI values
    while ssid_index < len(ssids) and rssi_index < len(rssi_values):
        ssid = ssids[ssid_index].strip()
        rssi = rssi_values[rssi_index]

        # Group RSSI values under each SSID
        if ssid in ssid_to_rssi:
            ssid_to_rssi[ssid].append(rssi)
        else:
            ssid_to_rssi[ssid] = [rssi]
        rssi_index += 1
        # If there are multiple SSIDs sharing RSSI values, move to the next unique SSID only after processing all corresponding RSSI values
        ssid_index += 1

    # Print output to verify the SSID to RSSI grouping
    print("SSID to RSSI Mapping:", ssid_to_rssi)

    # Collect SSIDs and Convert RSSI signal percentage -> dBm
    networks = []
    for ssid, rssi_list in ssid_to_rssi.items():
        if rssi_list:
            # Convert the average of RSSI percentages to approximate dBm value
            average_rssi = sum(rssi_list) // len(rssi_list)  # Take the average RSSI if multiple values exist
            try:
                rssi_dbm = (average_rssi - 100) // 2  # Approximate conversion to dBm
            except ValueError:
                rssi_dbm = "N/A"
            networks.append({"SSID": ssid, "RSSI (dBm)": rssi_dbm})
    return networks


def get_channel_load():
    # Run the netsh command to list visible Wi-Fi networks
    result = subprocess.run(["netsh", "wlan", "show", "network", "mode=Bssid"], capture_output=True, text=True)
    channel_pattern = re.compile(r"(频道|Channel)\s*:\s*(\d+)")  # Extract channel numbers, supports Mandarin and English

    # Extract channel numbers
    channels = channel_pattern.findall(result.stdout)
    channel_load = {}

    # Calculate load per channel
    for match in channels:
        channel = match[1]  # Extract the channel number
        if channel in channel_load:
            channel_load[channel] += 1
        else:
            channel_load[channel] = 1

    # Print channel load analysis
    print("\nChannel Load Analysis:")
    if channel_load:
        for channel, count in channel_load.items():
            print(f"Channel {channel}: {count} network(s) are using")
    else:
        print("No channel information found.")


def wlan_connection_traffic_analysis():
    # Run the netsh command to show interface statistics
    result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
    print("Debug: Netsh Command Output:\n", result.stdout)  # Debugging: Print the raw output to see its structure

    # Extract relevant traffic information
    receive_rate_pattern = re.compile(r"接收速率\(Mbps\)\s*:\s*(\d+\.\d+)")
    transmit_rate_pattern = re.compile(r"传输速率\s*\(Mbps\)\s*:\s*(\d+\.\d+)")
    signal_pattern = re.compile(r"信号\s*:\s*(\d+)%")

    receive_rate_match = receive_rate_pattern.search(result.stdout)
    transmit_rate_match = transmit_rate_pattern.search(result.stdout)
    signal_match = signal_pattern.search(result.stdout)

    if receive_rate_match and transmit_rate_match and signal_match:
        receive_rate = float(receive_rate_match.group(1))
        transmit_rate = float(transmit_rate_match.group(1))
        signal_strength = int(signal_match.group(1))

        print(f"\nWLAN Connection Traffic Analysis:")
        print(f"Receive Rate: {receive_rate} Mbps")
        print(f"Transmit Rate: {transmit_rate} Mbps")
        print(f"Signal Strength: {signal_strength}%")
    else:
        print("\nNo traffic information found.")


def menu():
    while True:
        print("\nWiFi Network Analysis Tool")
        print("1. Network Analysis")
        print("2. Channel Load ")
        print("3. WLAN Connection Traffic Analysis")
        print("4. Trilateration (Coming Soon)")
        print("5. Exit")
        choice = input("Enter your choice (In Number): ")

        if choice == "1":
            # Start network analysis loop
            try:
                analysis_thread = threading.Thread(target=network_analysis_loop)
                analysis_thread.start()
                analysis_thread.join()  # Wait for the thread to finish
            except KeyboardInterrupt:
                print("\nNetwork analysis stopped.")
        elif choice == "2":
            get_channel_load()
        elif choice == "3":
            wlan_connection_traffic_analysis()
        elif choice == "4":
            print("Trilateration feature is coming soon!")
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def network_analysis_loop():
    stop_event = threading.Event()  # Create an event to signal when to stop the loop

    def listen_for_exit():
        while True:
            if input("\n----------------- Found Networks -----------------") == 'q':
                stop_event.set()  # Set the stop event when 'q' is pressed
                break

    # Start the input listener thread
    listener_thread = threading.Thread(target=listen_for_exit)
    listener_thread.start()
    try:
        while not stop_event.is_set():
            networks_info = get_wifi_networks_rssi()
            for network in networks_info:
                print(f"Network: {network['SSID']}, RSSI: {network['RSSI (dBm)']} dBm")
            print("\n""--------------------- END OF THE RESULT ----------------------")
            print("--------------- Press 'q' and Entry to EXIT ------------------")
            print("-------------- Updating the list in 30 seconds ---------------")
            for _ in range(20):
                if stop_event.is_set():
                    break
                time.sleep(1)  # Wait for 20 seconds before running the analysis again
    except KeyboardInterrupt:
        print("\nExiting network analysis loop.")
    if not stop_event.is_set():
        networks_info = get_wifi_networks_rssi()  # Get the last set of network info before exit
    print("Last Scan:")
    for network in networks_info:
        print(f"Network: {network['SSID']}, RSSI: {network['RSSI (dBm)']} dBm")


if __name__ == "__main__":
    menu()
