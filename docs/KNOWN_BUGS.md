# Known Bugs

Bugs that recur or have been reported; track status and fix location here.

---

## TTS / Full-screen timeline playback: last segment repeats (audio and/or caption)

**Status:** **Open / recurring** (2026-03). Sentence dedupe in `ttsHelpers.ts` and Piper `onended` deduping plus a near-end guard in the audio watchdog in `useTTS.ts` are in place, but reports continue: the **last part of an article plays twice** in TTS, sometimes with the scrubber already at the final index (e.g. **58 / 58**).

**Description:** In full-screen **Timeline Audio** (`TTSSlideshowOverlay`), users hear the **closing content again** after narration should stop. An older pattern: the **last two scrubber steps** showed the **same caption** ("13 / 14" and "14 / 14" identical). Duplicate **array slots** (splitting) vs **double playback** of the last sentence (watchdog / `onend` race) are distinct; both should stay in scope.

**Where it appears:** `paradigm-threat-site` — `components/Timeline/TTSSlideshowOverlay.tsx` (caption + seek bar), `lib/hooks/useTTS.ts` (Piper `HTMLAudioElement` + Web Speech `SpeechSynthesisUtterance`).

**UI note:** The seek bar label says **Paragraph** but values are **sentence** indices (`ttsState.sentences`). The label is misleading for debugging only.

**Likely causes (investigation):**

1. **Sentence splitting (duplicate captions)** — `splitSentences()` in `components/Timeline/ttsHelpers.ts`; trailing identical sentences are stripped in a `while` loop. Remaining edge cases (speaker blocks, normalization) could still duplicate the last two slots.

2. **Piper: audio watchdog vs `onended` (duplicate audio)** — `startAudioWatchdog()` in `lib/tts/ttsResilience.ts` invokes `onStall` → `handlePiperSegmentFail` → **retry same sentence**. Near clip end, `useTTS` ignores stall when `el.ended || el.currentTime >= el.duration - 0.45` (see comment: *classic "last paragraph twice" bug*). Bad **`duration`** or timing can still **replay the last sentence**; `piperEndedDedupeRef` (900 ms, key `gen:segIndex:sentenceIndex`) mitigates double `onended`.

3. **Web Speech: utterance watchdog vs `onend`** — `startUtteranceWatchdog()` uses a large timeout (comment: underestimating *replays the sentence, often the long last one*). Late `onend` can overlap with watchdog **cancel + retry** on long final sentences.

4. **Double `onended`** — Rare; Piper path partially dedupes.

**Fix locations already in repo:** `ttsHelpers.ts` (`splitSentences` dedupe); `useTTS.ts` (Piper `onended` dedupe, audio watchdog guard, Web Speech paths).

**Next steps when fixing:** Reproduce under **Piper** vs **Speech API**; log watchdog vs end events with `sentenceIndex` and `sentences.length`; consider **no stall-retry** on the last sentence when near natural end; rename seek label **Paragraph** → **Sentence**.

**References:**

- Earlier report: duplicate caption on last two steps; possible slideshow/image duplication ("GRAVE GRAVE") — may be separate from TTS.
- 2026-03: **58 / 58** with **audio** repeating the end — favors (2) or (3) over (1).

---

*Add new recurring or known bugs below with the same structure: description, where, likely cause, fix location, status.*
