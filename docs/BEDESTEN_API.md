# Bedesten API — Reverse-Engineered Referans

> `saidsurucu/mevzuat-mcp` (MIT) reposundan çıkarıldı + canlı test edildi (2026-05-29, çalışıyor).
> **Amaç:** MCP'yi kurmadan, mevzuat (ve ileride içtihat) verisini doğrudan bu temiz JSON API'den çekmek.
> Çalışan minimal istemci: `scripts/bedesten_probe.py`.

## Genel
- **BASE:** `https://bedesten.adalet.gov.tr/mevzuat`
- **Auth/Playwright/cookie:** YOK (saf httpx/urllib yeter).
- **Erişim notu:** Adalet Bakanlığı backend'i; TR IP gerekebilir (mevzuat.gov.tr gibi — VPN kapalıyken test edildi, çalıştı).
- **Headers (zorunlu):**
  ```
  Content-Type: application/json
  Origin:  https://mevzuat.adalet.gov.tr
  Referer: https://mevzuat.adalet.gov.tr/
  User-Agent: Mozilla/5.0 ... (tarayıcı UA)
  ```
- **Sarmalama:** her POST gövdesi → `{"data": <inner>, "applicationName": "UyapMevzuat"}`. Aramada ek: `"paging": true`.
- **Başarı kontrolü:** `body.metadata.FMTY == "SUCCESS"` (hata: `FMTE` mesajı).

## Uçlar (hepsi POST)

### 1. `/searchDocuments` — mevzuat ara/listele
inner alanları:
```jsonc
{
  "pageSize": 5, "pageNumber": 1,
  "sortFields": ["RESMI_GAZETE_TARIHI"], "sortDirection": "desc",
  "mevzuatNo": "4857",                 // opsiyonel: kanun no
  "mevzuatAdi": "İş Kanunu",           // opsiyonel: ada göre
  "phrase": "...",                      // opsiyonel: tam-metin (Solr)
  "mevzuatTurList": ["KANUN","KHK"],   // opsiyonel: tür filtresi
  "basliktaAra": true, "tamCumle": false
}
```
→ `paging:true` ile sar. Yanıt: `body.data.mevzuatList[]`, `body.data.total`.
Her doküman: **`mevzuatId`** (asıl id, örn "103054"), `mevzuatNo`, `mevzuatAdi`, `mevzuatTur{id,name}`, `mevzuatTertip`, `resmiGazeteSayisi`, `url`, `gerekceId`.

### 2. `/getDocumentContent` — tam metin
```jsonc
{"documentType": "MEVZUAT", "id": "<mevzuatId>"}   // tüm kanun
{"documentType": "MADDE",   "id": "<maddeId>"}     // tek madde
```
→ `body.data.content` **base64** (genelde `text/html`), `body.data.mimeType`. Decode + HTML tag temizle.

### 3. `/mevzuatMaddeTree` — madde ağacı (TOC)
```jsonc
{"mevzuatId": "<mevzuatId>"}
```
→ kanun→bölüm→madde hiyerarşisi (her madde için id'ler; #2 ile tek tek metin çekilebilir).

### 4. Diğer
- `/getGerekceContent` → `{"id": "<gerekceId>"}` — kanun gerekçesi.
- `/mevzuatTypes` → `{}` — tür listesi (KANUN, KHK, YÖNETMELİK…).

## Mevzuat türleri (`mevzuatTurList`)
KANUN, CB_KARARNAME (Cumhurbaşkanlığı Kararnamesi), KHK, TUZUK, YONETMELIK, CB_KARAR, CB_GENELGE, TEBLIG, KKY, vb. (kesin liste için `/mevzuatTypes`).

## Bizim için kullanım planı
1. `mevzuatTurList:["KANUN"]` + sayfalama ile **tüm kanunları listele** → `mevzuatId` topla.
2. Her biri için `/getDocumentContent` (MEVZUAT) → tam metin; veya `/mevzuatMaddeTree` + madde-bazlı çekim.
3. Çıkar → temizle → `data/raw/` (grounding korpusu). Canlı = hep güncel.
4. (Faz 2) İçtihat: aynı backend `bedesten.adalet.gov.tr` (yargi-mcp contract'ı ayrıca çıkarılacak).
