#!/system/bin/sh
# Phase 1 witness — read-only snapshot of the Linux we are standing in.
# Run as root on the emulator.

echo "=== AetherOS witness ==="
date
echo
echo "=== identity ==="
id
echo
echo "=== kernel ==="
uname -a
cat /proc/version 2>/dev/null
echo
echo "=== cmdline ==="
cat /proc/cmdline 2>/dev/null
echo
echo "=== pid 1 ==="
ps -p 1 -o pid,user,cmd 2>/dev/null || tr '\0' ' ' < /proc/1/cmdline; echo
echo
echo "=== mounts (first 40) ==="
mount | head -n 40
echo
echo "=== top of / ==="
ls -la / | head -n 40
echo
echo "=== selinux ==="
getenforce 2>/dev/null || cat /sys/fs/selinux/enforce 2>/dev/null
echo
echo "=== memory ==="
head -n 5 /proc/meminfo
echo
echo "=== done ==="
