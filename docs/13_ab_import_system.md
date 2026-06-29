# A/B Import System

Users do not manually place files into A and B slots.

Suno creates two songs with the same track title, and Creator OS automatically classifies them as Version A and Version B.

## Example

Input files from Suno:

```text
Track01
Track01
```

Creator OS classification:

```text
Track01 Version A
Track01 Version B
```

## Supported Input

- Drag and drop multiple files at once
- Watch the project `Downloads` folder
- Automatically match files
- Show missing files
- Show corrupted files

## Matching Rules

- Files with the same normalized track title are grouped together.
- The first valid file in a matched pair becomes Version A.
- The second valid file in a matched pair becomes Version B.
- If only one file exists for a track, the missing version is shown.
- If more than two files match the same track, the project should flag the extra files for user review.
- Corrupted or unreadable files should not be assigned as winners.

## Workflow

1. User generates two Suno outputs with the same track title.
2. User drags files into Creator OS or places them in the project `Downloads` folder.
3. Creator OS scans and normalizes track names.
4. Creator OS groups matching files.
5. Creator OS assigns Version A and Version B.
6. Creator OS displays missing, extra, or corrupted files.

