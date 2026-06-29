# Hook Finder

Hook Finder is a core feature for Shorts production.

It identifies the strongest short-form sections from a source track or long-form video.

## Python Analysis

- Volume rise sections
- Chorus candidates
- Energy peaks
- Repeated structure
- Segment length

## Gemini Evaluation

- Emotional climax
- Lyric impact
- Chorus appeal
- Shorts suitability
- Viral potential

## Result Example

```text
Recommended segment: 00:48-01:18
Hook Score: 98
```

## Rules

- Hook candidates should fit the supported Shorts durations: 20, 30, 45, and 60 seconds.
- Python analysis should propose measurable candidate regions.
- Gemini should evaluate emotional and audience-facing strength.
- Final user approval is required before render or upload.
- Hook Finder should preserve links to the source long-form video, track, and project.

