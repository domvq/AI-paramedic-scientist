from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VitalSigns:
    heart_rate: Optional[float] = None
    respiratory_rate: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    spo2: Optional[float] = None
    temperature: Optional[float] = None
    glucose: Optional[float] = None
    etco2: Optional[float] = None


@dataclass
class PatientCase:
    age: Optional[int] = None
    sex: str = "Not specified"

    chief_complaint: str = ""

    history: list[str] = field(default_factory=list)

    medications: list[str] = field(default_factory=list)

    vital_signs: VitalSigns = field(
        default_factory=VitalSigns
    )

    mental_status: str = ""

    physical_exam: str = ""

    treatments: list[str] = field(
        default_factory=list
    )

    def to_dict(self):
        return {
            "age": self.age,
            "sex": self.sex,
            "chief_complaint": self.chief_complaint,
            "history": self.history,
            "medications": self.medications,
            "vital_signs": {
                "heart_rate": self.vital_signs.heart_rate,
                "respiratory_rate": self.vital_signs.respiratory_rate,
                "systolic_bp": self.vital_signs.systolic_bp,
                "diastolic_bp": self.vital_signs.diastolic_bp,
                "spo2": self.vital_signs.spo2,
                "temperature": self.vital_signs.temperature,
                "glucose": self.vital_signs.glucose,
                "etco2": self.vital_signs.etco2,
            },
            "mental_status": self.mental_status,
            "physical_exam": self.physical_exam,
            "treatments": self.treatments,
        }