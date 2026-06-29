# Core Rules

Creator OS follows these core rules across all workflows.

## Principles

1. Quality comes before length.
2. AI recommends, and the user gives final approval.
3. Original files are never modified.
4. Every operation is non-destructive.
5. Vocal playlists must be at least 60 minutes long.
6. Rendering is blocked when a vocal playlist is under 60 minutes.
7. Relaxing videos use a 50-70 minute master and loop it to the target duration.
8. Assets are managed by internal IDs instead of file names.
9. Long-form content and shorts must stay connected.
10. The program should learn the user's taste and successful patterns.

## Implementation Notes

- Source assets must be treated as read-only.
- Derived files should be written to managed output folders.
- Internal IDs should remain stable even when files are renamed or moved.
- Render validation must run before export begins.
- AI decisions should be stored as recommendations, not automatic approvals.
- Shorts should keep a relationship to the source track, playlist, or long-form render.

