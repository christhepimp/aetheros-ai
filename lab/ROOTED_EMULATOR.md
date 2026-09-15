# Phase 0 — rooted emulator lab

Goal: a disposable Android VM where you are root and can see Linux.

## Pick one host

### Path A (recommended): Android Studio AVD + rootAVD + Magisk

This is the path that still looks like real Android and still exposes a Linux kernel you can inspect.

1. Install [Android Studio](https://developer.android.com/studio) and create an AVD.
2. Prefer an **x86_64** image with Google APIs or Play Store (API 33–36 is a good lab range).
3. Clone [rootAVD](https://gitlab.com/newbit/rootAVD).
4. Point it at *your* ramdisk, not a guess:

```bash
export ANDROID_HOME=~/Android/Sdk   # Windows: %LOCALAPPDATA%\Android\Sdk
./rootAVD.sh system-images/<api>/<variant>/x86_64/ramdisk.img FAKEBOOTIMG
```

5. Install Magisk from the official GitHub release, patch as rootAVD instructs, reboot the AVD.
6. Confirm root:

```bash
adb shell
su
id
# expect uid=0(root) gid=0(root)
uname -a
cat /proc/version
```

Write-up that tracks Android 17 / modern ramdisk pain: [Rooting an Android 17 Emulator in 2026](https://falasi.prose.sh/Rooting-an-Android-17-Emulator-in-2026).

### Path B: AERoot (no permanent patch)

[AERoot](https://github.com/quarkslab/AERoot) grants root to a process on Google Play AVDs by talking to QEMU gdb.

```bash
pip install aeroot
emulator @Your_AVD -qemu -s
aeroot daemon    # then adb shell is already root
```

Kernel table and API coverage live in that repo. Use this when you do not want to mutate the system image.

### Path C: Genymotion Desktop

Genymotion can toggle root dynamically. Older images (roughly Android 11 and below on Desktop) often boot already rooted; newer images start unrooted and you flip **Root Access** in device settings / Advanced Developer Tools.

```bash
adb root
adb shell        # you should be #
```

Docs: [Root Access — Genymotion](https://docs.genymotion.com/features/root/).

### Path D: BlueStacks 5

Settings → Advanced → enable Root + ADB. Fine for app tests. Weak for kernel replacement work. Do not treat this as the AetherOS lab.

### Path E: Waydroid on a Linux host

Android userspace in a container on *your* kernel. Best if the long-term plan is “replace Linux on a real machine,” because there is no second kernel in a VM.

## What “get in the Linux” means here

Once `id` is root:

```bash
# kernel
uname -a
cat /proc/version
cat /proc/cmdline
ls /sys

# who is PID 1
ps -p 1 -o pid,cmd
ls -l /init /system/bin/init 2>/dev/null

# mounts and userspace layout
mount
ls /
ls /system /vendor /data 2>/dev/null

# can we write anywhere interesting?
touch /data/local/tmp/aether-probe && echo ok
```

Push the witness script from this repo:

```bash
adb push lab/witness.sh /data/local/tmp/witness.sh
adb shell su -c "sh /data/local/tmp/witness.sh" > lab/last-witness.txt
```

## Safety

- Use a throwaway Google account or none.
- Do not store banking sessions in a rooted image.
- Snapshot the AVD before Phase 3 (steward with write tools).
