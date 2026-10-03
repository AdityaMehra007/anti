# 🖥️ MACHINE AUDIT: OMEGA COMMAND CENTER

**Audit Execution Timestamp**: `2026-10-01T16:05:30+05:30`  
**Host Architecture**: Windows x64 Workstation  
**Auditor**: Antigravity OMEGA Senior Autonomous Technology Organization  
**Operating Principle**: *Zero Vibe Coding & Verified Evidence (AGENTS.md)*

---

## 1. Operating System & System Kernel

| Metric | Ground-Truth Value | Assessment |
| :--- | :--- | :--- |
| **Operating System** | Microsoft Windows 10 Home Single Language | Consumer OS; Hyper-V native enterprise management disabled |
| **Version** | `10.0.19045` | Stable 22H2 servicing channel |
| **Build Number** | `19045` | Up-to-date Windows 10 baseline |
| **Kernel Architecture** | 64-bit (`x86_64`) | Full modern 64-bit runtime support |
| **Total Visible RAM** | `16,600,864 KB` (15.83 GiB) | Host addressable space |
| **Free Physical RAM** | `~2,602,800 KB` (~2.48 - 2.60 GiB free) | **High Memory Pressure** under current multi-app baseline |

---

## 2. Central Processing Unit (CPU)

| Metric | Ground-Truth Value | Technical Implications |
| :--- | :--- | :--- |
| **Model** | Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz | 6th Gen Skylake mobile performance tier |
| **Manufacturer** | GenuineIntel | Standard Intel x86_64 architecture |
| **Physical Cores** | `4` Cores | Capable of moderate parallel compilation & worker loops |
| **Logical Threads** | `8` Threads | Hyper-threading enabled |
| **Base Clock** | `2601 MHz` (2.60 GHz) | Base frequency |
| **Max Turbo Clock** | ~`3.50 GHz` single-core turbo | Thermal throttling common under sustained multi-thread load |
| **Instruction Extensions** | `AVX2`, `FMA3`, `SSE4.2`, `VT-x` (Intel Virtualization) | Supports optimized GGUF quantized matrix kernels (llama.cpp) |

---

## 3. Graphics Processing Unit (GPU) & Acceleration

| Metric | Integrated GPU | Dedicated Discrete GPU |
| :--- | :--- | :--- |
| **Device Name** | Intel(R) HD Graphics 530 | **NVIDIA GeForce GTX 960M** |
| **Architecture** | Skylake GT2 | Maxwell (GM107 core) |
| **Compute Capability** | N/A (DirectX 12 / QuickSync) | **SM 5.0 (Compute Capability 5.0)** |
| **Total VRAM** | 1,024 MB (Shared) | **4,096 MiB (4.0 GB GDDR5)** |
| **VRAM Bandwidth** | System DDR4 shared | 80.0 GB/s (128-bit GDDR5) |
| **Driver Version** | `23.20.16.4973` | **`581.80` (WDDM 2.7)** |
| **CUDA Driver Support** | N/A | **CUDA Driver 13.0 reported** |
| **Current VRAM Usage** | Managed by DWM | **341 MiB used / 3,755 MiB free** |
| **AI Inference Engines** | DirectML / OpenVINO | **cuBLAS (SM 5.0), Vulkan, llama.cpp GGUF** |

> [!IMPORTANT]
> **GPU Compute Constraint (CC 5.0)**: Modern PyTorch nightly builds (CUDA 12.x/13.x) deprecate SM 5.0. However, **llama.cpp / Ollama with cuBLAS or Vulkan backends natively compiles and executes high-speed quantized inference** on GM107 Maxwell. Small quantized models (1B to 3B parameters) fit entirely within the 4 GB VRAM!

---

## 4. Physical Memory (RAM)

| Module | Manufacturer | Capacity | Speed | Form Factor |
| :--- | :--- | :--- | :--- | :--- |
| **DIMM 1** | SK Hynix | 8,589,934,592 bytes (8 GB) | 2133 MHz DDR4 | SODIMM (FormFactor 12) |
| **DIMM 2** | SK Hynix | 8,589,934,592 bytes (8 GB) | 2133 MHz DDR4 | SODIMM (FormFactor 12) |
| **Total Physical RAM**| Dual-Channel | **17,179,869,184 bytes (16.0 GB)** | 2133 MT/s | High bandwidth dual-channel |

---

## 5. Storage Topology & Volume Health

