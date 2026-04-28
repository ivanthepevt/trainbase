from IPython.display import display, HTML, Markdown

from .loader import make_loader
from .parser import parse_blocks
from .progress import ProgressStore
from .renderer import render_blocks


def learn(source, branch="main", progress_path="trainbase_progress.json"):
    loader = make_loader(source, branch=branch)
    course_data = loader.load_yaml("course.yaml")
    progress_store = ProgressStore(progress_path, course_data["id"])
    return Course(loader, course_data, progress_store)


class Course:
    def __init__(self, loader, course_data, progress_store):
        self.loader = loader
        self.course_data = course_data
        self.progress_store = progress_store

    @property
    def agenda(self):
        progress = self.progress_store.load()
        rows = []

        for chapter in self.course_data.get("chapters", []):
            chapter_id = chapter["id"]

            if chapter_id in progress["completed_chapters"]:
                status = "completed"
            elif self._is_unlocked(chapter_id):
                status = "available"
            else:
                status = "locked"

            rows.append({
                "id": chapter_id,
                "title": chapter.get("title", chapter_id),
                "description": chapter.get("description", ""),
                "status": status
            })

        return rows

    def show_agenda(self):
        rows = self.agenda

        html = f"""
        <h2>{self.course_data.get("title", "Course")}</h2>
        <p>{self.course_data.get("description", "")}</p>
        <table border="1" cellpadding="8" cellspacing="0">
          <tr>
            <th>Chapter</th>
            <th>Title</th>
            <th>Description</th>
            <th>Status</th>
          </tr>
        """

        for row in rows:
            html += f"""
            <tr>
              <td>{row["id"]}</td>
              <td>{row["title"]}</td>
              <td>{row["description"]}</td>
              <td>{row["status"]}</td>
            </tr>
            """

        html += "</table>"
        display(HTML(html))

    def play(self, chapter_id):
        if not self._is_unlocked(chapter_id):
            chapter = self._get_chapter(chapter_id)
            prereqs = chapter.get("unlock_after", [])
            display(Markdown(f"## 🔒 `{chapter_id}` is locked"))
            display(Markdown(f"Complete first: `{', '.join(prereqs)}`"))
            return

        chapter = self._get_chapter(chapter_id)
        markdown_text = self.loader.load_text(chapter["path"])
        blocks = parse_blocks(markdown_text)

        display(Markdown(f"# {chapter.get('title', chapter_id)}"))
        render_blocks(chapter_id, blocks, self.progress_store)

    def progress(self):
        return self.progress_store.load()

    def reset(self):
        self.progress_store.reset()
        display(Markdown("## Progress reset."))

    def certificate(self, learner_name):
        progress = self.progress_store.load()
        all_chapter_ids = [c["id"] for c in self.course_data.get("chapters", [])]

        if not all(cid in progress["completed_chapters"] for cid in all_chapter_ids):
            display(Markdown("## ❌ Finish all chapters before generating a certificate."))
            return

        total_score = sum(progress.get("scores", {}).values())

        html = f"""
        <div style="border:2px solid #222; padding:28px; margin:16px 0; text-align:center;">
          <h1>Certificate of Completion</h1>
          <p>This certifies that</p>
          <h2>{learner_name}</h2>
          <p>has completed</p>
          <h2>{self.course_data.get("title", "Course")}</h2>
          <p>Total score: <strong>{total_score}</strong></p>
        </div>
        """
        display(HTML(html))

    def _get_chapter(self, chapter_id):
        for chapter in self.course_data.get("chapters", []):
            if chapter["id"] == chapter_id:
                return chapter
        raise ValueError(f"Chapter not found: {chapter_id}")

    def _is_unlocked(self, chapter_id):
        chapter = self._get_chapter(chapter_id)
        progress = self.progress_store.load()
        prereqs = chapter.get("unlock_after", [])
        return all(prereq in progress["completed_chapters"] for prereq in prereqs)
