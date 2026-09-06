# ⏸️ M5 ölçümü DURDURULDU — pilde, 2026-09-07

**Neden durduruldu:** makine **pilde** ve GPU **P5 · SM clock 180 MHz**'e kısılıyor
(şarjda ~2.000 MHz). Üretim **8,4 t/s** (şarjda ~42 t/s) ⇒ 80 kalem **~4,8 saat** sürecekti.
Şarjda **~57 dakika**.

**Koşu SAĞLAM, takılma YOK** — 3 kalemlik duman testiyle ayırt edildi: sunucu üretiyor,
üretimler ~900 token'da doğal sonlanıyor, hat çalışıyor. Tek sorun hız.

⭐ **Yan ölçüm (yeni bilgi):** M5'te **kalem başına İKİ üretim** gerekiyor — model kör modda
`</think>`'i bütçe içinde kapatmıyor, zorla-kapatma yolu devreye giriyor
([#42](../../../docs/record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md)'nin kalıntısı).
⇒ M5 kalem başına ~1800 token, diğer modların **iki katı**.

**Bu klasördeki `*_detail.jsonl` BOŞ (0 bayt)** — hiçbir kalem tamamlanmadı, sayı üretilmedi.

## Yarın şarjda koşulacak komut

```bash
cd /home/ersoy/code/Hukuk-SLM
setsid nohup bash -c 'source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a && \
  export PYTHONUNBUFFERED=1 && \
  OUT_DIR=outputs/eval/f07-m5-anti-hedef MODES="m5" THINK_BUDGET=1024 MAXTOK=512 CTX=8192 \
  bash scripts/cp0_thinking_gen.sh models/gguf/tgta_v1-q4_k_m.gguf tgta_v1_m5_v2; \
  echo "EXIT=$?"' > /tmp/m5_run.log 2>&1 < /dev/null &
```
⛔ Başlatmadan önce künyede **`güç : ŞARJDA`** yazdığını doğrula.
Sonra puanlama + ADR-0064 madde (3) kapanışı.
