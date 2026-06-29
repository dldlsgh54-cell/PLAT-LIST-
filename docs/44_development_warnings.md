# Development Warnings

These warnings should guide Creator OS implementation decisions.

## Warnings

1. Do not use Gemini alone to judge plagiarism.
2. Cache Gemini judgments and do not repeatedly evaluate the same audio.
3. Do not send long audio to Gemini all at once.
4. Run A/B comparisons track by track, two versions at a time.
5. Never modify original files.
6. Do not render vocal playlists under 60 minutes.
7. Do not trust file names alone. Manage assets by internal ID.
8. Check YouTube Retention API limits early in development.
9. Run FFmpeg renders in the background.
10. Always create a Preview Render before rendering a long video.

## Implementation Notes

- Gemini calls should use caching keyed by asset ID, file hash, prompt version, and model.
- Long audio should be summarized, segmented, or analyzed locally before Gemini evaluation.
- A/B evaluation should stay scoped to one track pair at a time.
- FFmpeg jobs should not block the GUI thread.
- Preview Render is required before Full Render.
- Internal IDs should remain stable when files are renamed or moved.

