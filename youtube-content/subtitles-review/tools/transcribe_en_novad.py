"""English subtitle ASR: faster-whisper medium, word timestamps, VAD off -> <out>.words.json"""
import json, sys, time
from pathlib import Path
from faster_whisper import WhisperModel
wav, out = sys.argv[1], Path(sys.argv[2])
PROMPT = ("Dr Senai Aksoy explains IVF and the first ultrasound: weeks of pregnancy, cardiac activity, gestational sac, "
          "yolk sac, transvaginal scan, ectopic pregnancy, heterotopic pregnancy, beta hCG, blastocyst, progesterone, "
          "NICE NG126, Mortimer, AJOG, Spandorfer, Doubilet, Bree.")
t0 = time.time()
model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
segs, info = model.transcribe(wav, language="en", beam_size=5, word_timestamps=True, initial_prompt=PROMPT,
                              condition_on_previous_text=False, vad_filter=False)
words = []
for s in segs:
    for w in s.words or []:
        words.append([w.word, round(w.start, 3), round(w.end, 3), round(w.probability, 3)])
    print(f"{s.end:7.1f}s {len(words)} words ({time.time()-t0:.0f}s)", flush=True)
out.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
print("DONE", len(words), f"{time.time()-t0:.0f}s", flush=True)
