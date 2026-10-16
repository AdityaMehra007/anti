"""
VENTURE 02: Robotics & Vision AI Dataset Quality Assurance Copilot
===================================================================
Automates multi-modal bounding box and annotation schema validation to maintain
the 99%+ QA benchmark required for warehouse robotics and computer vision models.
"""

from typing import Any


class DatasetQAValidator:
    """Validates spatial coordinates, labels, and boundary conditions for ML training data."""

    def __init__(
        self,
        allowed_classes: list[str],
        min_box_size: int = 10,
        max_image_dims: tuple[int, int] = (1920, 1080),
    ):
        self.allowed_classes = set(allowed_classes)
        self.min_box_size = min_box_size
        self.max_width, self.max_height = max_image_dims

    def validate_dataset(self, frames: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Audits a batch of annotated frames.
        Frame: {"frame_id": str, "annotations": [{"class": str, "bbox": [x, y, w, h]}]}
        """
        total_annotations = 0
        total_valid = 0
        defects = []

        for frame in frames:
            fid = frame.get("frame_id", "unknown")
            for idx, ann in enumerate(frame.get("annotations", [])):
                total_annotations += 1
                cls_name = ann.get("class", "")
                bbox = ann.get("bbox", [])

                # Validation 1: Class existence
                if cls_name not in self.allowed_classes:
                    defects.append(
                        {
                            "frame_id": fid,
                            "annotation_idx": idx,
                            "type": "INVALID_CLASS",
                            "message": f"Class '{cls_name}' not in allowed taxonomy.",
                        }
                    )
                    continue

                # Validation 2: Bounding box format
                if len(bbox) != 4 or not all(isinstance(v, (int, float)) for v in bbox):
                    defects.append(
                        {
                            "frame_id": fid,
                            "annotation_idx": idx,
                            "type": "MALFORMED_BBOX",
                            "message": "Bounding box must contain 4 coordinates [x, y, w, h].",
                        }
                    )
                    continue

                x, y, w, h = bbox

                # Validation 3: Geometry & bounds
                if w < self.min_box_size or h < self.min_box_size:
                    defects.append(
                        {
                            "frame_id": fid,
                            "annotation_idx": idx,
                            "type": "DEGENERATE_BOX",
                            "message": f"Box dimensions ({w}x{h}) smaller than min threshold {self.min_box_size}px.",
                        }
                    )
                    continue

                if (
                    x < 0
                    or y < 0
                    or (x + w) > self.max_width
                    or (y + h) > self.max_height
                ):
                    defects.append(
                        {
                            "frame_id": fid,
                            "annotation_idx": idx,
                            "type": "OUT_OF_BOUNDS",
                            "message": f"Box exceeds frame dimensions ({self.max_width}x{self.max_height}).",
                        }
                    )
                    continue

                total_valid += 1

        qa_score = (
            round((total_valid / total_annotations) * 100, 2)
            if total_annotations > 0
            else 100.0
        )
        meets_sla = qa_score >= 99.0

        return {
            "total_frames_audited": len(frames),
            "total_annotations": total_annotations,
            "valid_annotations": total_valid,
            "defect_count": len(defects),
            "qa_compliance_percentage": qa_score,
            "meets_99_sla": meets_sla,
            "defects": defects[:10],  # Top 10 sample defects
        }


if __name__ == "__main__":
    taxonomy = [
        "robot_arm",
        "pallet",
        "forklift",
        "worker",
        "bin_tote",
        "safety_barrier",
    ]
    validator = DatasetQAValidator(allowed_classes=taxonomy)

    sample_frames = [
        {
            "frame_id": "FRAME_001_AERO_LOGISTICS",
            "annotations": [
                {"class": "robot_arm", "bbox": [100, 150, 250, 400]},
                {"class": "pallet", "bbox": [50, 600, 300, 150]},
                {"class": "worker", "bbox": [800, 200, 80, 220]},
            ],
        },
        {
            "frame_id": "FRAME_002_DRIFT_EDGE_CASE",
            "annotations": [
                {"class": "forklift", "bbox": [400, 300, 350, 280]},
                {
                    "class": "unknown_object",
                    "bbox": [200, 100, 50, 50],
                },  # Defect: not in taxonomy
                {
                    "class": "bin_tote",
                    "bbox": [1900, 500, 50, 50],
                },  # Defect: out of bounds
            ],
        },
    ]

    report = validator.validate_dataset(sample_frames)
    print("=== ROBOTICS AI DATASET QA REPORT ===")
    print(f"Total Annotations:    {report['total_annotations']}")
    print(f"Valid Annotations:    {report['valid_annotations']}")
    print(f"Defects Detected:     {report['defect_count']}")
    print(f"QA Accuracy Score:    {report['qa_compliance_percentage']}%")
    print(f"Meets 99% SLA:        {report['meets_99_sla']}")
