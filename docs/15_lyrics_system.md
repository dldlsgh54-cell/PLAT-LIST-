# Lyrics System

Creator OS does not retrieve lyrics from Suno.

The original lyrics are stored and managed by Creator OS. Suno is only used as a tool to turn those lyrics into songs.

## Source of Truth

- Creator OS stores the original English lyrics.
- Suno output is not treated as the lyrics source.
- The database tracks the relationship between lyrics, tracks, versions, and selected winners.

## Subtitle Generation

Inputs:

- Original English lyrics
- Selected winner audio
- Forced alignment

Outputs:

- SRT
- ASS

## Rules

- Whisper-style transcription is not the main subtitle method.
- To avoid transcription typos, subtitle text comes from the original lyrics.
- Forced alignment is used to match the original lyrics to timing.
- Subtitles are generated only from approved or selected winner audio.
- Generated subtitle files should remain linked to the source lyrics and winner version.

## Purpose

- Prevent lyric drift and transcription errors.
- Keep subtitle text consistent with the intended song.
- Preserve Creator OS as the source of truth for lyrics.
- Support accurate SRT and ASS subtitle generation.

