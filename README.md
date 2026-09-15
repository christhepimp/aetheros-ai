# AetherOS

**An AI-native operating system grown inside a rooted Android/Linux lab.**

AetherOS does not start by rewriting the kernel on day one. It starts where we can actually get root, inspect Linux, and *replace pieces of userspace one subsystem at a time* until the machine is no longer “Android + Linux + apps” but “an AI that *is* the OS.”

This repository is the lab, the architecture, and the first code.

## The idea

Traditional OS stack:

```
Hardware → Kernel (Linux) → Init / systemd → Services → Apps → You type commands
```

AetherOS target stack:

```
Hardware → Thin kernel / hypervisor (keep Linux only as long as needed)
        → Cognition runtime (the OS itself is an agent)
        → Tools, drivers, and capabilities as skills
        → You speak intent; the OS plans and acts
```

You do not “open an app and ask an AI.” The scheduler, the shell, the package manager, and the window manager *are* the AI.

## Why a rooted Android emulator first

Android already *is* Linux. A rooted emulator gives:

- `uid=0` (real root)
- `adb shell` into a live Linux userspace
- Visible kernel (`/proc`, `/sys`, `dmesg`)
- Ability to replace init children, mount overlays, inject services
- A disposable lab that will not brick a phone

### Recommended lab hosts (2026)

| Tool | Root story | Why use it |
| --- | --- | --- |
| **Android Studio AVD + rootAVD + Magisk** | Patch ramdisk, install Magisk | Official images, closest to real Android, kernel visible |
| **AERoot** | On-the-fly root for Play AVDs via QEMU gdb | No permanent image patch; good for experiments |
| **Genymotion Desktop** | Dynamic root toggle on many images | Fast, documented root, `adb root` / `su` |
| **BlueStacks 5** | Settings → Advanced → Root | Easy, but more closed; worse for kernel work |
| **Waydroid** (Linux host) | Android userspace on *host* kernel | Best if you already live in Linux |

**Primary path for this repo:** Android Studio AVD (x86_64 Google APIs / Play image) + [rootAVD](https://gitlab.com/newbit/rootAVD) + Magisk, with [AERoot](https://github.com/quarkslab/AERoot) as a fallback.

You cannot “replace Linux” from a closed gaming emulator. You need a system image you can inspect and a kernel you can talk to.

## Honest scope

Replacing Linux *the kernel* is a multi-year systems project (bootloader, drivers, memory, scheduling, filesystems). Claiming that is done in one repo would be a lie.

What *is* done here:

1. A lab recipe to get root on an Android emulator and stand inside Linux.
2. A **cognition runtime** that sits *above* the kernel and slowly owns: shell, init services, package install, file ops, process policy.
3. An overlay strategy: keep Linux as the substrate, replace userspace *roles* with an agent that has tools.
4. A written path from “AI on Linux” → “AI *is* PID 1” → “kernel is just a driver layer.”

## Repo map

```
lab/                 How to boot a rooted emulator and enter Linux
runtime/             Aether cognition process (the OS brain)
skills/              Tools the OS is allowed to use (shell, fs, pkg, proc)
policy/              What the AI may and may not do as root
docs/architecture    How replacement happens in phases
```

## Phases

| Phase | Name | What we replace |
| --- | --- | --- |
| 0 | Lab | Nothing. Get root. Prove `id` is `uid=0`. |
| 1 | Witness | Read-only: kernel version, mounts, init, running procs. |
| 2 | Shell | `aether` becomes the interactive shell instead of `sh`. |
| 3 | Steward | Aether owns selected services (logging, package install, file policy). |
| 4 | Init | Aether is started from init; it supervises userspace. |
| 5 | Substrate | Custom kernel / unikernel / hypervisor. Linux is optional. |

We are building Phase 0–3 in this repo. Phase 5 is documented, not shipped.

## Quick start (host)

```bash
# cognition runtime (no emulator required to try the brain)
cd runtime
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m aether.cli "what is this machine and what should an OS do next?"
```

Lab setup lives in [`lab/ROOTED_EMULATOR.md`](lab/ROOTED_EMULATOR.md).

## License

MIT. Experiment. Do not run the steward against a device you care about until you have read `policy/`.
