"""Ürünün tek derin modülü: answer(soru) → Cevap.

Arayüz tek fonksiyon; retriever, llama-server, istem ve terazi ARKASINDA gizli.
⛔ Harness GPU'ya GİRMEZ (embedder CPU, indeks CPU RAM/disk) — "sığar/sığmaz" farkı budur.

⚠️ Retriever boş dönerse model ÇAĞRILMAZ. Sebebi ölçülmüştür: kaynaksız (M5) koşullarda
model kendinden emin ve YANLIŞ hukuk üretiyor (2026-09-07: İş K. 31 → "35. ve 36. madde",
İİK 79/a → "110. madde", TBK 230 → "6502 Sayılı Tüketici Kanunu"). Üründe bu koşul
OLUŞMAMALIDIR.
"""
import json
import os
import sys
import urllib.request

from hakhukuk.istem import SISTEM_COK_KAYNAK
from hakhukuk.terazi import siniflandir
from hakhukuk.tipler import Cevap, Durum, Kaynak, Yururluk

VARSAYILAN_K = 10          # ADR-0068 · RRF_K=10 ile ölçülen recall@10 = 0,9500
DUSUNCE_BUTCESI = 1024     # ADR-0043 · ADR-0070: toplam bütçe 1536'nın düşünce payı
CEVAP_BUTCESI = 512
KAYNAK_KIRPMA = 900        # ⚠️ ölçüm rejiminin `--max-chunk-chars 900` değişmezi
SUNUCU_URL = os.environ.get("HAKHUKUK_SUNUCU", "http://127.0.0.1:8080/v1")
TOHUM = 3407

_INDEKS = os.environ.get("HAKHUKUK_INDEKS", "data/index/mevzuat_bge_m3_s2")
_retriever = None

# ⛔ Araç döngüsünün SINIRI. Sınır yoksa model sonsuza kadar arayabilir; sınır görünmezse
# vatandaş yarım dayanaklı bir cevabı tam sanır. İkisi de ADR-0076'nın yasakladığı şey.
AZAMI_ADIM = 4
_araclar = None


def _getir(soru: str, k: int) -> tuple[Kaynak, ...]:
    """Hibrit BM25 + bge-m3, RRF ile füzyon. CPU'da çalışır.

    ⚠️ `retriever` bir SINIFTIR, modül fonksiyonu değil; ve korpus alanı `text`, `metin`
    değil. İkisi de koda bakılarak alındı (plan taslağı ikisinde de yanılıyordu).
    Yürürlük süzgeci varsayılan: mülga madde vatandaşa gitmez (Görev 8b).
    """
    global _retriever
    if _retriever is None:
        kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path[:0] = [os.path.join(kok, "scripts"),
                        os.path.join(kok, "scripts", "erisim_korpus")]
        from retriever import Retriever  # noqa: PLC0415 — ağır bağımlılık, gecikmeli
        _retriever = Retriever.yukle(os.path.join(kok, _INDEKS)
                                     if not os.path.isabs(_INDEKS) else _INDEKS)
    ham = _retriever.getir(soru, k=k, yururluk=Yururluk.YALNIZ_YURURLUKTE)
    return tuple(
        Kaynak(kanun_adi=h["kanun_adi"], kanun_no=str(h["kanun_no"]),
               madde_no=h["madde_no"], metin=h["text"], sira=i + 1)
        for i, h in enumerate(ham)
    )


