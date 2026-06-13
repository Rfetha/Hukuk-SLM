# scripts/_legacy — arşivlenmiş script'ler

Bunlar **artık aktif boru hattının parçası değil** ama **silinmedi** — araştırma projesi olduğumuz
için (paper repro + denetim izi) saklanıyor. Aktif `scripts/` dizinini hafifletmek için buraya alındı
(2026-06-13). Hiçbiri aktif script tarafından import edilmiyor (taşımadan önce doğrulandı).

| Script | Neden arşiv | Yerine ne |
|---|---|---|
| `scan_hf_datasets.py` | v0 dönemi HF aday tarama (tek-seferlik, bitti) | — (veri kararı verildi) |
| `eda_datasets.py` | v0 dönemi dataset EDA (tek-seferlik) | — |
| `build_sft_dataset.py` | **v0** (forum verisi) SFT setini kurdu → v0 battı (paper K3). Repro için saklı | grounded hat: `gen_grounded.py` + `gen_sft_v1.py` |
| `make_eval_sample.py` | eski `eval.py` için 30-soru sabit örneklem | `build_eval_sets.py` (CORE-HARD + TRAP) |
| `score_corpus.py` | ⚠️ referans=cevap koyar → groundedness'e verilince YANILTIR (dokümanlar "tek başına kullanma" diyor) | `score_grounded_corpus.py` (gerçek madde-join köprüsü) |

Geri almak gerekirse: `git mv scripts/_legacy/<x>.py scripts/`.
