import socket
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import errno


# ----------------------------
# Parse Arguments
# ----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="TCP Port Scanner")

    parser.add_argument("--host", required=True, help="Target host (IP or hostname)")
    parser.add_argument(
        "--ports",
        required=True,
        help="Port range (e.g. 1-1024) or list (e.g. 22,80,443)",
    )
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout in seconds")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--log", default="scan.log", help="Log file name")

    return parser.parse_args()


# ----------------------------
# Parse Ports
# ----------------------------
def parse_ports(port_str):
    ports = set()

    try:
        if "-" in port_str:
            start, end = map(int, port_str.split("-"))
            ports.update(range(start, end + 1))
        else:
            ports.update(int(p.strip()) for p in port_str.split(","))
    except Exception:
        raise ValueError("Invalid port format. Use '1-1024' or '22,80,443'")

    return sorted(ports)


# ----------------------------
# Scanner Class
# ----------------------------
class PortScanner:
    def __init__(self, host, ports, timeout, max_threads):
        self.host = host
        self.ports = ports
        self.timeout = timeout
        self.max_threads = max_threads
        self.results = []

    def scan_port(self, port):
        status = "unknown"

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.host, port))

                if result == 0:
                    status = "open"
                elif result == errno.ECONNREFUSED:
                    status = "closed"
                else:
                    status = "timed out"

        except socket.gaierror:
            raise Exception("DNS resolution failed")
        except PermissionError:
            status = "permission denied"
        except Exception as e:
            status = f"error: {e}"

        return port, status

    def run(self):
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self.scan_port, p) for p in self.ports]

            for future in as_completed(futures):
                port, status = future.result()
                self.results.append((port, status))

                # Print result
                print(f"Port {port}: {status}")

                # Log result
                logging.info(f"Port {port}: {status}")

        return sorted(self.results)


# ----------------------------
# Logging Setup
# ----------------------------
def setup_logging(file_name):
    logging.basicConfig(
        filename=file_name,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )


# ----------------------------
# Main
# ----------------------------
def main():
    args = parse_args()

    setup_logging(args.log)

    # Resolve host
    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print("❌ Could not resolve hostname")
        return

    print(f"\n🔍 Scanning {args.host} ({ip})")
    print(f"Ports: {args.ports}")
    print(f"Timeout: {args.timeout}s\n")

    # Parse ports
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"❌ {e}")
        return

    scanner = PortScanner(ip, ports, args.timeout, args.threads)

    start = datetime.now()
    scanner.run()
    end = datetime.now()

    print(f"\n✅ Scan completed in {end - start}")


if __name__ == "__main__":
    main()                                            
