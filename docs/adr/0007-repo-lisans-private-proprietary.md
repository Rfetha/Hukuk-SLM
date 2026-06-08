# ADR 0007 — Repo & lisans: private + proprietary

- **Durum:** Yürürlükte (2026-05-29)
- **Geriye dönük kayıt.**

## Bağlam
Proje hem ticari değer taşıyor hem akademik yayın kapısını açık tutmak istiyor. Açık-kaynak mı,
kapalı mı? Karar baştan netleşmeli çünkü veri/kod/lisans hijyenini (atıf, telif) etkiler.

## Karar
- **Repo private + proprietary lisans.** Ticari haklar sahibinde.
- Model ağırlıkları + model kartı ileride HF'de yayımlanabilir (opsiyonel, şart değil).
- **Akademik yayın kapısı açık** → rigor/reproducibility baştan korunur (sabit seed, loglu koşu,
  temiz ablasyon). Mantıken bugün de "paper olacakmış gibi" çalışılır.

## Değerlendirilen alternatifler
- **OSS / Apache-2.0 (proje için)** → REDDEDİLDİ. Ticari hakları korumak öncelik. **Dikkat:** base
  model Gemma 4 Apache-2.0 → atıf ZORUNLU; bu, *projenin* lisansını OSS yapmaz.
- **Tam kapalı, paper yok** → REDDEDİLDİ; yayın opsiyonu değerli, maliyeti sadece disiplin.

## Sonuç
- Veri yalnız açık/kamu kaynak + PII maskeleme (ADR 0005) — repo private olsa bile telif zehiri
  (Lexpera/Kazancı) yasak; ağırlık yayımlanabilirliği için de şart.
- Gemma 4 Apache-2.0 atfı model kartında verilecek.

## İlgili
CLAUDE.md > Project framing, ADR 0003, ADR 0005
