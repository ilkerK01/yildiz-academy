---
lang: en
slug: aci-piramidi
title: Pyramid of Pain
summary: A model showing how much pain you cause an attacker by blocking each kind of indicator.
---

The model proposed by David Bianco in 2013 ranks how much cost blocking an
indicator imposes on an attacker. Moving from the bottom up, the attacker's job
gets harder.

## The levels

1. **Hash values.** The easiest to block and the cheapest for the attacker to
   evade. Change a single byte in the file and the hash changes.
2. **IP addresses.** A bit more effort, but getting a new address from a cloud
   provider takes minutes.
3. **Domain names.** They require registration and configuration, so they are
   somewhat more expensive.
4. **Network and host artifacts.** User-agent strings, registry keys, file
   paths. The attacker has to change their tools.
5. **Tools.** The attacker is forced to abandon the software they use.
6. **TTPs.** Tactics, techniques and procedures. If you detect at this level,
   the attacker has to change the way they operate, and that is genuinely
   expensive.

## What it means in practice

Blocking a list of hashes is not a bad thing; it is cheap and automatic. But if
the **entire** defense program sits at the bottom of the pyramid, the attacker
never feels any pain.

Detection investment gets more expensive and slower as it moves up, but it
lasts. A TTP detection can work for years; a hash signature works for a week.

## Seeing it in a lab

The `hash-avi` lab works exactly at the bottom of the pyramid: you are given a
hash and expected to climb upward from it.
