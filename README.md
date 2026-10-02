<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Aditya Kumar — Backend · Real-time systems · Open source. B.Tech CSE, BIT Mesra ’27, open to SDE-1 / new-grad roles." src="assets/banner-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/aditya-kumar-37b82627b"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Aditya_Kumar-0A66C2?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0yMC40NDcgMjAuNDUyaC0zLjU1NHYtNS41NjljMC0xLjMyOC0uMDI3LTMuMDM3LTEuODUyLTMuMDM3LTEuODUzIDAtMi4xMzYgMS40NDUtMi4xMzYgMi45Mzl2NS42NjdIOS4zNTFWOWgzLjQxNHYxLjU2MWguMDQ2Yy40NzctLjkgMS42MzctMS44NSAzLjM3LTEuODUgMy42MDEgMCA0LjI2NyAyLjM3IDQuMjY3IDUuNDU1djYuMjg2ek01LjMzNyA3LjQzM2EyLjA2MiAyLjA2MiAwIDEgMSAwLTQuMTI1IDIuMDYyIDIuMDYyIDAgMCAxIDAgNC4xMjV6TTcuMTE5IDIwLjQ1MkgzLjU1NVY5aDMuNTY0djExLjQ1MnpNMjIuMjI1IDBIMS43NzFDLjc5MiAwIDAgLjc3NCAwIDEuNzI5djIwLjU0MkMwIDIzLjIyNy43OTIgMjQgMS43NzEgMjRoMjAuNDUxQzIzLjIgMjQgMjQgMjMuMjI3IDI0IDIyLjI3MVYxLjcyOUMyNCAuNzc0IDIzLjIgMCAyMi4yMjIgMGguMDAzeiIvPjwvc3ZnPg=="></a>
  <a href="mailto:adityaccds@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-adityaccds%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white"></a>
  <a href="https://leetcode.com/u/adityaccds/"><img alt="LeetCode" src="https://img.shields.io/badge/LeetCode-adityaccds-FFA116?style=for-the-badge&logo=leetcode&logoColor=black"></a>
  <a href="https://collaborative-editor-flax.vercel.app"><img alt="Live demo: CollabEdit" src="https://img.shields.io/badge/Live_demo-CollabEdit-2EA44F?style=for-the-badge&logo=vercel&logoColor=white"></a>
</p>

I'm a final-year Computer Science student at **BIT Mesra** (graduating **May 2027**), looking for **SDE-1 / new-grad** software engineering roles.
I like the backend side of real-time products — sync protocols, storage, rate limiting, and the bugs that hide in shared state — and I fix those bugs in other people's code too: my patches are merged in **Microsoft's Agent Framework** and **LibreDB Studio**.

