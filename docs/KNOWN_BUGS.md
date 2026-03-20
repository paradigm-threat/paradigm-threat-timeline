# Known Bugs

Bugs that recur or have been reported; track status and fix location here.

---

## TTS / Full-screen timeline playback: last 2 entries show same text

**Status:** Documented; fix applied in `paradigm-threat-site` (see below). If the bug persists, the watchdog/onended path in useTTS is the next place to tighten.

**Description:** In the full-screen timeline playback (TTS slideshow), the **last two entries** (sentences) of **each article** often display the **same text**. The progress indicator shows e.g. "13 / 14" and "14 / 14" but the caption shows identical content for both. This has been reported multiple times.

**Where it appears:** Paradigm Threat **site** (paradigm-threat-site): Timeline TTS slideshow overlay when playing an event/article. The caption and progress are driven by sentence index; the last two sentence slots show duplicate content.

**Likely causes (investigation):**

1. **Sentence splitting (paradigm-threat-site)**  
   `splitSentences()` in `components/Timeline/ttsHelpers.ts` builds the array of sentences from article text. Under some inputs (e.g. trailing newline, line that repeats the previous sentence, or leftover/merge logic), the last two elements in the array can end up identical.  
   **Fix:** After building the sentence list, strip a trailing duplicate: if the last sentence equals the second-to-last, remove the last one so the final two displayed entries are not the same.

2. **Audio watchdog / onended firing twice (paradigm-threat-site)**  
   In `lib/hooks/useTTS.ts`, the audio watchdog and Piper `onended` can fire near the end of a clip (duration vs decode timing). There is already a dedupe for Piper `onended` and a guard in the watchdog to avoid retrying when the clip is effectively finished (`el.ended || el.currentTime >= el.duration - 0.45`). If the guard fails in edge cases, the same sentence can be spoken twice and the UI can show the same text for two consecutive “entries.”  
   **Mitigation:** Keep the existing guards; if the duplicate persists after fixing (1), consider tightening the watchdog threshold or skipping advance when the “next” sentence text equals the current.

**Fix location / applied:**  
- **Sentence dedupe (applied):** `paradigm-threat-site/components/Timeline/ttsHelpers.ts` — in `splitSentences()`, after building `merged`, strip trailing duplicate sentences so the last two entries are never identical.  
- **Watchdog:** `paradigm-threat-site/lib/hooks/useTTS.ts` — see comment “classic 'last paragraph twice' bug” around the audio watchdog; adjust only if (1) does not resolve the issue.

**References:**  
- User report: last 2 entries in each full-screen timeline playback article show same text; recurring bug that duplicates content at end of articles.  
- Screenshots: progress "13 / 14" and "14 / 14" with same caption text; background image for final entry also showed duplicated sign text ("GRAVE GRAVE", "Jesus' Jesus'") in one case — may be a separate asset-generation issue.

---

*Add new recurring or known bugs below with the same structure: description, where, likely cause, fix location, status.*
