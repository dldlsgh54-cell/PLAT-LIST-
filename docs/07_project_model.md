# Project Model

Creator OS manages work as an Album or Playlist project, not as a single video file.

Each project contains tracks, versions, lyrics, visual assets, subtitle output, long-form video output, shorts, metadata, and upload data.

## Album Project Structure

```text
Album Project/
|-- Track01/
|   |-- Version A/
|   `-- Version B/
|-- Track02/
|   |-- Version A/
|   `-- Version B/
|-- Lyrics/
|-- Images/
|-- Subtitles/
|-- Long Video/
|-- Shorts/
|-- Metadata/
|-- Upload Data/
`-- project.db
```

## Rules

- A project represents an album or playlist production unit.
- Tracks can have A/B versions.
- Version A and Version B are evaluated before final track approval.
- Long-form videos and shorts are derived from the same project.
- Project metadata and upload data belong to the project.
- Each project has its own `project.db`.
- `project.db` stores project-local state, decisions, analysis results, render status, and asset relationships.