- 🔀 **<!-- MERGED:START -->5 merged pull requests<!-- MERGED:END -->** in open source, including fixes in [microsoft/agent-framework](https://github.com/microsoft/agent-framework) — with more in review at pytest, Swift, Mermaid and Zulip
- 🚀 **[CollabEdit](https://github.com/Aditya-XR/collaborative-editor)** — a live Google Docs–style editor on a CRDT sync server I wrote in Python, with 250+ automated tests
- 🏆 **70th of 8,500+ teams** in the Amazon ML Challenge 2026 · 🥇 **1st place** at Hatch From Scratch (AR indoor navigation)
- 🧮 **600+ DSA problems** solved in C++ · LeetCode contest rating peaked at **1605**

## 🚀 Featured project — CollabEdit

Real-time collaborative documents in the spirit of Google Docs — live cursors, offline editing, version history, full-text search and link sharing — built from scratch on FastAPI, Yjs/pycrdt, PostgreSQL and Redis.

<a href="https://collaborative-editor-flax.vercel.app"><img src="assets/collabedit.png" alt="CollabEdit: two people editing the same document. Rahul's caret and name appear live in Priya's window, with both avatars and All changes synced in the header." width="100%"></a>

**[▶ Try it live](https://collaborative-editor-flax.vercel.app)** · [Source](https://github.com/Aditya-XR/collaborative-editor) · [Design decisions (ADRs)](https://github.com/Aditya-XR/collaborative-editor/tree/main/docs/adr) · [Roadmap](https://github.com/Aditya-XR/collaborative-editor/blob/main/docs/PLAN.md)

- **Own sync server.** FastAPI WebSockets speak the Yjs sync and awareness protocols on top of pycrdt (Rust Yrs): one room per open document, per-connection send queues, and roles enforced on every update. In production, edits reach other users in about 110 ms.
- **Edit log + compaction.** Every edit lands in an append-only Postgres log (batched every 500 ms) and is folded into snapshots under an advisory lock — opening a 10,000-keystroke document went from **218 ms to 17 ms**.
- **Self-built rate limiter.** A token bucket in one Redis Lua script: atomic across API instances, in a single round trip.
- **Careful sessions.** Argon2id passwords, 15-minute JWTs, rotating refresh tokens with reuse detection, and one-time WebSocket tickets.
- **Offline-first.** The browser keeps an IndexedDB copy, and offline edits merge automatically when the connection returns.
- **Tested and documented.** 173 API tests against real Postgres and Redis (including Hypothesis convergence properties) and 79 web tests run in CI on every push; 10 architecture decision records explain the trade-offs.

## 🔧 Open source

I look for real bugs in projects I use, reduce them to a minimal reproduction, and fix them with regression tests. Some favourites:

- **[microsoft/agent-framework #8660](https://github.com/microsoft/agent-framework/pull/8660)** — `is_type_compatible` special-cased `Any` only as a target type, so workflow edge validation rejected executors declaring `WorkflowContext[Any]`.
- **[microsoft/agent-framework #8648](https://github.com/microsoft/agent-framework/pull/8648)** — middleware type detection failed under `from __future__ import annotations`; postponed (PEP 563) annotations are now resolved before dispatch.
- **[libredb/libredb-studio #1121](https://github.com/libredb/libredb-studio/pull/1121)** — a single `SELECT`, `AUTH` or `HELLO` could silently move or re-authenticate the Redis connection shared by every later request; blocked at the provider boundary after verifying each command against live Redis 8.

<!-- OSS:START -->
**✅ Merged** — 5 pull requests in 3 projects

| Project | Pull requests |
| :-- | :-- |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework)<br><sub>★ 13.9k</sub> | [Fix middleware type detection with postponed annotations](https://github.com/microsoft/agent-framework/pull/8648)<br>[Fix type compatibility for Any source types](https://github.com/microsoft/agent-framework/pull/8660) |
| [libredb/libredb-studio](https://github.com/libredb/libredb-studio)<br><sub>★ 1k</sub> | [Refuse commands that move the shared connection](https://github.com/libredb/libredb-studio/pull/1121)<br>[Anchor schema diff migration copy button outside scroll area](https://github.com/libredb/libredb-studio/pull/1082) |
| [anishmehta24/OSS-Contributor-engine](https://github.com/anishmehta24/OSS-Contributor-engine) | [Preserve CRLF line endings when applying edits](https://github.com/anishmehta24/OSS-Contributor-engine/pull/3) |

**🔄 In review** — 7 open

| Project | Pull requests |
| :-- | :-- |
| [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid)<br><sub>★ 90.5k</sub> | [Allow milestones to be declared without a duration](https://github.com/mermaid-js/mermaid/pull/8291) |
| [swiftlang/swift](https://github.com/swiftlang/swift)<br><sub>★ 70.4k</sub> | [Document source.request.relatedidents](https://github.com/swiftlang/swift/pull/92586) |
| [zulip/zulip](https://github.com/zulip/zulip)<br><sub>★ 26k</sub> | [Fix API URL in Home Assistant documentation](https://github.com/zulip/zulip/pull/40197)<br>[Replace deprecated URI with URL in avatar/logo settings](https://github.com/zulip/zulip/pull/40191) |
| [pytest-dev/pytest](https://github.com/pytest-dev/pytest)<br><sub>★ 14.6k</sub> | [Fix `WarningsRecorder.pop()` returning the last match for unrelated categories](https://github.com/pytest-dev/pytest/pull/15098) |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework)<br><sub>★ 13.9k</sub> | [Fix tool argument validation for datetime, set and tuple parameters](https://github.com/microsoft/agent-framework/pull/8824) |
| [libredb/libredb-studio](https://github.com/libredb/libredb-studio)<br><sub>★ 1k</sub> | [Read DATE and TIMESTAMP as the stored wall clock, not a local Date](https://github.com/libredb/libredb-studio/pull/1225) |

<sub>Both tables refresh daily from the GitHub API.</sub>
<!-- OSS:END -->

## 🧩 More projects

| Project | What it is | Built with |
| :-- | :-- | :-- |
| [**WebChat**](https://github.com/Aditya-XR/webChat) | Real-time one-to-one chat with contact invites, blocking, read receipts and presence. Messages are persisted before the Socket.IO emit, so history and unread counts survive disconnects | React · Express · Socket.IO · MongoDB |
| [**Rehabilitation**](https://github.com/Aditya-XR/Rehabilitation) | Booking system for a rehab centre. A MongoDB transaction claims each slot with one conditional update — of 8 simultaneous requests for a slot, exactly one wins | React 19 · Express 5 · MongoDB |
| [**Primetrade-Assignment**](https://github.com/Aditya-XR/Primetrade-Assignment) | Task-management REST API with JWT auth and role-based access, documented with Postman | Node.js · Express · MongoDB |

## 🧰 Tech

<p>
  <img alt="Python, TypeScript, JavaScript, C++, C, FastAPI, Node.js, Express, React, Tailwind CSS, PostgreSQL, Redis, MongoDB, Docker, GitHub Actions, Linux, Git" src="https://skillicons.dev/icons?i=python,ts,js,cpp,c,fastapi,nodejs,express,react,tailwind,postgres,redis,mongodb,docker,githubactions,linux,git&perline=9">
</p>

**Also:** SQLAlchemy · Alembic · WebSockets · Socket.IO · Yjs / CRDTs · JWT · OAuth 2.0 · pytest · Hypothesis · Vitest · Render · Vercel

**CS fundamentals:** data structures & algorithms, operating systems, computer networks, DBMS

---

<p align="center">
  📫 <a href="mailto:adityaccds@gmail.com">adityaccds@gmail.com</a> · <a href="https://www.linkedin.com/in/aditya-kumar-37b82627b">LinkedIn</a> — happy to talk about backend roles, real-time systems, or anything above.
</p>