def _uret(mesajlar: list[dict]) -> tuple[str, str]:
    """llama-server'a tek istek. Döner: (metin, finish_reason).

    Deterministik: temperature=0, sabit tohum — aynı soru aynı cevabı verir.
    ⚠️ Bu değişmez SUNUCU YAPILANDIRMASI SABİTKEN geçerlidir. Ölçüldü 2026-09-09: yalnız KV
    önbelleğinin kuantizasyonunu değiştirmek (q8_0 ↔ varsayılan fp16) aynı soruda durum
    sınıfını SUSKUNLUK'tan ÇEKİNCELİ'ye çeviriyor. Yayımlanan sayıların bağlayıcı
    yapılandırması: `-ngl 99 -fa on --no-context-shift --cache-type-k q8_0
    --cache-type-v q8_0 -c 8192` (MODEL_CARD §7.10).
    ⚠️ Bütçe TEK havuzdur (düşünce + cevap). Ölçüm hattı iki geçişli zorunlu kapatma
    kullanıyor; ürün kullanmıyor çünkü kesiklik burada GİZLENMİYOR: bütçe biterse
    `finish_reason="length"` gelir ve terazi cevabı KESİK olarak damgalar.
    """
    govde = json.dumps({
        "model": "local",
        "messages": mesajlar,
        "max_tokens": DUSUNCE_BUTCESI + CEVAP_BUTCESI,
        "temperature": 0.0,
        "seed": TOHUM,
    }).encode("utf-8")
    istek = urllib.request.Request(
        SUNUCU_URL.rstrip("/") + "/chat/completions", data=govde,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(istek, timeout=300) as y:
        d = json.load(y)
    secim = d["choices"][0]
    return secim["message"].get("content") or "", secim.get("finish_reason") or "stop"


ARAC_SEMALARI = (
    {"ad": "ara", "aciklama": "Mevzuatta arama yap, en uygun maddeleri getir.",
     "parametreler": {"sorgu": "str", "k": "int"}},
    {"ad": "madde_getir", "aciklama": "Belirli bir maddenin tam metnini getir.",
     "parametreler": {"kanun_no": "str", "madde_no": "str"}},
    {"ad": "madde_var_mi", "aciklama": "Madde korpusta var mı.",
     "parametreler": {"kanun_no": "str", "madde_no": "str"}},
    {"ad": "kanun_bul", "aciklama": "Kanun adına uyan BÜTÜN kanun numaralarını bul.",
     "parametreler": {"ad": "str"}},
    {"ad": "yururlukte_mi", "aciklama": "Madde yürürlükte mi, mülga mı, yok mu.",
     "parametreler": {"kanun_no": "str", "madde_no": "str"}},
)


def _varsayilan_araclar():
    """Ürün korpusuyla kurulmuş kaldıraçlar. Testler kendi sahtesini geçirir."""
    global _araclar
    if _araclar is None:
        from hakhukuk.araclar import Araclar  # noqa: PLC0415 — korpus ağır
        kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yol = os.path.join(kok, "data/corpus/mevzuat_maddeler.jsonl")
        kayitlar = [json.loads(l) for l in open(yol, encoding="utf-8") if l.strip()]

        def getir(soru, k, yururluk):
            _getir(soru, k)          # retriever'ı kurdurur
            return [dict(h) for h in _retriever.getir(soru, k=k, yururluk=yururluk)]
        _araclar = Araclar(kayitlar, getir=getir)
    return _araclar


def answer_arac(soru: str, *, k: int = VARSAYILAN_K, azami_adim: int = AZAMI_ADIM,
                araclar=None, uret=None) -> Cevap:
    """Çok adımlı cevap: model KALDIRAÇ çağırabilir. `answer()`'ın davranışını DEĞİŞTİRMEZ.

    ⛔ **Ayrı fonksiyon, `answer(..., araclar=True)` değil** (CLAUDE.md §4: public API'de
    bool bayrak yok). Ayrılık ayrıca regresyon kapısını ucuzlatır: araçsız yolun 80 kalemlik
    çıktısı bu dosyada **hiç dokunulmayan** koddan gelir.

    🔒 **KAPI'lar döngünün DIŞINDA, koşulsuz.** Model hiç araç çağırmasa da atıf doğrulama
    ve durum sınıflandırma çalışır — uydurulmuş madde numarasının 0/114 (DEV) ve 0/52
    (donmuş TEST) olması buradan gelir, modelin bir aracı çağırmayı hatırlamasından değil.

    ⛔ Döngü SINIRLI ve sınır GÖRÜNÜR: `azami_adim` dolarsa `Durum.ARAMA_TUKENDI`.
    Bu, `KESIK` ile **birleştirilmez** — *"cümle yarım"* ile *"cümle tam, dayanağı eksik
    olabilir"* vatandaşa farklı şey söyler.
    """
    if not soru.strip():
        return _bos_sorgu_cevabi()
    araclar = araclar if araclar is not None else _varsayilan_araclar()
    uret = uret or _uret_arac
    kaynaklar = _getir(soru, k)
    if not kaynaklar:
        return _suskunluk()

    mesajlar = [{"role": "system", "content": SISTEM_COK_KAYNAK},
                {"role": "user", "content": f"KAYNAKLAR:\n{_blok(kaynaklar)}\n\nSORU: {soru}"}]
    for _ in range(azami_adim):
        metin, finish, cagrilar = uret(mesajlar, ARAC_SEMALARI)
        if not cagrilar:
            break
        for c in cagrilar:
            sonuc = _arac_calistir(araclar, c)
            if isinstance(sonuc, tuple):     # `ara` · yeni kaynaklar listeye girer
                kaynaklar = _kaynaklari_birlestir(kaynaklar, sonuc)
            mesajlar.append({"role": "assistant", "content": f"[ARAÇ {c['ad']}] {sonuc}"})
    else:
        # Sınıra dayandı: döngü `break` görmedi ⇒ model hâlâ arıyordu.
        return Cevap(
            metin="Aramayı sürdürdüm ama elimdeki kaynaklarla dayanağı tamamlayamadım. "
                  "Aşağıdaki maddeler ilgili olabilir; kesin bir hüküm kurmuyorum.",
            durum=Durum.ARAMA_TUKENDI, atiflar=(), kaynaklar=kaynaklar)

    durum, atiflar = siniflandir(metin, kaynaklar, finish)
    return Cevap(metin=metin, durum=durum, atiflar=atiflar, kaynaklar=kaynaklar)


def _arac_calistir(araclar, cagri: dict):
    """⛔ Bilinmeyen araç sessizce yutulmaz — model neyi yanlış çağırdığını GÖRSÜN."""
    ad, arg = cagri["ad"], dict(cagri.get("arg") or {})
    islev = getattr(araclar, ad, None)
    if islev is None:
        return f"BİLİNMEYEN ARAÇ: {ad}"
    return islev(**arg)


def _kaynaklari_birlestir(mevcut, yeni):
    """Kimliği zaten olan madde yeniden eklenmez; sıra numaraları yeniden verilir."""
    goruldu = {s.kimlik for s in mevcut}
    ek = [s for s in yeni if s.kimlik not in goruldu]
    hepsi = list(mevcut) + ek
    return tuple(Kaynak(kanun_adi=s.kanun_adi, kanun_no=s.kanun_no, madde_no=s.madde_no,
                        metin=s.metin, sira=i + 1) for i, s in enumerate(hepsi))


def _blok(kaynaklar) -> str:
    return "\n\n".join(
        f"[KAYNAK {s.sira}] {s.kanun_adi} {s.madde_no}\n{s.metin[:KAYNAK_KIRPMA]}"
        for s in kaynaklar)


def _suskunluk() -> Cevap:
    return Cevap(
        metin="Elimdeki mevzuat kaynaklarında bu soruyu karşılayan bir hüküm bulamadım. "
              "Güncel mevzuata veya bir avukata danışmanızı öneririm.",
        durum=Durum.SUSKUNLUK, atiflar=(), kaynaklar=())


def _bos_sorgu_cevabi() -> Cevap:
    """Boş/yalnız-boşluk sorguya dürüst yanıt — `_getir` bu dala hiç girmez.

    Durum=SUSKUNLUK: kaynaksızlıkla aynı ailede, dürüst "cevaplayacak bir şey yok" hâli
    (uydurulmuş bir uzunluk eşiği yok — yalnız boş/boşluk sorgu bu kapıdan döner).

    ⚠️ ŞERH (kod incelemesi B5, 2026-09-11): rozet ile gövde aynı şeyi SÖYLEMİYOR — rozet
    "kaynaklarda karşılık bulunamadı" (aradım, bulamadım) derken bu dalda hiç arama
    YAPILMADI ve gövde "soru boş" diyor. Ölçüm etkisi bugün SIFIR (DEV'de 0 boş kalem) ama
    suskunluk sayımının içine bir yol açıldı. Altıncı bir `Durum` eklemek tip düzeyinde bir
    tasarım değişikliğidir ve ADR ister; bu yüzden kapatılmadı, planın AÇIK KUSURLAR
    bölümüne kaydedildi.
    """
    return Cevap(
        metin="Soru boş görünüyor. Cevap üretebilmem için mevzuatla ilgili bir soru yazmanız "
              "gerekir.",
        durum=Durum.SUSKUNLUK, atiflar=(), kaynaklar=())


def _uret_arac(mesajlar: list[dict], semalar=None) -> tuple[str, str, tuple]:
    """Araçlı üretim taşıyıcısı. Bugün araç çağrısı **ayrıştırılmıyor** — sunucu tarafı
    tool-calling desteği açılana kadar tek atış davranır ve bu **açıkça** böyle yazılıdır.
    ⚠️ Sessiz bir boş demet döndürmek, *"model araç istemedi"* ile *"taşıyıcı aracı
    taşımıyor"*u aynı şeye çevirirdi; ayrım burada durur.
    """
    metin, finish = _uret(mesajlar)
    return metin, finish, ()


def answer(soru: str, *, k: int = VARSAYILAN_K) -> Cevap:
    """Bir soruya kaynaklı, atıfları doğrulanmış cevap üret.

    Boş getirmede model çağrılmaz; dürüst suskunluk döner.
    """
    if not soru.strip():
        return _bos_sorgu_cevabi()
    kaynaklar = _getir(soru, k)
    if not kaynaklar:
        return Cevap(
            metin="Elimdeki mevzuat kaynaklarında bu soruyu karşılayan bir hüküm bulamadım. "
                  "Güncel mevzuata veya bir avukata danışmanızı öneririm.",
            durum=Durum.SUSKUNLUK, atiflar=(), kaynaklar=())

    blok = "\n\n".join(
        f"[KAYNAK {s.sira}] {s.kanun_adi} {s.madde_no}\n{s.metin[:KAYNAK_KIRPMA]}"
        for s in kaynaklar)
    mesajlar = [{"role": "system", "content": SISTEM_COK_KAYNAK},
                {"role": "user", "content": f"KAYNAKLAR:\n{blok}\n\nSORU: {soru}"}]
    metin, finish = _uret(mesajlar)
    durum, atiflar = siniflandir(metin, kaynaklar, finish)
    return Cevap(metin=metin, durum=durum, atiflar=atiflar, kaynaklar=kaynaklar)
