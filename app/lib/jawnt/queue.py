import uuid
from collections import deque
from typing import Any, Dict, Optional, Tuple

class MessageQueue:
    def __init__(self):
        self.queue = deque()

    def publish(self, payload: Dict[str, Any]) -> str:
        """
        Add a task to the queue. Returns a unique task ID.
        """
        task_id = str(uuid.uuid4())
        self.queue.append((task_id, payload))
        print(f"Queued task {task_id}: {payload}")
        return task_id

    def consume(self) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Remove and return the next task from the queue.
        Returns (task_id, payload) or None if queue is empty.
        """
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self) -> bool:
        return len(self.queue) == 0

message_queue = MessageQueue()