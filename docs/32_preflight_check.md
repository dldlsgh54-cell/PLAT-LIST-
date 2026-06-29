# Preflight Check

Preflight Check must run before rendering.

If any check fails, rendering is blocked.

## Check Items

- Audio files exist
- Winner selection is complete
- Lyrics exist
- Subtitles are generated
- Images exist
- Video loop exists
- Brand rules pass
- Vocal project is at least 60 minutes
- No similarity risk
- No corrupted files
- Thumbnail exists
- Metadata exists

## Rules

- Rendering cannot start until all required checks pass.
- Failed checks should show clear reasons and affected files or tracks.
- Vocal projects under 60 minutes are blocked.
- Missing or corrupted source assets are blockers.
- AI recommendations cannot bypass Preflight Check.
- User approval cannot override hard render blockers unless a specific override rule is later defined.

