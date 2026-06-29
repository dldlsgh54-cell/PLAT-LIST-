# Suno Workspace

Creator OS assumes there is no Suno API integration.

The Suno Workspace is a manual-assist screen that helps the user create tracks in Suno consistently.

## Screen Fields

- Track number
- Real title
- Lyrics
- Suno prompt
- Copy Lyrics
- Copy Prompt
- Open Suno
- Next Track

## Naming Rule

Files are managed by track number names:

```text
Track01
Track02
Track03
```

Real song titles are stored in the database.

## Rules

- The user copies lyrics and prompts into Suno manually.
- Creator OS should not depend on a Suno API.
- Suno output files should use track number names such as `Track01` and `Track02`.
- The actual title is project metadata, not the file identity.
- A/B import should match files by track number.
- `Next Track` moves the user through the prepared Suno work list.

## Purpose

- Keep Suno generation organized.
- Reduce naming mistakes.
- Preserve real titles separately from file names.
- Support the A/B import system without requiring Suno integration.

