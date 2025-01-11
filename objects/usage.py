from dataclasses import dataclass
from typing import Optional

@dataclass
class Usage:
    cap_reset_day: int
    project_cap: str
    project_id: str
    project_usage: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Usage':
        """
        Creates a Usage object from a dictionary
        
        Args:
            data: Dictionary containing usage information from Twitter API response
            
        Returns:
            Usage object with project usage information
        """
        if not data:
            return cls(
                cap_reset_day=0,
                project_cap="0",
                project_id="",
                project_usage="0"
            )
            
        return cls(
            cap_reset_day=data['cap_reset_day'],
            project_cap=data['project_cap'],
            project_id=data['project_id'],
            project_usage=data['project_usage']
        )
