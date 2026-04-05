#TCP Port Scanner (Kali Linux)

## Task 1

This project is a multithreaded TCP port scanner built using Python in Kali Linux.

---

## ⚙️ Features

* Scan single or multiple ports
* Supports port ranges (e.g. 1-1024)
* Multithreading for faster scanning
* Logging results to a file
* Timeout handling

---

## 🛠️ Technologies Used

* Python 3
* Socket Programming
* ThreadPoolExecutor
* Kali Linux

---

## 🚀 How to Run

```bash
python3 port_scanner.py --host 127.0.0.1 --ports 22,80,443
```

---

## 📊 Example Output

```
Port 22: open
Port 80: open
```

---

## 🧪 Testing with Netcat

```bash
nc -lvp 8080
python3 port_scanner.py --host 127.0.0.1 --ports 8080
```

##  Author

NEEDHU B
