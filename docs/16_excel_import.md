# Excel Import

Creator OS supports Excel lyrics upload for vocal projects.

## Supported Formats

### Basic Lyrics Format

```text
No | Title | Style | Lyrics
```

### A/B Lyrics Format

```text
No | Title | Style | Lyrics A | Lyrics B
```

## Track Count

- Projects must support 20 or more tracks.
- Additional tracks such as `Track21`, `Track22`, and beyond must be supported.
- Track count should not be hard-coded to 20.

## Import Rules

- `No` becomes the track number source.
- `Title` is stored as the real song title in the database.
- `Style` is used to help generate Suno prompts and classify the track.
- `Lyrics` stores the original lyric text for the track.
- `Lyrics A` and `Lyrics B` allow alternate lyric versions for the same track.
- Imported lyrics become the source of truth for subtitle generation.

## Naming

Imported rows are mapped to track identifiers:

```text
Track01
Track02
Track03
...
Track21
Track22
```

The real title is stored separately from the file name.

