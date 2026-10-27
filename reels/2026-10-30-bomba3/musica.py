#!/usr/bin/env python3
"""Base instrumental original para el reel (sintetizada acá, sin material de terceros).
Uso: python3 musica.py salida.wav"""
import sys
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 44100
DUR = 15.0
N = int(SR * DUR)
t = np.arange(N) / SR
BPM = 120
BEAT = 60 / BPM
rng = np.random.default_rng(11)


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a * sr), int(d * sr), int(r * sr)
    e = np.ones(n) * s
    e[:a] = np.linspace(0, 1, a, endpoint=False)
    e[a:a + d] = np.linspace(1, s, d, endpoint=False)[: max(0, min(d, n - a))]
    if r > 0:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)


def place(buf, sig, at):
    i = int(at * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


# ---- acordes (La menor): Am9, Fmaj7, C(add9), G6 — 2 compases (4 s) cada uno
chords = [[50, 57, 60, 64, 65], [46, 53, 57, 62, 65], [53, 57, 60, 64, 67], [48, 55, 60, 64, 67]]
roots = [38, 46, 41, 48]
pad = np.zeros((N, 2))
for ci, ch in enumerate(chords):
    start, length = ci * 4.0, 4.6
    n = int(length * SR)
    tt = np.arange(n) / SR
    e = env_adsr(n, 0.9, 0.6, 0.8, 1.2)
    for m in ch:
        f = midi(m + 12)
        for k, det in enumerate([-0.12, 0.0, 0.11]):
            ff = f * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            w = (np.sin(2 * np.pi * ff * tt + ph) + 0.35 * np.sin(4 * np.pi * ff * tt + ph)
                 + 0.12 * np.sin(6 * np.pi * ff * tt + ph))
            pan = [0.5, 0.5]
            pan = [0.75, 0.25] if k == 0 else ([0.25, 0.75] if k == 2 else [0.5, 0.5])
            for c in range(2):
                place(pad[:, c], w * e * pan[c] * 0.12, start)
for c in range(2):
    pad[:, c] = lp(pad[:, c], 3200)

# ---- bombo, sub y hi-hat
kick = np.zeros(N)
kn = int(0.45 * SR)
kt = np.arange(kn) / SR
kf = 45 + 85 * np.exp(-kt * 30)
kshape = np.sin(2 * np.pi * np.cumsum(kf) / SR) * np.exp(-kt * 9) + 0.15 * rng.standard_normal(kn) * np.exp(-kt * 120)
kick_times = [2.6 + b * BEAT for b in range(30) if 2.6 + b * BEAT < 7.6] + [8.05 + b * BEAT for b in range(30) if 8.05 + b * BEAT < 12.0] + [12.55]
for kt0 in kick_times:
    place(kick, kshape * 0.42, kt0)

# compresión lateral: el pad respira con el bombo
duck = np.ones(N)
dn = int(0.35 * SR)
dshape = 1 - 0.55 * np.exp(-np.arange(dn) / SR * 9)
for kt0 in kick_times:
    i = int(kt0 * SR)
    j = min(N, i + dn)
    duck[i:j] = np.minimum(duck[i:j], dshape[: j - i])
pad *= duck[:, None]

sub = np.zeros(N)
for ci, r in enumerate(roots):
    for b in range(8):
        at = ci * 4.0 + b * BEAT
        if not ((2.6 <= at < 7.6) or (8.05 <= at < 12.0)):
            continue
        n = int(BEAT * SR)
        tt = np.arange(n) / SR
        e = env_adsr(n, 0.02, 0.1, 0.7, 0.12)
        place(sub, np.sin(2 * np.pi * midi(r) * tt) * e * 0.13, at)

hat = np.zeros(N)
hn = int(0.08 * SR)
hshape = hp(rng.standard_normal(hn), 7000) * np.exp(-np.arange(hn) / SR * 60)
for b in range(int(DUR / BEAT) * 2):
    at = b * BEAT / 2
    if 3.0 <= at < 7.6:
        place(hat, hshape * (0.30 if b % 2 else 0.12), at)
        place(hat, hshape * 0.08, at + BEAT / 4)
    elif 9.0 <= at < 12.0:
        place(hat, hshape * (0.30 if b % 2 else 0.12), at)

# ---- melodía de campanitas (pluck) en los cambios de pantalla
pluck = np.zeros(N)
notes = [(0.05, 84), (0.2, 88), (9.6, 81), (9.72, 86), (9.84, 89), (12.55, 77), (12.8, 81), (13.05, 84), (13.6, 88)]
for at, m in notes:
    n = int(1.2 * SR)
    tt = np.arange(n) / SR
    f = midi(m)
    w = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 6)) * np.exp(-tt * 4.5)
    place(pluck, w * 0.20, at)

# ---- clics de interfaz y barridos de transición
fx = np.zeros(N)
cn = int(0.05 * SR)
click = hp(rng.standard_normal(cn), 2500) * np.exp(-np.arange(cn) / SR * 160) * 0.25
for at in [8.55 + k * 0.1 for k in range(6)]:
    place(fx, click * 0.8, at)


def sweep(a, b, f0, f1, gain):
    n = int((b - a) * SR)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    seg = 512
    for i in range(0, n, seg):
        fc = f0 * (f1 / f0) ** (i / n)
        out[i:i + seg] = sosfilt(butter(2, [fc * 0.7, fc * 1.3], 'band', fs=SR, output='sos'), x[i:i + seg])
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    place(fx, out * e * gain, a)


sweep(2.2, 2.8, 500, 5000, 0.30)
sweep(7.0, 7.95, 300, 7000, 0.38)
sweep(11.9, 12.6, 6000, 500, 0.30)

# ---- reverb simple
ir_n = int(1.6 * SR)
ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 3.2)
ir /= np.sqrt(np.sum(ir ** 2))
wet_src = pluck + fx * 0.6
wetL = fftconvolve(wet_src, ir)[:N]
wetR = fftconvolve(wet_src, np.roll(ir, 331))[:N]

mix = np.zeros((N, 2))
mix += pad
for c, w in enumerate([wetL, wetR]):
    mix[:, c] += kick + sub + hat + pluck + fx + 0.35 * w
# fundido de salida
fo = int(1.4 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
fi = int(0.05 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix /= np.max(np.abs(mix)) / 0.89
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print('ok', sys.argv[1])
