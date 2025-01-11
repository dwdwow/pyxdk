from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class PollOption:
    position: int
    label: str
    votes: int

@dataclass
class Poll:
    id: str
    voting_status: str
    duration_minutes: int
    options: List[PollOption]
    end_datetime: datetime

    @classmethod
    def from_dict(cls, data: dict) -> 'Poll':
        # Convert options to PollOption objects
        options = [
            PollOption(**option)
            for option in data['options']
        ]
        
        # Convert end_datetime string to datetime object
        end_datetime = datetime.strptime(data['end_datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        return cls(
            id=data['id'],
            voting_status=data['voting_status'],
            duration_minutes=data['duration_minutes'],
            options=options,
            end_datetime=end_datetime
        )

    # @classmethod
    # def from_api_response(cls, response: Dict) -> Dict[str, List]:
    #     """
    #     Creates Poll objects from a full API response
        
    #     Returns:
    #         Dict with 'data' and 'includes' keys containing lists of objects
    #     """
    #     result = {'data': [], 'includes': {'polls': []}}
        
    #     # Process polls in includes
    #     if 'includes' in response and 'polls' in response['includes']:
    #         result['includes']['polls'] = [
    #             cls.from_dict(poll_data) 
    #             for poll_data in response['includes']['polls']
    #         ]
            
        return result
