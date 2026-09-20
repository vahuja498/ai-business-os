from enum import Enum


class AutonomyLevel(str, Enum):
    LEVEL_0_OBSERVE = "LEVEL_0_OBSERVE"
    LEVEL_1_ASSIST = "LEVEL_1_ASSIST"
    LEVEL_2_CONTROLLED_AUTONOMY = "LEVEL_2_CONTROLLED_AUTONOMY"
    LEVEL_3_HIGH_AUTONOMY = "LEVEL_3_HIGH_AUTONOMY"

    @classmethod
    def can_execute_autonomously(cls, current_level: "AutonomyLevel", required_level: "AutonomyLevel") -> bool:
        hierarchy = {
            cls.LEVEL_0_OBSERVE: 0,
            cls.LEVEL_1_ASSIST: 1,
            cls.LEVEL_2_CONTROLLED_AUTONOMY: 2,
            cls.LEVEL_3_HIGH_AUTONOMY: 3,
        }
        return hierarchy[current_level] >= hierarchy[required_level]
