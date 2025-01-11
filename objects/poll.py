from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class VotingStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"

@dataclass
class PollOption:
    position: int
    label: str
    votes: int

@dataclass
class Poll:
    # Required fields
    id: str
    options: list[PollOption]
    voting_status: VotingStatus
    
    # Optional fields
    duration_minutes: int | None = None
    end_datetime: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Poll':
        # Convert options array to list of PollOption objects
        options = [
            PollOption(
                position=option['position'],
                label=option['label'],
                votes=option['votes']
            )
            for option in data['options']
        ]
        
        # Convert voting status string to enum
        voting_status = VotingStatus(data['voting_status'])
        
        # Convert end_datetime string to datetime object if present
        end_datetime = None
        if 'end_datetime' in data and data['end_datetime']:
            end_datetime = datetime.strptime(
                data['end_datetime'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        
        return cls(
            id=data['id'],
            options=options,
            voting_status=voting_status,
            duration_minutes=data.get('duration_minutes'),
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
