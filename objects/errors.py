from dataclasses import dataclass

@dataclass
class Errors:
    # All fields are optional
    client_id: str | None = None
    required_enrollment: str | None = None
    registration_url: str | None = None
    title: str | None = None
    detail: str | None = None
    reason: str | None = None
    error_type: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Errors':
        return cls(
            client_id=data.get('client_id'),
            required_enrollment=data.get('required_enrollment'),
            registration_url=data.get('registration_url'),
            title=data.get('title'),
            detail=data.get('detail'),
            reason=data.get('reason'),
            error_type=data.get('type')
        )
