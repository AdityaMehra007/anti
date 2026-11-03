# HYPRLAND SUPREME ARCHITECTURE & PROTOCOL DOSSIER
**System Identity**: Hyprland Autonomous Compositor & IPC Ecosystem  
**Repository**: [hyprwm/Hyprland](https://github.com/hyprwm/Hyprland)  
**Standard**: OMEGA Production Engineering Codex & ISO/IEC 25010 Quality Framework  
**Classification**: Sovereign Desktop Compositor, Aquamarine Rendering Pipeline & IPC Engine  

---

## 1. Executive Summary & Core Philosophy

**Hyprland** is an independent, dynamic tiling Wayland compositor written in modern **C++ (C++23)** that merges uncompromised low-latency performance with state-of-the-art desktop visual aesthetics. Unlike minimal tiling window managers that omit visual fidelity or monolithic desktop environments (GNOME Mutter, KDE KWin) that impose heavy background daemon footprints, Hyprland implements:

1. **Hardware-Accelerated Fluid Aesthetics**: Native dual-kawase blur, drop shadows, customizable cubic-bezier physics animations, and animated gradient borders rendered directly inside the compositor render pass.
2. **Independent Rendering Abstraction (Aquamarine)**: Purpose-built rendering engine that abstracts backend display protocols (DRM/KMS, Wayland-in-Wayland, headless) away from legacy `wlroots` constraints, enabling tight integration with custom Vulkan/GLES2 pipelines.
3. **Bi-Directional IPC Architecture**: Dual UNIX domain socket interface providing synchronous command/response dispatch (`.socket.sock`) alongside a dedicated, non-blocking zero-polling real-time event stream (`.socket2.sock`).
4. **Dynamic Tiling Topology**: Dual-engine support for **Dwindle** (BSP-tree recursive splitting preserving screen ratio) and **Master** (traditional dynamic stack) layouts, fully integrated with floating windows, pin states, and scratchpad/special workspaces.
5. **Dynamic Native Plugin Subsystem**: Shared library C++ ABI architecture managed via `hyprpm` with compile-time header verification and dynamic symbol binding.

```
                      +---------------------------------------+
                      |       Hyprland Core (C++23)          |
                      |   Event Loop & Dispatcher Engine      |
                      +-------------------+-------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
+-------v---------+              +--------v--------+               +--------v--------+
|  Aquamarine     |              |  Layout Engine  |               |  Dual Socket    |
|  Render Backend |              | Dwindle/Master  |               |  IPC Pipeline   |
| (GLES2/Vulkan)  |              | Scene Graph     |               | (Cmd & Stream)  |
+-------+---------+              +--------+--------+               +--------+--------+
        |                                 |                                 |
+-------v---------+              +--------v--------+               +--------v--------+
| Displays & DRM  |              | Client Surfaces |               | hyprctl, SDKs,  |
| KMS Frame Pacing|              | Wayland / XWay  |               | UI Cockpit, MCP |
+-----------------+              +-----------------+               +-----------------+
```

---

## 2. Rendering Subsystem: Aquamarine & GPU Shader Pipeline

### 2.1 The Aquamarine Abstraction Layer
Hyprland historically utilized `wlroots` as its backend compositor library. To overcome `wlroots` design limitations regarding modern C++ object lifetimes, multi-GPU synchronization, and custom rendering backends, Hyprland introduced **Aquamarine**:
- **Backend Portability**: Provides uniform interfaces for DRM/KMS, Libinput, and headless/virtual monitors.
- **Native C++ Object Semantics**: Employs RAII and smart pointers (`std::shared_ptr`, `std::unique_ptr`), eliminating C-style manual memory lifecycle hazards.
- **Direct Buffer Allocation**: Native GBM (Generic Buffer Management) and EGL stream integration for NVidia and AMD/Intel GPUs.

### 2.2 Shader & Filter Pipeline
Hyprland integrates shaders into its single-pass compositor pipeline:
- **Dual-Kawase Blur**: Multi-pass downsampling and upsampling algorithm with configurable radius and iteration count, executed as GPU compute/fragment shaders with minimal memory bandwidth overhead.
- **Shadow Mapping**: Fast analytical box-blur shadow computation around client geometry, accounting for window borders and rounded corner stencils.
- **Rounded Corner Stencils**: Fragment-level anti-aliased stencil clipping guaranteeing zero pixel jaggedness regardless of display scaling factor.
- **Gradient Borders**: Real-time multi-stop color interpolator supporting linear gradients, angular rotations, and animated color phase shifts.

---

## 3. Dynamic Tiling & Scene Graph Mechanics

Hyprland models desktop geometry through a hierarchical scene graph:

```
Monitor (Output)
 └── Workspace (ID: 1..N or special:name)
      ├── Tiling Node (Dwindle Binary Tree / Master Stack)
      │    ├── Client Surface A (Active Tiled Window)
      │    └── Client Surface B (Tiled Window)
      ├── Floating Stack (Z-Indexed Overlay)
      │    ├── Floating Window (Pin / Modal)
      │    └── Picture-in-Picture Node
      └── Layer Shell Surfaces
           ├── Top Layer (Waybar / Status Bar)
           ├── Overlay Layer (Rofi / Application Launcher)
           └── Notification Layer (SwayNC / Dunst)
```

### 3.1 Dwindle Layout Engine
- **Recursive Binary Split**: When a new window opens, the active node's bounding rectangle splits horizontally or vertically depending on aspect ratio.
- **Preserve Split**: Optional lock on split orientation (`preserve_split = true`) allowing deterministic BSP manual tiling.
- **Smart Gaps & Padding**: Inner gaps between tiled windows and outer gaps separating windows from monitor edges or Layer Shell surfaces.

### 3.2 Master Layout Engine
- Allocates one or more "Master" windows occupying a designated percentage of the display (e.g. 50%), while all slave windows stack sequentially in the remainder.
- Orientation dynamically configurable (`left`, `right`, `top`, `bottom`, `center`).

---

## 4. Dual-Socket IPC Architecture & Event Model

Hyprland exposes two dedicated UNIX domain sockets located under:
`$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/`

### 4.1 Command Socket (`.socket.sock`)
- **Protocol**: Request-Response plain text or JSON.
- **Operation**: Synchronous. Client writes a command (e.g., `j/clients`, `dispatch workspace 2`, `keyword decoration:rounding 12`), and Hyprland returns the response payload.
- **Flag Support**:
  - `j/`: Returns structured JSON array or object.
  - Plain dispatch: Executes compositor actions and returns status strings (`ok` or error description).

### 4.2 Event Stream Socket (`.socket2.sock`)
- **Protocol**: Real-time line-delimited event broadcast.
- **Operation**: Asynchronous push notification. Hyprland emits notifications without requiring polling:
  ```
  workspace>>2
  focusedmon>>DP-1,2
  openwindow>>0x55a9b2,2,kitty,kitty
  closewindow>>0x55a9b2
  activewindowv2>>0x55b1c8
  movewindow>>0x55b1c8,3
  fullscreen>>1
  monitoradded>>HDMI-A-1
  ```

---

## 5. Visual Physics & Bezier Animation Mathematics

Hyprland evaluates window transitions using parametric cubic Bézier curves:
$$B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3, \quad t \in [0, 1]$$

Where:
- $P_0 = (0, 0)$ is the initial state at $t=0$.
- $P_3 = (1, 1)$ is the target state at $t=1$.
- $P_1 = (x_1, y_1)$ and $P_2 = (x_2, y_2)$ define the control points.

Values of $y_1, y_2 > 1.0$ yield physical **overshoot/rebound** animations (e.g. bouncy window pop-in), while $y < 0.0$ generates anticipation retraction.

### Configured Curves
- **Standard Ease**: `cubic-bezier(0.25, 0.1, 0.25, 1.0)`
- **Aggressive Overshot**: `cubic-bezier(0.05, 0.9, 0.1, 1.05)`
- **Silky Decel**: `cubic-bezier(0.16, 1, 0.3, 1)`

---

## 6. Architecture Comparison Matrix

| Capability / Metric | Hyprland | Sway / wlroots | KDE KWin (Wayland) | GNOME Mutter | dwl |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Language & Standard** | Modern C++23 | C (C11) | C++20 / Qt6 | C / GObject | C (C99) |
| **Backend Subsystem** | Aquamarine | wlroots | KWin DRM / Wayland | Mutter Clutter/DRM | wlroots |
| **Dynamic Tiling Mode** | Dwindle + Master | Manual i3 tree | Scripted (Krohnkite) | Extension-based | Tag-based (dwm) |
| **Native Blur & Bling** | Dual-Kawase / In-pass | None (patches req.) | KWin Effects | Ext-dependent | None |
| **Bezier Physics** | Native cubic-bezier | None | Limited curves | Fixed curves | None |
| **IPC Mechanism** | Dual UNIX socket + JSON | i3 IPC socket | D-Bus | D-Bus | None / Patch |
| **Memory Footprint** | ~35 MB - 60 MB | ~20 MB - 35 MB | ~180 MB - 350 MB | ~250 MB - 500 MB | ~8 MB - 15 MB |
| **Plugin Subsystem** | Dynamic C++ (`hyprpm`) | None | KWin Scripting | Shell Extensions | Config.h patch |
| **Multi-Monitor VRR** | Per-monitor adaptive | Global / patchy | Supported | Partial | Manual |

---

## 7. Security, Sandboxing & Protocol Isolation

1. **Wayland Protocol Boundary**: Applications cannot snoop keystrokes from other windows or capture screen contents unless authorized via the `xdg-desktop-portal-hyprland` Wayland desktop portal.
2. **XWayland Isolation**: Legacy X11 applications run in an isolated XWayland rootless server; direct access to Wayland client buffers is restricted.
3. **Privileged Wayland Protocols**: Specialized protocols (`wlr-layer-shell-unstable-v1`, `wlr-screencopy-unstable-v1`, `wlr-virtual-keyboard-v1`) are guarded by socket access permissions.
4. **IPC Socket Access**: UNIX domain socket permissions restrict IPC control to the authenticated user owning the session (`0700` directory mask).

---

## 8. Sovereign Operational Lifecycle (12 Phases)

To guarantee absolute verification and zero-defect execution, the Hyprland Autonomous Orchestration Ecosystem verifies all 12 operational layers:
1. **Compositor Telemetry**: Version, Aquamarine renderer, instance signature, and PID check.
2. **Display Output Topology**: Multi-head resolution, refresh rates, positions, and scaling.
3. **Workspace Management**: Active, vacant, and special scratchpad workspaces.
4. **Client Tiling Engine**: Dwindle vs master placement, tiled and floating geometries.
5. **Window Rule Matrix**: Exact and regex class matchers (`windowrulev2`).
6. **Bling & Blurs**: Dual-kawase shader parameters, drop shadows, and rounding.
7. **Animation Curves**: Bezier parameter validation and animation speeds.
8. **Input Devices**: Keyboards, touchpads, gesture settings, and mouse acceleration.
9. **Keybinding Matrix**: Super-key ergonomically bound actions and dispatchers.
10. **Layer Shell Surfaces**: Status bar (`waybar`), launcher (`rofi`), and notifications (`swaync`).
11. **Socket2 Event Stream**: Live real-time event reactor and subscription telemetry.
12. **Plugin Subsystem**: Dynamic shared library integrity and ecosystem tools (`hyprlock`, `hypridle`).
