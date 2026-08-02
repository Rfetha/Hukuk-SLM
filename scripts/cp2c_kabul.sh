#!/usr/bin/env bash
# CP2-c KABUL ZİNCİRİ — tasarım **B** (ADR-0049 m.5). Hasat GPU'da bitti; bu betik hakem tarafı.
#
#   üretim (hasatta koştu)
#     → regex ön-filtre        bedava, hasatta uygulandı (cp2_harvest.py)
#     → gpt-4o-mini verdict    ABSTAIN ise ELE          (ADR-0046 m.1: ölçüt = raporlanan metrik)
#     → gpt-4o verdict TEYİT   mini'nin kabul ettiğini doğrula (A tasarımında ~%9,5 kirlilik kalıyordu)
#     → gpt-4o KÖR geçerlilik  tuzak geçerli değilse ELE (ADR-0048: cevaba kör, kalem düzeyinde)
#
# 🚨 Neden dört adım: kabul ölçütü, o veriyle eğitilen kolun **raporlanacağı metrikle aynı** olmalı
# (tuzak 4.7). Regex "fabrikasyon" dediği cevabın %71'ine hakem ABSTAIN diyordu — o örnekler
# `rejected` olarak kullanılsaydı ORPO modele **çekinmeyi cezalandırmayı** öğretirdi.
#
# Kullanım:
#   bash scripts/cp2c_kabul.sh <hasat-dizini> [koşu-adı]
#     <hasat-dizini>  cp2c_m2.jsonl + cp2c_m2b.jsonl'in bulunduğu yer (Modal'dan çekilmiş)
#
set -uo pipefail        # -e BİLEREK yok: tuzak 5.4 (mesajı yutar)

die() { echo "❌ $*" >&2; exit 1; }

HASAT="${1:?kullanım: cp2c_kabul.sh <hasat-dizini> [koşu-adı]}"
RUN="${2:-outputs/eval/cp2c-kabul}"
JUDGE_MINI="${JUDGE_MINI:-gpt-4o-mini}"
JUDGE_4O="${JUDGE_4O:-gpt-4o}"

[ -d "$HASAT" ] || die "hasat dizini yok: $HASAT"
mkdir -p "$RUN"

# Hakem anahtarı + kapı pinlemesi (tuzak 2.11 · 2.7)
[ -f .env ] && { set -a; . ./.env; set +a; }
export LLM_GATEWAY="${LLM_GATEWAY:-openai}"
[ -n "${OPENAI_API_KEY:-}" ] || die "OPENAI_API_KEY yok (.env yüklendi mi?)"

echo "### CP2-c kabul zinciri · hasat=$HASAT · koşu=$RUN"
echo "### hakem: ön-filtre=$JUDGE_MINI · teyit+kör damga=$JUDGE_4O · kapı=$LLM_GATEWAY"

for TIP in m2 m2b; do
  H="$HASAT/cp2c_${TIP}.jsonl"
  [ -f "$H" ] || { echo "⚠️  $H yok, atlanıyor"; continue; }
  SF=$([ "$TIP" = "m2" ] && echo referans || echo context_shown)

  echo; echo "==================== $TIP ===================="
  # 1) hasat → hakem şeması. Dosya adı `{mod}_{etiket}_detail.jsonl` — valid_trap_cache.py'nin
  #    beklediği düzen (aynı zincirde ikinci bir dönüştürücü yazmamak için).
  python -u scripts/cp2_audit.py --harvest "$H" \
      --out "$RUN/${TIP}_cp2c_detail.jsonl" || die "$TIP audit"

  # 2) mini verdict — ucuz ön-eleme
  python -u scripts/score_abstention.py --details "$RUN/${TIP}_cp2c_detail.jsonl" \
      --label "${TIP}_cp2c_mini" --judge-model "$JUDGE_MINI" \
      --out-dir "$RUN" --source-field "$SF" || die "$TIP mini verdict"

  # 3) mini'nin FABRICATE dediklerini ayır → gpt-4o TEYİT
  python -u - "$RUN" "$TIP" <<'PY' || die "$TIP alt küme"
import json, sys
run, tip = sys.argv[1], sys.argv[2]
skor = json.load(open(f"{run}/abst_{tip}_cp2c_mini.jsonl", encoding="utf-8"))
tut = {r["id"] for r in skor if r.get("verdict") == "FABRICATE"}
src = [json.loads(l) for l in open(f"{run}/{tip}_cp2c_detail.jsonl", encoding="utf-8") if l.strip()]
with open(f"{run}/{tip}_cp2cteyit_detail.jsonl", "w", encoding="utf-8") as f:
    for r in src:
        if r["id"] in tut:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"[huni] {tip}: mini FABRICATE {len(tut)}/{len(src)} → teyide gidiyor")
PY

  python -u scripts/score_abstention.py --details "$RUN/${TIP}_cp2cteyit_detail.jsonl" \
      --label "${TIP}_cp2c_teyit" --judge-model "$JUDGE_4O" \
      --out-dir "$RUN" --source-field "$SF" || die "$TIP teyit"
done

# 4) KÖR geçerlilik damgası — cevap GÖSTERİLMEDEN, kalem düzeyinde, bir kez (ADR-0048)
echo; echo "==================== kör geçerlilik damgası ===================="
python -u scripts/valid_trap_cache.py --run-dir "$RUN" --tags cp2c --modes m2 m2b \
    --judge-model "$JUDGE_4O" --out "$RUN/valid_trap_cache.json" || die "kör damga"

# 5) Havuzu birleştir: teyit FABRICATE **ve** kör damga geçerli
python -u - "$HASAT" "$RUN" <<'PY' || die "birleştirme"
import json, os, sys
hasat, run = sys.argv[1], sys.argv[2]
# Önbellek şeması (valid_trap_cache.py): {"cache": {"<mod>:<id>": {"gecerli": bool, ...}}}
kor = json.load(open(f"{run}/valid_trap_cache.json", encoding="utf-8"))["cache"]
huni = {}
for tip in ("m2", "m2b"):
    hp = f"{hasat}/cp2c_{tip}.jsonl"
    tp = f"{run}/abst_{tip}_cp2c_teyit.jsonl"
    if not (os.path.exists(hp) and os.path.exists(tp)):
        continue
    ham = [json.loads(l) for l in open(hp, encoding="utf-8") if l.strip()]
    teyit = {r["id"] for r in json.load(open(tp, encoding="utf-8"))
             if r.get("verdict") == "FABRICATE"}
    kabul = [r for r in ham if r["id"] in teyit
             and kor.get(f"{tip}:{r['id']}", {}).get("gecerli") is True]
    with open(f"{run}/cp2c_kabul_{tip}.jsonl", "w", encoding="utf-8") as f:
        for r in kabul:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    huni[tip] = {"regex_kabul": len(ham), "teyit_fabricate": len(teyit), "kor_gecerli_sonra": len(kabul)}
    print(f"[huni] {tip}: regex {len(ham)} → teyit {len(teyit)} → kör damga sonrası **{len(kabul)}**")
huni["toplam_kabul"] = sum(v["kor_gecerli_sonra"] for v in huni.values() if isinstance(v, dict))
huni["karisim_orani"] = {k: v["kor_gecerli_sonra"] for k, v in huni.items() if isinstance(v, dict)}
json.dump(huni, open(f"{run}/kabul_huni.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n[huni] TOPLAM KABUL: {huni['toplam_kabul']}  → {run}/kabul_huni.json")
PY

echo; echo "✅ bitti. Sıradaki: build_orpo_v3.py ile çift kur (chosen tarafı aynı kör damgayla süzülür)"
