### 2026-06-09 — v1 SFT eğitimi (Modal A100)
- 1 epoch, 1207 step, ~3.5h ≈ ~$10. **Başlatma dersi (ADR-0008):** `modal run --detach ...::spawn_train` (fire-and-forget); `train.remote` client'a bağlı bekler → WSL kapanınca cancel → job ölür (4 kez yandı). Çözüm: `spawn()`.
- Adapter → `outputs/v1/` (checkpoint-1207).

