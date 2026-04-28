import json
from pathlib import Path


class ProgressStore:
    def __init__(self, path: str, course_id: str):
        self.path = Path(path).expanduser()
        self.course_id = course_id

    def default(self):
        return {
            "course_id": self.course_id,
            "completed_chapters": [],
            "block_progress": {},
            "scores": {},
            "reflections": {}
        }

    def load(self):
        if not self.path.exists():
            return self.default()

        data = json.loads(self.path.read_text(encoding="utf-8"))

        if data.get("course_id") != self.course_id:
            return self.default()

        return data

    def save(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def get_block_index(self, chapter_id: str) -> int:
        data = self.load()
        return data["block_progress"].get(chapter_id, 0)

    def set_block_index(self, chapter_id: str, index: int):
        data = self.load()
        data["block_progress"][chapter_id] = index
        self.save(data)

    def mark_chapter_complete(self, chapter_id: str):
        data = self.load()
        if chapter_id not in data["completed_chapters"]:
            data["completed_chapters"].append(chapter_id)
        self.save(data)

    def add_score(self, chapter_id: str, points: int):
        data = self.load()
        data["scores"][chapter_id] = data["scores"].get(chapter_id, 0) + points
        self.save(data)

    def save_reflection(self, chapter_id: str, question: str, answer: str):
        data = self.load()
        data["reflections"].setdefault(chapter_id, [])
        data["reflections"][chapter_id].append({
            "question": question,
            "answer": answer
        })
        self.save(data)

    def reset(self):
        self.save(self.default())
