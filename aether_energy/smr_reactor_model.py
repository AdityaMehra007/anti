"""
Aether Energy-Compute: Micro-SMR & Direct Thermal-Compute Coupling Model.
Models collocated High-Temperature Gas-Cooled Small Modular Reactors (HTGR)
powering gigawatt-scale AI inference clusters with zero transmission grid dependence.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SMRModuleSpecification:
    thermal_power_mwth: float = 160.0
    electric_power_mwe: float = 65.0
    core_outlet_temp_c: float = 750.0
    capacity_factor: float = 0.95
    fuel_cycle_months: int = 48
    waste_heat_recovery_efficiency: float = 0.35


@dataclass
class CollocatedDataCenterCluster:
    cluster_name: str
    num_smr_units: int
    total_compute_flops_exaflops: float
    annual_pue: float = 1.08  # Ultra-efficient direct liquid cooling from SMR secondary loop


class AetherThermalComputePlant:
    """
    Coupled Nuclear-AI cluster calculating continuous clean baseload compute generation.
    """

    def __init__(self, smr_spec: SMRModuleSpecification = None):
        self.smr_spec = smr_spec or SMRModuleSpecification()

    def calculate_cluster_capacity(self, num_reactors: int) -> Dict[str, float]:
        total_mwe = num_reactors * self.smr_spec.electric_power_mwe * self.smr_spec.capacity_factor
        annual_mwh = total_mwe * 8760.0

        # Assuming 1 MW powers ~350 Nvidia Blackwell B200 SXM nodes
        total_gpu_nodes = int(total_mwe * 350)
        # Each B200 delivers ~20 PFLOPS FP4 AI compute
        total_compute_exaflops = (total_gpu_nodes * 20.0) / 1000.0

        return {
            "num_reactors": num_reactors,
            "continuous_clean_power_mwe": round(total_mwe, 1),
            "annual_generation_mwh": round(annual_mwh, 1),
            "collocated_ai_gpu_nodes": total_gpu_nodes,
            "total_ai_compute_exaflops": round(total_compute_exaflops, 2),
            "grid_transmission_losses_pct": 0.0,  # Zero public grid transit
        }
