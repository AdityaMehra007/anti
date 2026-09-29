"""
Domain Randomization Engine for Sim-to-Real Transfer.
Injects controlled parameter variances into physics simulation to bridge the Reality Gap.
"""

from dataclasses import dataclass
import random
from typing import Dict, Tuple


@dataclass
class RandomizedPhysicsEnvironment:
    friction_coefficient: float
    restitution: float
    link_mass_multiplier: float
    joint_damping_multiplier: float
    actuator_backlash_rad: float
    camera_latency_jitter_ms: float
    ambient_lux: float
    sensor_noise_sigma: float


class DomainRandomizer:
    """
    Applies Gaussian and Uniform randomization across physical parameters
    to generate resilient sim-to-real transfer policies.
    """

    def __init__(
        self,
        friction_range: Tuple[float, float] = (0.2, 1.4),
        mass_variance_pct: float = 0.15,
        latency_jitter_range_ms: Tuple[float, float] = (0.5, 8.0),
        ambient_lux_range: Tuple[float, float] = (150.0, 1500.0),
    ):
        self.friction_range = friction_range
        self.mass_variance_pct = mass_variance_pct
        self.latency_jitter_range_ms = latency_jitter_range_ms
        self.ambient_lux_range = ambient_lux_range

    def sample_environment(self, seed: int = None) -> RandomizedPhysicsEnvironment:
        """
        Samples a randomized physical environment parameter vector.
        """
        if seed is not None:
            random.seed(seed)

        return RandomizedPhysicsEnvironment(
            friction_coefficient=random.uniform(*self.friction_range),
            restitution=random.uniform(0.01, 0.45),
            link_mass_multiplier=random.uniform(1.0 - self.mass_variance_pct, 1.0 + self.mass_variance_pct),
            joint_damping_multiplier=random.uniform(0.85, 1.35),
            actuator_backlash_rad=random.gauss(0.0, 0.003),
            camera_latency_jitter_ms=random.uniform(*self.latency_jitter_range_ms),
            ambient_lux=random.uniform(*self.ambient_lux_range),
            sensor_noise_sigma=random.uniform(0.001, 0.012),
        )

    def perturb_telemetry(self, values: list[float], env: RandomizedPhysicsEnvironment) -> list[float]:
        """
        Injects real-world sensor noise and actuator drift into telemetry.
        """
        return [v + random.gauss(0.0, env.sensor_noise_sigma) for v in values]
