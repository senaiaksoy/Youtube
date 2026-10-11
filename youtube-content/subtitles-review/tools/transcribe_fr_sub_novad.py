"""French subtitle ASR: faster-whisper medium (local cache), word timestamps, glossary-primed. -> <out>.words.json"""
import json, sys, time
from pathlib import Path
from faster_whisper import WhisperModel

wav, out = sys.argv[1], Path(sys.argv[2])
PROMPT = ("Le Dr Senai Aksoy parle de FIV et de la première échographie : SA, semaines d'aménorrhée, activité cardiaque, "
          "sac gestationnel, vésicule vitelline, échographie endovaginale, grossesse extra-utérine, grossesse hétérotopique, "
          "bêta-hCG, blastocyste, progestérone, NICE NG126, Mortimer, AJOG, Spandorfer, Doubilet, Bree.")
t0 = time.time()
model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
segs, info = model.transcribe(wav, language="fr", beam_size=5, word_timestamps=True, initial_prompt=PROMPT,
                              condition_on_previous_text=False, vad_filter=False)
words = []
for s in segs:
    for w in s.words or []:
        words.append([w.word, round(w.start, 3), round(w.end, 3), round(w.probability, 3)])
    print(f"{s.end:7.1f}s {len(words)} words  ({time.time() - t0:.0f}s elapsed)", flush=True)
out.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
print("DONE", len(words), "words", f"{time.time() - t0:.0f}s", flush=True)
