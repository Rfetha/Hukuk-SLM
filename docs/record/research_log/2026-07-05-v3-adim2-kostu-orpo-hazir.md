## 2026-07-05 · v3 ADIM 2 KOŞTU + ADIM 6a paketlendi — harvest tamam, ORPO train/val hazır

**Modal engeli kalktı → harvest KOŞTU (ADIM 2 kapandı).** 2026-07-04 girişindeki "Could not connect to the Modal server" engeli geçti. **Kritik mühendislik keşfi:** `modal run modal_train.py::spawn_harvest` (sade `.spawn()`, `--detach`SİZ) → ephemeral app local-entrypoint bitince STOP → spawn'lanan `harvest_rejected` **iptal** (dashboard'da kırmızı bar, "Live Apps 0/Stopped 7"). **Doğru kalıp: `modal run --detach modal_train.py::harvest_rejected --target 1500`** (doğrudan fonksiyon çağrısı + detached). Bu temiz koştu. → v3_recipe HANDOFF'taki "sade `.spawn()` yeterli" notu YANLIŞ'tı, düzeltildi.

**Harvest sonucu (n=1728, ORACLE eval-aynası zor-trap, v2b):**
| Ölçüm | Değer |
|---|---|
| Toplam üretilen | 1728 |
| **Fabrikasyon (abstained=False)** | **1504** |
| Çekimser (abstained=True) | 224 |
| **fab_oranı** | **0.870** |
| Baş-mojibake (pad-fix sonrası) | 4/1504 = **%0.3** (→ 5 satır in-place temizlendi) |

→ **K3 funnel doğrulandı ölçekte:** v2b, "makul-komşu yanlış madde + ORACLE framing"de **%87 uyduruyor** (2026-07-04'teki n=24 smoke tahmini 0.79'du; tam koşuda 0.870 çıktı, aynı yön). Bu, eval M2'deki v2b fab davranışının (M2 abstention 0.346) train-tarafı kanıtı → ORPO rejected havuzu bol ve temsili. **pad-fix tuttu:** mojibake ~%26 (pad=eos) → %0.3 (pad=`<pad>`).

**ADIM 6a paketleme KOŞTU (`build_orpo_v3.py`, lokal $0, `HF_HUB_OFFLINE=1`).** Funnel (`orpo_report.json`):
| | |
|---|---|
| abstain_pairs (is_pref=1, ORACLE) | 1495 |
| grounding_replay (is_pref=0, RAG_MULTI, replay_frac=0.20) | 299 |
| total | 1794 → **train 1741 / validation 53** |
| interleave_step | 6 (deterministik, batch-varyans emniyeti) |
| elenen | abstained_no_contrast 224 · dev_excluded 9 · no_chosen 0 |
| hi_overlap_provisional | 108 (ADIM 4 τ-judge RAFİNE edecek; şimdilik DAHİL) |

**Yapı doğrulandı (decode):** abstain prompt'u `KAYNAK MADDE:` (ORACLE, eval M2 hedefi) içeriyor; grounding prompt'u `KAYNAKLAR:` (RAG_MULTI, M1 sınavı) içeriyor; is_pref satır-bazlı korunuyor (1449 abstain + 292 grounding, train'de). train/validation.jsonl Modal `hukuk-data:/sft_v3/`'e yüklendi (path teyitli).

**Ağ-kısıt durum değişikliği (kalıcı not):** bu oturumda **Claude'un kendi Bash aracının dışa ağ erişimi AÇILDI** (Modal 200, HF 200, git-push erişilebilir) — 2026-07-04'teki "sandbox ağsız → kullanıcı `!` shell gerekir" kısıtı **kalktı**. Modal/HF/git artık doğrudan koşulabiliyor.

**Sıradaki = ADIM 7 Modal smoke (PARA-KAPISI, ~$0.15, kullanıcı onayı bekliyor):** `modal run --detach modal_train.py::train_orpo --run-name v3-smoke --max-steps 50`. Doğrular: (a) v2b-continuation `PeftModel is_trainable`, (b) is_pref collator-list, (c) OOM/NaN/nll_loss.

**Kaynak:** `data/processed/sft_v3/{rejected,train,validation,orpo_report.json}` (seed 3407) · `scripts/{gen_v3_rejected,build_orpo_v3}.py` · `modal_train.py::{harvest_rejected,train_orpo}`.
**Paper eşleme:** fab_oranı 0.870 = K3 "near-miss fabrikasyon" olgusunun train-tarafı nicel kanıtı (ORPO'nun düzelteceği hedef davranış); Modal detach-kalıbı = reprodüksiyon-notu (spawn iptal tuzağı).

---

