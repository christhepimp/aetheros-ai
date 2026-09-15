# How we replace Linux without pretending we already did

## Principle

Keep a working kernel. Steal userspace jobs until Linux is only a driver and syscall layer. Then, if we still need to, replace that layer.

Trying to write a from-scratch kernel *and* an AI OS in the same week produces neither.

## Phase 0 — Lab

Artifact: a rooted AVD (or Genymotion / Waydroid) and `uid=0`.

Exit criteria: `adb shell su -c id` prints root.

## Phase 1 — Witness

Artifact: `lab/witness.sh` output checked into `lab/last-witness.txt` (local, not required upstream).

The cognition runtime may only *read* facts: kernel, pid 1, mounts, memory.

## Phase 2 — Shell

Artifact: `python -m aether.cli` on the host, later `aether` binary/script on-device.

The human talks in intent. Aether plans. Skills execute. Default skills are read-only plus a sandboxed shell in `/data/local/tmp`.

This is already an OS *interface*, even while Android still owns the screen.

## Phase 3 — Steward

Aether owns named jobs:

- log collection
- package / apk install policy
- file writes under `/data/local/aether`
- process inventory

Linux still schedules. Aether decides *what is allowed to exist*.

Policy file: `policy/steward.yaml`.

## Phase 4 — Init

Start Aether from Android `init` (`.rc` service) or as a Magisk service (`service.sh`).

Aether becomes the supervisor of userspace daemons we care about. PID 1 can stay `init` for a long time. “AI is the OS” does not require Aether to be PID 1 on day one. It requires Aether to be the authority that starts and stops the rest.

## Phase 5 — Substrate

Only after Phase 4 is boring:

- custom Android kernel build (goldfish / cuttlefish / GKI)
- or drop Android and boot a Linux VM with Aether as PID 1 (`aether-init`)
- or unikernel / hypervisor where the only guest process is the cognition runtime

This phase is a *research track*, not a checkbox in this README.

## What “the OS is an AI” means in code

Not a chatbot bolted onto settings.

- **Intent in**: natural language or structured goals
- **World model**: witness facts + process table + mounts
- **Plan**: tool calls with policy gates
- **Act**: skills
- **Memory**: what was done and whether it worked
- **Loop**: the same process keeps running; it is not a one-shot script

That loop *is* the OS personality.
