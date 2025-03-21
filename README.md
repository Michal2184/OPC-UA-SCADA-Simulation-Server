# OPC UA SCADA Simulation Server

This project provides a fully-featured **OPC UA Server with a GUI**, designed for **SCADA system testing and simulation**. It emulates 5 production lines with various tag values such as levels, temperatures, pumps, and agitators.

## 🚀 Features

- 🧪 **Simulation-ready** with dynamic tag updates
- 🔐 **Secure communication** via self-signed certificates (Basic256Sha256 - Sign & Encrypt)
- 🔍 **GUI Interface** built using `FreeSimpleGUI` for real-time monitoring
- ⚙️ **Customizable** tag data model and client certificate handling
- 📦 **Certificate management** with automated generation and validation

## 📁 Project Structure

```
.
├── OPCUAServer_GUI4a.py       # Main application script
├── certificates/              # Generated SSL/TLS certificates
│   ├── certs/
│   ├── private/
│   ├── clients/
│   └── csr/
└── README.md
```

## 🧰 Requirements

- Python 3.10+
- Packages:
  - `asyncua`
  - `cryptography`
  - `FreeSimpleGUI` (custom PySimpleGUI fork)

Install dependencies:

```bash
pip install asyncua cryptography FreeSimpleGUI
```

## 🛠️ Running the Server

1. Run the server script:

```bash
python OPCUAServer_GUI4a.py
```

2. On first run, you'll be prompted to **generate certificates**. Follow the on-screen instructions.
3. Once the server starts, connect using any OPC UA client with a **client certificate** placed in:
   ```
   certificates/clients/
   ```

## 🧪 Simulation Details

The server simulates 5 production lines (`Line1` to `Line5`) with the following variables:
- `Temperature.PV`
- `Level.PV`
- `Pump1/2.PV`, `.CMD`, `.Speed.SP`
- `Agitator.PV`, `.CMD`, `.Speed.PV`
- `Inlet1/2.CMD`, `.CLS`, `.OLS`
- `Outlet.CMD`, `.CLS`, `.OLS`
- `Status.STR`
- `MixingTime.PV`

Each line goes through **Filling → Mixing → Draining** phases.

## 🔐 Security Setup

- Server generates self-signed certificates in `certificates/certs/`.
- To allow client access, place the client's certificate in `certificates/clients/`.
- All traffic is encrypted using the Basic256Sha256 profile.

## 🖥️ GUI Preview

- View server logs and client connections in real-time.
- Option to reload client certificates without restarting.

---

## 📬 License

This project is provided as-is for SCADA testing and educational purposes.
