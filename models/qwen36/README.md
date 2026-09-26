---
license: apache-2.0
base_model: Qwen/Qwen3.6-35B-A3B
tags:
  - colibri
  - qwen3.6
  - qwen3.6-35b-a3b
  - moe
  - int4
  - gs64
library_name: colibri
---

# Qwen3.6-35B-A3B — colibri int4 **gs64** container (group-scaled, higher accuracy)

[colibri](https://github.com/JustVugg/colibri) container for
**Qwen3.6-35B-A3B**, quantized to **group-scaled int4** (one f32 scale per 64
input elements per row, `expert_gs=64`, ~22 GB). This is the higher-accuracy
sibling of the per-row container
[`Kreuzzelg/qwen36-35b-a3b-colibri-i4`](https://huggingface.co/Kreuzzelg/qwen36-35b-a3b-colibri-i4):
in a controlled A/B against an int8 anchor it cuts the first-token logit error
by **~44 %** (mean cosine 0.98777 → 0.99313 over 4 prompts). Same self-contained
layout (bundled `tokenizer.json`, flat `config.json`).

**Which one should I use?** The per-row container is the current PR default and
runs on the plain `qwen36-engine` branch. This gs64 container needs the
group-scaled expert path (`matmul_q_gs`), which lives on the
[`gs64-ab`](https://github.com/kreuzzelg/colibri/tree/gs64-ab) branch (pending
upstream). If you're on that branch and want the best quality, use this one; the
container size grows ~10 % (20 → 22 GB) and decode speed is unchanged.

## Measured accuracy (controlled A/B vs int8 anchor, same base model & engine)

| prompt | per-row int4 | gs64 int4 |
|---|---|---|
| logit cosine (mean, 4 prompts) | 0.98777 | **0.99313** |
| KL divergence (mean) | 0.1091 | **0.0795** |

Behavior: greedy 512-token generation on 4 reasoning prompts showed **no
degenerate loops** on either container — the group scaling is a quality
improvement here, not a fix for a runaway-generation bug.

## Run it

```bash
git clone -b gs64-ab https://github.com/kreuzzelg/colibri && cd colibri
make -C c qwen36                         # CPU; add CUDA=1 CUDA_ARCH=native for the GPU tier
SNAP=$(python -c "from huggingface_hub import snapshot_download; \
print(snapshot_download('Kreuzzelg/qwen36-35b-a3b-colibri-i4-gs64'))")
echo "Explain MoE routing in 100 words." > prompt.txt
SNAP=$SNAP N_NEW=200 OMP_NUM_THREADS=<physical cores> ./c/qwen36 256 4 prompt.txt
```

The engine reads `expert_gs` from `qwen36_meta.json` and picks the group-scaled
GEMV automatically; no extra flag needed.

## Container format

As the per-row container, but the expert `.qs` arrays hold one f32 scale per
`gs`=64 input elements per output row (layout `[O][I/gs]` row-major) instead of
one per row. `qwen36_meta.json` carries `expert_gs: 64`.

## Credits

- Base model: [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) (Apache-2.0)
- colibri engine & concept: [JustVugg/colibri](https://github.com/JustVugg/colibri)
- Original qwen36 engine + converter: [@minne100](https://huggingface.co/minne100)
  ([PR #602](https://github.com/JustVugg/colibri/pull/602)); group-scaled
  quantization + A/B added on top.
