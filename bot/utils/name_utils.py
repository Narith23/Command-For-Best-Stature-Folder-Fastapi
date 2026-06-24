"""Name formatting helpers."""

import re


def to_project_slug(name: str) -> str:
    """Convert a project name into a filesystem-friendly slug."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")

    return slug or "my_project"


def to_title(name: str) -> str:
    """Convert a project name into a readable title."""

    words = re.split(r"[^a-zA-Z0-9]+", name.strip())
    title = " ".join(word.capitalize() for word in words if word)

    return title or "My Project"
