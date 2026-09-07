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


def answer(soru: str, *, k: int = VARSAYILAN_K) -> Cevap:
    """Bir soruya kaynaklı, atıfları doğrulanmış cevap üret.

    Boş getirmede model çağrılmaz; dürüst suskunluk döner.
    """
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
