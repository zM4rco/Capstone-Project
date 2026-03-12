import subprocess
import re


def get_wifi_networks_rssi():
    # Run the netsh command to list visible Wi-Fi networks
    result = subprocess.run(["netsh", "wlan", "show", "network", "mode=Bssid"], capture_output=True, text=True)
    print("Netsh Command Output:\n", result.stdout)  # Print the entire netsh command output for debugging

    # Expressions to match only SSIDs and RSSI values correctly
    ssid_pattern = re.compile(r"SSID\s+\d+\s*:\s*([^\n]+)")  # Match SSIDs (network names)
    rssi_pattern = re.compile(r"(Signal)\s*:\s*(\d+)%")

    # Extract SSIDs and RSSI
    ssids = ssid_pattern.findall(result.stdout)
    rssi_matches = rssi_pattern.findall(result.stdout)  # Extract using the refined pattern

    # Convert extracted RSSI matches to a simple list of values
    rssi_values = [int(match[1]) for match in rssi_matches]

    # Print the extracted values
    print("Extracted SSID & MAC Address:", ssids)
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


if __name__ == "__main__":
    networks_info = get_wifi_networks_rssi()
    for network in networks_info:
        print(f"Network: {network['SSID']}, RSSI: {network['RSSI (dBm)']} dBm")  # Fixed the print statement.
