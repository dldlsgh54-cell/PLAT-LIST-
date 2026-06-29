# Render System

Creator OS uses FFmpeg-based rendering.

Before the full render, Creator OS creates a 10-second Preview Render.

## Relaxing Render

Inputs and behavior:

- Master Playlist
- Ambient Profile
- Loop Video
- Repeat until target duration
- Natural crossfade

## Vocal Render

Inputs and behavior:

- Selected Tracks
- Images or Loop Videos
- Player UI
- Spectrum
- Subtitles
- Chapter generation

## Shorts Render

Inputs and behavior:

- Hook Segment
- Vertical Layout
- Subtitle
- Spectrum
- CTA

## Rules

- FFmpeg is the primary render backend.
- Preflight Check must pass before preview or full render.
- A 10-second Preview Render must be generated before the full render.
- Full render should require user approval after preview review.
- Render outputs should be non-destructive and written to managed output folders.
- Render jobs should report status, progress, errors, and output paths.

