import time
from app.lib.jawnt.queue import message_queue

def process_task(task_type: str, payload: dict):
    print(f"Processing {task_type} task...")
    time.sleep(1)  # Simulate processing time
    print(f"✅ Done with task: {payload}")

def run_queue_consumer():
    print("🔁 Starting queue consumer...")
    while not message_queue.is_empty():
        task = message_queue.consume()
        if task:
            task_id, payload = task
            print(f"🔧 Consuming task {task_id}: {payload}")
            process_task(payload.get("type", "UNKNOWN"), payload)
        else:
            print("🚫 No tasks to consume.")
    print("🎉 All tasks consumed.")

if __name__ == "__main__":
    run_queue_consumer()