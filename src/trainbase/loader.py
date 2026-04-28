from pathlib import Path
import requests
import yaml


class CourseLoader:
    def load_text(self, path: str) -> str:
        raise NotImplementedError

    def load_yaml(self, path: str):
        return yaml.safe_load(self.load_text(path))


class LocalCourseLoader(CourseLoader):
    def __init__(self, root_path: str):
        self.root = Path(root_path).expanduser().resolve()

    def load_text(self, path: str) -> str:
        file_path = self.root / path
        return file_path.read_text(encoding="utf-8")


class GitHubCourseLoader(CourseLoader):
    def __init__(self, repo_url: str, branch: str = "main"):
        self.repo_url = repo_url.rstrip("/")
        self.branch = branch
        self.raw_base = self._to_raw_url(repo_url, branch)

    def _to_raw_url(self, repo_url: str, branch: str) -> str:
        if "github.com" not in repo_url:
            raise ValueError("GitHubCourseLoader only supports github.com URLs.")

        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1]

        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"

    def load_text(self, path: str) -> str:
        url = f"{self.raw_base}/{path}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text


def make_loader(source: str, branch: str = "main") -> CourseLoader:
    if source.startswith("http://") or source.startswith("https://"):
        if "github.com" in source:
            return GitHubCourseLoader(source, branch=branch)
        raise ValueError("Only GitHub URLs are supported in v0.1.")

    return LocalCourseLoader(source)
