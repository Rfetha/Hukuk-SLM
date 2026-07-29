# ADR-0034 — Emekli hattın artefaktları repo'dan çıkarıldı (`old-version-gemma4-12b/` silindi)

> ### 🔴 TEK-NÜSHA RİSKİ GERÇEKLEŞTİ (2026-07-29) — 12B adaptörleri **kalıcı kayıp**
> Bu ADR'nin *"yedeklenmemiş tek nüsha"* diye işaretlediği `~/code/hukuk-devir/` paketi
> **kullanıcı tarafından silindi.** **Kasıtlı:** 12B hattı emekli, sayıları yeni hatta taşınmıyor,
> o ağırlıklara bir daha ihtiyaç duyulmayacak.
>
> | ne | durum |
> | :--- | :--- |
> | `outputs/adapters_12b/` — **v0/v1/v2b/v2c/v3, 1.8 GB** | 🔴 **kalıcı kayıp** (git'te hiç olmadılar) |
> | `DEVIR.md` · `RECETELER_12B.md` (devir için yazılmış notlar) | 🔴 muhtemelen kayıp — git geçmişinde bu adlarda kayıt yok |
> | `git/hukuk-slm-full.bundle` | 🟢 önemsiz — repo'nun kendisi o geçmiş |
> | `SCORECARD.md` · v3 reçeteleri · `gemma4_nothink.jinja` · eval çıktıları | 🟢 **git'te:** `git show a19fc25^:old-version-gemma4-12b/record/SCORECARD.md` |
> | 12B'nin **sayıları ve dersleri** | 🟢 repo içi: `gemma4-12b-kronoloji.md` · `gemma4-12b-dersler.md` |
>
> **Kurtarma yolu artık BİR tane:** git geçmişi. Bu ADR'nin *"iki yoldan doğrulandı"* cümlesi
> ve `~/code/hukuk-devir/…` adresini öneren **kural fıkrası geçersizdir** — o adresi bir daha yazma.
> **Bedel:** 12B modelleri bir daha koşulamaz/ölçülemez. ADR-0028 dış geçerlilik açığını zaten
> kabul etmişti; bu, girmemeye karar verilmiş bir kapıyı kilitliyor, argümanda yeni delik açmıyor.
>
> **Yeni kural (kullanıcı, 2026-07-29):** **repo dışı artefakt YOK** — her şey
> `/home/ersoy/code/Hukuk-SLM` altında. Kollar versiyonlu ve kayıtlı:
> [`docs/record/kollar.md`](../record/kollar.md). Yeni hattın adaptörleri de git'te **değil** ve
> **yedeklenmiyor** — bilinçli karar: adaptör veri + reçete + seed sabitken yeniden üretilebilir.

**Statü:** Yürürlükte (kurtarma yolu ikiden **bire** indi — bkz. üst not) · **Tarih:** 2026-07-28
**Otorite belge:** `TASARIM.md` §2 (belge haritası)
**İlgili:** **ADR-0024 (emeklilik) — bu ADR onun *"taşındı, silinmedi"* yarısını süperseder**,
diğer yarısı (*dersler taşınır, sayılar taşınmaz*) aynen yürürlükte ·
ADR-0026 (base parametre) · `gemma4-12b-dersler.md#adr-0024`
**Kanıt:** `git ls-tree -r a0575e6 old-version-gemma4-12b/` → **205 dosya / 8.1 MB, tamamı kayıtlı** ·
`git bundle verify ~/code/hukuk-devir/git/hukuk-slm-full.bundle` → *"records a complete history"* ·
`~/code/hukuk-devir/outputs/adapters_12b/` → 1.8 GB, v0/v1/v2b/v2c/v3
**Uygulayan commit:** `a19fc25` (silme) + bu commit (referans onarımı)

---

## Bağlam

ADR-0024 Gemma 4 12B hattını emekli ederken artefaktları silmek yerine `old-version-gemma4-12b/`
altına taşımıştı; gerekçe *"makale Results'ının ham kaynağı kaybolmasın"* idi. O karardan bu yana
iki şey değişti:

1. **2026-07-24'te repo dışı bir devir paketi kuruldu:** `~/code/hukuk-devir/` — `DEVIR.md`,
   `RECETELER_12B.md`, tam git bundle'ı, 12B adaptörleri, eval çıktıları ve `SCORECARD.md`.
2. **Aynı gün ham kayıt repo'ya damıtıldı:** `docs/record/gemma4-12b-kronoloji.md` (sayılar birebir)
   ve `docs/adr/gemma4-12b-dersler.md` (26 ADR + dersler). Makalenin Results/Methodology'sinin
   yazılacağı belgeler bunlar — `old-version-gemma4-12b/` değil.

Yani ağaç, iki ayrı yerde daha iyi biçimde tutulan bir şeyin üçüncü kopyasına dönüştü.

## Karar

`old-version-gemma4-12b/` ağacı **çalışma repo'sundan silindi** (kullanıcı kararı, 2026-07-28).
Kurtarma yolu **iki tane**, ikisi de doğrulandı:

| ne | nerede | doğrulama |
| :--- | :--- | :--- |
| 205 metin artefaktı (eval `jsonl`, SCORECARD, tur belgeleri, scriptler) | git geçmişi — `git show a0575e6:old-version-gemma4-12b/<yol>` | `ls-tree` → 205/205 kayıtlı |
| **LoRA adaptörleri** (v0/v1/v2b/v2c/v3) — **git'te hiç olmadılar** (`.gitignore`: `*.safetensors`, `old-version-gemma4-12b/outputs/v*/`) | `~/code/hukuk-devir/outputs/adapters_12b/` (1.8 GB) | dizin yerinde |
| tam git geçmişi (repo'dan bağımsız) | `~/code/hukuk-devir/git/hukuk-slm-full.bundle` (12 MB) | `git bundle verify` → complete history |

Repo içindeki 9 ölü referans aynı commit'te onarıldı: `CLAUDE.md` · `TASARIM.md` ·
`docs/VISION.md` · `docs/adr/README.md` · `docs/record/README.md` · `data/README.md` (×2) ·
`configs/README.md` · `docs/adr/gemma4-12b-dersler.md` (×2).

## Değerlendirilen alternatifler

- **Ağacı olduğu gibi bırakmak** *(ADR-0024'ün orijinal kararı)* — REDDEDİLDİ: kronoloji + dersler
  belgeleri damıtıldıktan sonra ağaç okuma yüzeyine yük bindiren üçüncü kopya oldu. ADR-0024'ün
  gerekçesi (*"kaynak kaybolmasın"*) artık git geçmişi + devir paketiyle zaten karşılanıyor.
- **Sembolik bağ bırakmak** (`old-version-gemma4-12b -> ~/code/hukuk-devir`) — REDDEDİLDİ: ev
  dizinine mutlak bağ versiyonlanamaz, başka makinede kırılır, git'te dosya olarak görünür.
  Bir belge satırı aynı işi taşınabilir biçimde yapıyor.
- **Git geçmişini de temizlemek** (`filter-repo`) — REDDEDİLDİ ve bir daha önerilmemeli: 8.1 MB
  için tüm commit sha'larını yeniden yazmak, ~560 `ADR-00NN` göndermesinin dayandığı geçmişi ve
  bu ADR'nin kurtarma yolunu birlikte yok ederdi.

## Sonuç — kabul edilen bedel

**Bir artefakt kalıcı olarak kayboldu:** `sft_v0_KIRLI_forum` (v0'ı batıran, tek cevabın 154 soruya
yapıştırıldığı forum seti). Git'e hiç girmemişti *ve* devir paketine de alınmamıştı; ağaçla birlikte
gitti. **Ders yaşıyor, kanıt-veri yaşamıyor** — `gemma4-12b-kronoloji.md` #02 ve
`gemma4-12b-dersler.md` A1.1 olguyu sayılarıyla (`legal_acc 0.362 → 0.124`) kayda geçirmiş durumda,
ama setin kendisi bir daha örneklenemez. Bu ADR'nin tek gerçek maliyeti budur; makalede bir iddiaya
dayanak gerekirse dayanak kayıt belgesidir, veri değil.

**Yeni tek-nüsha riski:** adaptörler artık yalnız `~/code/hukuk-devir/` altında ve orası **git
dışı, yedeksiz.** Silinirse 12B hattının ağırlıkları geri gelmez (yeniden eğitmek ~$25 × 5 tur).
Yedekleme kullanıcı sorumluluğunda — bu ADR onu bir eylem maddesi olarak işaretler, çözmez.

**Kural — bundan sonra:** emekli hattın bir dosyasına atıf verirken **repo içi damıtılmış belgeyi**
göster (`gemma4-12b-kronoloji.md` / `gemma4-12b-dersler.md`). Ham dosya gerçekten şartsa adres
`~/code/hukuk-devir/…` ya da `git show a0575e6:…` biçiminde yazılır — çıplak
`old-version-gemma4-12b/…` yolu artık **kırık referanstır.**
