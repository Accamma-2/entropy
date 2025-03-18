import random
import math
import time
import socket
from collections import Counter

# Step 1: Simulate sending data packets to a server
def packetgeneration(numofpackets, diversity=255):
    packets = []
    for _ in range(numofpackets):
        ipaddress = f"{random.randint(1, diversity)}.{random.randint(1, diversity)}.{random.randint(1, diversity)}.{random.randint(1, diversity)}"
        packets.append(ipaddress)
    return packets

# Step 2: Send packets to a server (Simulated)
def send_packets(packets, port=8080, delay=0.01):
    server_ip = socket.gethostbyname(socket.gethostname())  # Dynamically get local machine's IP
    print(f"Sending packets to {server_ip}:{port}")
    for packet in packets:
        print(f"Sending the packets: {packet}")
        time.sleep(delay)  # Simulate network delay
    print("Packets sent successfully.")

# Step 3: Calculate entropy of IP distribution
def entropycalculation(packets):
    packetcount = Counter(packets)
    totalnoofpackets = len(packets)
    probabilities = []
    for count in packetcount.values():
        p = count / totalnoofpackets
        probabilities.append(p)
    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy

# Step 4: Improved DDoS detection with moving average and adaptive threshold
class DDoSDetector:
    def __init__(self, window_size=10, threshold=3.5):
        self.window_size = window_size
        self.threshold = threshold
        self.entropy_window = []

    def detect_ddos(self, packets):
        if len(packets) < 5:
            print("Warning: Small packet size may affect detection accuracy.")

        entropy = entropycalculation(packets)
        print("Entropy:", round(entropy, 4))

        # Update moving average window
        self.entropy_window.append(entropy)
        if len(self.entropy_window) > self.window_size:
            self.entropy_window.pop(0)

        avg_entropy = sum(self.entropy_window) / len(self.entropy_window)

        # Prevent adaptive threshold from dropping too low
        adaptive_threshold = max(2.0, avg_entropy * 0.9)

        if entropy < adaptive_threshold:
            print("DDoS attack detected!")
            return True
        else:
            print("Normal traffic")
            return False


# Step 5: Evaluate accuracy
def evaluate_accuracy(detector, test_cases):
    correct = 0
    for packets, is_attack in test_cases:
        detected = detector.detect_ddos(packets)
        if detected == is_attack:
            correct += 1
    accuracy = (correct / len(test_cases)) * 100
    print("Accuracy of the attack detection:", round(accuracy, 2), "%")
    return accuracy

# Step 6: Main function
if __name__ == "__main__":
    print("DDoS detection using entropy computing with adaptive threshold")

    try:
        packet_size = int(input("Enter the packet size of maximum 1000 "))
        if packet_size > 1000:
            print("Invalid packet size")
            exit()
    except ValueError:
        print("Invalid input.Default packet size is used")
        exit()

    # Simulate normal traffic (high entropy, diverse IPs)
    normal_traffic = packetgeneration(packet_size)

    # Simulate DDoS traffic (low entropy, repeated IPs)
    ddos_traffic = packetgeneration(packet_size, diversity=2)
    # Send packets to a simulated server
    send_packets(normal_traffic)
    send_packets(ddos_traffic)

    # Initialize DDoS detector with moving average window
    detector = DDoSDetector(window_size=10, threshold=3.5)

    # Evaluate accuracy using test cases
    test_cases = [(normal_traffic, False), (ddos_traffic, True)]
    evaluate_accuracy(detector, test_cases)


