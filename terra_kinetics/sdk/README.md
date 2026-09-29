# Universal Kinematic Protocol (UKP) SDK

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)]()

The **Universal Kinematic Protocol (UKP)** is an open-source hardware abstraction standard for modern physical robotics. It provides a vendor-neutral interface between high-level physical AI world models and heterogeneous robot hardware (6-DOF/7-DOF industrial arms, quadrupeds, wheeled AMRs, and bipedal humanoids).

## Quickstart for Hardware OEMs

```python
from terra_kinetics.protocol.ukp_schema import (
    HardwareAbstractionLayer,
    RobotMorphology,
    SafetyEnvelope,
)

# 1. Initialize HAL for your robot morphology
hal = HardwareAbstractionLayer(
    morphology=RobotMorphology.MANIPULATOR_6DOF,
    safety_envelope=SafetyEnvelope(max_joint_torque_nm=120.0),
)

# 2. Convert raw model tensors into normalized action tokens
action_token = hal.normalize_action(
    raw_action_tensor=[0.0, -1.57, 1.57, 0.0, 1.57, 0.0],
    joint_names=["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"],
)

# 3. Deterministically validate safety before transmission to actuators
is_valid, reason = hal.validate_command(action_token)
if is_valid:
    print("Action token validated for physical execution.")
```

## Key Capabilities

- **Sub-5ms Deterministic Latency**: Zero-allocation byte serialization for 200 Hz hard real-time control.
- **Dynamic Safety Envelopes**: Formal verification of joint torques, velocity limits, and 3D Euclidean bounding volumes.
- **Uncertainty Fallback Hooks**: Seamless integration with shadow tele-operation and compliance braking.
