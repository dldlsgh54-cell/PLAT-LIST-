# Non-Destructive Workflow

Original files are never modified.

Creator OS uses separate folders for source files, working files, render outputs, and final exports.

## Folder Model

```text
Original/
Working/
Render/
Export/
```

## Folder Purpose

- `Original`: Read-only source files.
- `Working`: Temporary and transformed working files.
- `Render`: Rendered intermediate outputs and previews.
- `Export`: Final delivery files.

## Rules

- All conversions are performed in `Working`.
- Original files must remain recoverable at all times.
- Render and export operations must not overwrite source files.
- Reprocessing should start from `Original` or approved project state, not from destructive edits.
- Generated files should preserve links to their source asset IDs.
- The user should always be able to return to the original source files.

