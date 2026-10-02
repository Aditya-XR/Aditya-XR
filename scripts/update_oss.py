"""Refresh the open-source section of README.md from GitHub.

Lists the pull requests I opened in repositories owned by someone else: merged ones
first, then the ones still in review. Closed-without-merge and draft PRs are left out.
Only the text between the marker comments is rewritten (the table between OSS:START and
OSS:END, the merged count between MERGED:START and MERGED:END), so the rest of the
README stays hand-written.

Usage: GITHUB_TOKEN=... python3 scripts/update_oss.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "Aditya-XR")
README = Path(__file__).resolve().parent.parent / "README.md"

QUERY = """
query($q: String!, $cursor: String) {
  search(query: $q, type: ISSUE, first: 100, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number title url state isDraft merged mergedAt createdAt
        repository { nameWithOwner url stargazerCount }
      }
    }
  }
}
"""


def graphql(token: str, variables: dict) -> dict:
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{USER}-profile-readme",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.load(response)
    if body.get("errors"):
        raise RuntimeError(f"GitHub GraphQL error: {body['errors']}")
    return body["data"]["search"]


def fetch_pull_requests(token: str) -> list[dict]:
    pulls, cursor = [], None
    while True:
        page = graphql(token, {"q": f"is:pr author:{USER} -user:{USER}", "cursor": cursor})
        pulls += [node for node in page["nodes"] if node]
        if not page["pageInfo"]["hasNextPage"]:
            return pulls
        cursor = page["pageInfo"]["endCursor"]


def stars(count: int) -> str:
    if count >= 1000:
        return f"★ {count / 1000:.1f}k".replace(".0k", "k")
    return f"★ {count}" if count else ""


def clean_title(title: str) -> str:
    """Drop project-convention prefixes such as "Python:", "fix(redis):" or "[SourceKit]"."""
    title = re.sub(r"^(\[[^\]]+\]\s*)+", "", title.strip())
    title = re.sub(r"^[A-Za-z.]+(\([^)]*\))?!?:\s+", "", title)
    title = title.rstrip(".").replace("|", "\\|").replace("\n", " ")
    return title[:1].upper() + title[1:]


def split(pulls: list[dict]) -> tuple[list[dict], list[dict]]:
    merged = [p for p in pulls if p["merged"]]
    in_review = [p for p in pulls if p["state"] == "OPEN" and not p["isDraft"]]
    # Bigger projects first, newest first within a project.
    merged.sort(key=lambda p: p["mergedAt"], reverse=True)
    merged.sort(key=lambda p: p["repository"]["stargazerCount"], reverse=True)
    in_review.sort(key=lambda p: p["createdAt"], reverse=True)
    in_review.sort(key=lambda p: p["repository"]["stargazerCount"], reverse=True)
    return merged, in_review


def render_count(merged: list[dict]) -> str:
    return f"{len(merged)} merged pull request{'s' if len(merged) != 1 else ''}"


def render_group(heading: str, pulls: list[dict]) -> list[str]:
    """One table row per project, its pull requests stacked in a single cell."""
    if not pulls:
        return []
    by_project: dict[str, list[dict]] = {}
    for pull in pulls:  # already sorted, so dict order is display order
        by_project.setdefault(pull["repository"]["nameWithOwner"], []).append(pull)
    lines = [heading, "", "| Project | Pull requests |", "| :-- | :-- |"]
    for name, project_pulls in by_project.items():
        repo = project_pulls[0]["repository"]
        project = f"[{name}]({repo['url']})"
        if star_text := stars(repo["stargazerCount"]):
            project += f"<br><sub>{star_text}</sub>"
        links = "<br>".join(f"[{clean_title(p['title'])}]({p['url']})" for p in project_pulls)
        lines.append(f"| {project} | {links} |")
    return lines + [""]


def render_table(merged: list[dict], in_review: list[dict]) -> str:
    projects = len({p["repository"]["nameWithOwner"] for p in merged})
    lines = render_group(
        f"**✅ Merged** — {len(merged)} pull request{'s' if len(merged) != 1 else ''}"
        f" in {projects} project{'s' if projects != 1 else ''}",
        merged,
    )
    lines += render_group(f"**🔄 In review** — {len(in_review)} open", in_review)
    lines.append("<sub>Both tables refresh daily from the GitHub API.</sub>")
    return "\n".join(lines)


def replace_between(text: str, name: str, content: str) -> str:
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    head, found_start, rest = text.partition(start)
    _, found_end, tail = rest.partition(end)
    if not (found_start and found_end):
        raise ValueError(f"README is missing the {start} / {end} markers")
    return f"{head}{start}{content}{end}{tail}"


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 1
    readme = README.read_text(encoding="utf-8")
    merged, in_review = split(fetch_pull_requests(token))
    updated = replace_between(readme, "MERGED", render_count(merged))
    updated = replace_between(updated, "OSS", f"\n{render_table(merged, in_review)}\n")
    if updated == readme:
        print("Open-source section is already up to date")
        return 0
    README.write_text(updated, encoding="utf-8", newline="\n")
    print("Open-source section updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