| Drive | Friendly Name | File System | Health | Total Size | Free Space | Utilization % | Strategic Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **C:** | System | NTFS | Healthy | **97.73 GB** | **17.59 GB** | 82.0% | **RESTRICTED**: OS, AppData, Core Tools only. NO models or Docker storage. |
| **D:** | Data | NTFS | Healthy | **344.84 GB** | **69.04 GB** | 79.9% | Secondary assets, media, historical cold archives. |
| **E:** | Workspace / Hub | NTFS | Healthy | **586.54 GB** | **335.76 GB** | 42.7% | **PRIMARY OMEGA HUB (`AIOS_ROOT`)**: 335.76 GB Free. All models, databases, containers, repos. |
| **Hidden** | Recovery | NTFS | Healthy | 19.29 GB | 3.49 GB | 81.9% | OEM System Recovery Partition. |
| **Hidden** | EFI / System | NTFS | Healthy | 0.98 GB | 0.21 GB | 78.5% | UEFI Bootloader. |

---

## 6. Network Configuration & Connectivity

- **Active Interface**: `Wi-Fi` via `Intel(R) Dual Band Wireless-AC 3165`
- **Link Speed**: `292.5 Mbps` (802.11ac dual-band)
- **Local IP Address**: `192.168.1.14` (DHCP Assigned, Subnet 24)
- **Gateway / DNS Ping**: Verified (Direct TCP handshake to `8.8.8.8:53` passed in 12ms)
- **Ethernet Controller**: `Realtek PCIe GBE Family Controller` (Available, currently disconnected)
- **Host Security Posture**: Internal private network NAT (`192.168.1.0/24`). Zero public ports exposed to WAN.

---

## 7. Virtualization & Container Subsystems

- **Hypervisor Present**: `False` (Hyper-V native hypervisor not active in Windows 10 Home)
- **Windows Subsystem for Linux (WSL)**: 
  - Version: `WSL 2.7.14.0` (Default Version: 2)
  - Installed Distros: `None` (`Windows Subsystem for Linux has no installed distributions`)
- **Docker Desktop**:
  - Binaries: Docker CLI `29.6.1`, Docker Compose `v5.1.4` installed in `C:\Program Files\Docker\Docker\resources\bin\`
  - Daemon Service: `com.docker.service` (Installed, Status: `Stopped`)
  - Engine Status: Inactive (`//./pipe/dockerDesktopLinuxEngine` not listening)
  - Finding: Docker Desktop requires either an installed WSL2 distro (e.g., Ubuntu/Alpine) or launch of Docker Desktop background daemon.

---

## 8. Runtime & Toolchain Inventory

| Tool / Runtime | Installed Version | Executable Path | Status |
| :--- | :--- | :--- | :--- |
| **Git** | `2.54.0.windows.1` | `C:\Program Files\Git\cmd\git.exe` | Verified Online |
| **GitHub CLI (`gh`)**| `2.95.0` | `C:\Program Files\GitHub CLI\gh.exe` | Verified Online |
| **Python Primary** | `3.13.15 (64-bit)` | `C:\Users\amehr\AppData\Local\Programs\Python\Python313\python.exe` | Verified Online |
| **Python Secondary**| `3.12.10 (64-bit)` | `C:\Users\amehr\AppData\Local\Programs\Python\Python312\python.exe` | Verified Online |
| **uv Package Mgr** | `0.11.26` | `C:\Users\amehr\.local\bin\uv.exe` | Verified Online |
| **Node.js** | `v26.4.0` | `C:\Program Files\nodejs\node.exe` | Verified Online |
| **npm** | `11.x` | `C:\Program Files\nodejs\npm.ps1` | Verified Online |
| **pnpm** | `11.9.0` | `E:\anti gravity\npm-global\pnpm.ps1` | Verified Online |
| **bun** | `1.4.0` | `E:\anti gravity\npm-global\bun.ps1` | Verified Online |
| **Rust Toolchain** | `rustc 1.98.0 / cargo` | `C:\Users\amehr\.cargo\bin\rustc.exe` | Verified Online |
| **.NET Host** | Runtime Host | `C:\Program Files\dotnet\dotnet.exe` | Runtime Present (No SDK) |
| **Ollama Client** | `0.31.1` | `E:\anti gravity\Tools\Ollama\ollama.exe` | Installed on Drive E: |
| **Ollama Data/Models**| Pre-configured | `E:\anti gravity\OllamaData\models` | Contains `qwen2.5-coder:3b`, `llama3:latest` |

---

## 9. Baseline Memory Footprint Analysis

Top working sets currently active on the host machine:
1. `language_server.exe` (Antigravity IDE assistant): **~3,680 MB**
2. `node.exe` (Omniroute / OpenHands canvas): **~777 MB**
3. `Memory Compression` (Windows kernel): **~759 MB**
4. `ChatGPT Classic` Desktop App: **~704 MB**
5. `Antigravity.exe` (IDE Main process): **~596 MB**
6. `chrome.exe` (Active browser sessions): **~1,200 MB** combined
7. `MsMpEng.exe` (Windows Defender): **~440 MB**

**Audit Conclusion**: System is functional with exceptional disk capacity on `E:` (335 GB), powerful modern developer runtimes (Python 3.13, uv, Node 26, Bun, Rust, Ollama), but **requires strict RAM and GPU VRAM discipline** to prevent memory thrashing.
