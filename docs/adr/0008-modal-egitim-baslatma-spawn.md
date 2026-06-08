# ADR 0008 — Modal eğitim başlatma: fire-and-forget `spawn` (WSL-kapanması cancel dersi)

- **Durum:** Yürürlükte (2026-06-09)

## Bağlam
v1 SFT'yi Modal A100'de bağımsız (PC kapalıyken de süren) bir koşu olarak başlatmak istedik.
`modal run modal_train.py` ve `modal run --detach modal_train.py` denendi — **ikisinde de koşu
WSL/PC kapanınca erken öldü** (4 kez: step 31, 13, ... checkpoint'e ulaşmadan, ~$4-5 boşa).

Kök neden (deneysel olarak bulundu): `train.remote()` entrypoint'i eğitim bitene kadar **bekler**
→ local'de eğitime bağlı bir client process kalır. WSL/PC/IDE kapanışı bu client'a **SIGTERM**
gönderir; modal client SIGTERM'i "graceful shutdown" sayıp Modal'a **cancel** yollar → job iptal.
`--detach` tek başına yetmedi (bekleyen client hâlâ var). Hatta client'ı `kill` (SIGTERM) ile
öldürmek de cancel tetikledi; `kill -9` denemesi de güvenilir olmadı.

## Karar
Tam koşu **fire-and-forget** başlatılır: `train.spawn()` job'ı kuyruğa atıp **hemen döner**
(bekleyen client YOK). `modal_train.py::spawn_train` entrypoint'i bunu yapar.

```
modal run --detach modal_train.py::spawn_train --epochs 1
```
- **spawn** → bekleyen client process yok → kapanışta SIGTERM gönderilecek bir şey yok → cancel olamaz.
- **--detach** → entrypoint bitince ephemeral app'i öldürmez; spawned job yaşar (saf `spawn` tek
  başına ephemeral app entrypoint'le birlikte kapanıyordu — onaylandı).

## Değerlendirilen alternatifler
- **`modal run modal_train.py` / `--detach` (train.remote)** → REDDEDİLDİ; client bekler, kapanış = cancel.
- **Client'ı `kill`/`kill -9` ile öldürüp detach'e güvenmek** → güvenilmez; SIGTERM cancel tetikliyor.
- **PC'yi gece açık bırakmak** → yedek plan (kod gerektirmez) ama kullanıcı kapatabilmek istedi.
- **`modal deploy` (kalıcı app)** → gereksiz ağır; tek-seferlik eğitim için spawn+detach yeterli.

## Sonuç (kanıt 2026-06-09)
- spawn+detach ile başlatıldı → client'sız job step monoton arttı, **cancellation gelmedi**.
- **IDE (Zed/WSL) kapat-aç testi GEÇTİ:** step 29 → 41 → 62 kesintisiz; loss ~0.95 plato; app `running`.
- Ek dayanıklılık (ADR ilişkili, `train_sft.py`/`modal_train.py`): `save_steps=200` + `save_total_limit=3`
  ara checkpoint, `get_last_checkpoint` ile **oto-resume**, 15dk'da bir `out_vol.commit()` (checkpoint
  buluta kalıcı). Yani spawn tutmazsa bile checkpoint ≥200'den resume edilebilir.
- **Reproducibility (paper):** uzun GPU koşuları daima `spawn_train` ile başlatılacak; bu, sonuçların
  istemci kararlılığından bağımsız tekrar-üretilebilirliğini sağlar.

## İlgili
`modal_train.py` (`spawn_train`), `scripts/train_sft.py` (resume/save_steps), ADR 0004 (Modal), `[[cloud-gpu-modal]]`
