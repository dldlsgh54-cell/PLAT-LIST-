# Ambient Scanner

Ambient Scanner analyzes user-provided ambient sound folders and prepares them for Room Profiles and Journey Profiles.

## Input

- User-selected ambient folder

## Processing

- Scan all audio files
- Run Python analysis
- Run Gemini classification
- Automatically tag categories
- Analyze loop suitability
- Assign quality score
- Check duplicates

## Gemini Result Example

```json
{
  "category": "Rain",
  "subcategory": "Window Rain",
  "intensity": "Medium",
  "mood": "Cozy",
  "loop_quality": 95,
  "quality": 94
}
```

## Rules

- Classification should not depend only on file names.
- Python analysis should detect audio properties, quality, silence, clipping, and loop suitability.
- Gemini should classify mood, category, subcategory, and contextual usefulness.
- Duplicate checks should use audio fingerprints or similarity analysis.
- Low-quality or non-loopable files should be flagged before use in Rest Studio.
- Tagged ambient files become available for Room Profiles and Journey Profiles.

