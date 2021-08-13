from enum import Enum


class TaskStatus(Enum):
    OPEN = 'open'
    SUBSCRIBED = 'subscribed'
    COMPLETED = 'completed'
    APPROVED = 'approved'
