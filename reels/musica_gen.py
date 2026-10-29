#!/usr/bin/env python3
"""Base instrumental original para un reel, sincronizada con sus escenas (sin material de terceros).
Uso: python3 reels/musica_gen.py reels/<slug>/musica.json salida.wav"""
import sys, json
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

cfg = json.load(open(sys.argv[1]))
SR = 44100
DUR, END, CUES = cfg['dur'], cfg['end'], cfg['cues']
N = int(SR * DUR)
BPM = cfg.get('bpm', 120)
BEAT = 60 / BPM
KEY = cfg.get('key', 0)
rng = np.random.default_rng(cfg.get('seed', 7))

PROGS = [
    [[57, 60, 64, 67, 71], [53, 57, 60, 64, 69], [48, 55, 60, 62, 64], [55, 59, 62, 64, 67]],   # Am9 F C G
    [[50, 57, 60, 64, 65], [46, 53, 57, 62, 65], [53, 57, 60, 64, 67], [48, 55, 60, 64, 67]],   # Dm Bb F C
    [[52, 59, 62, 66, 67], [48, 55, 59, 62, 64], [55, 59, 62, 66, 69], [50, 57, 62, 66, 69]],   # Em C G D
    [[55, 59, 62, 66, 69], [52, 55, 59, 62, 66], [48, 55, 60, 64, 67], [50, 54, 57, 62, 64]],   # G Em C D
]
prog = PROGS[cfg.get('seed', 7) % len(PROGS)]
SCALE = [0, 2, 3, 5, 7, 9, 10]


def midi(m):
    return 440.0 * 2 ** ((m + KEY - 69) / 12)


def env(n, a, d, s, r):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    e = np.ones(n) * s
    e[:a] = np.linspace(0, 1, a, endpoint=False)
    dd = max(0, min(d, n - a))
    e[a:a + dd] = np.linspace(1, s, d, endpoint=False)[:dd]
    if r > 0:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def lp(x, fc):
    return sosfilt(butter(2, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc):
    return sosfilt(butter(2, fc, 'high', fs=SR, output='sos'), x)


def place(buf, sig, at):
    i = int(at * SR)
    j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf):
        buf[i:j] += sig[: j - i]


# pad
pad = np.zeros((N, 2))
nch = int(np.ceil(DUR / 4.0)) + 1
for ci in range(nch):
    ch = prog[ci % 4]
    n = int(4.6 * SR)
    tt = np.arange(n) / SR
    e = env(n, 0.9, 0.6, 0.8, 1.2)
    for m in ch:
        f = midi(m + 12)
        for k, det in enumerate([-0.12, 0.0, 0.11]):
            ff = f * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            w = np.sin(2*np.pi*ff*tt+ph) + .35*np.sin(4*np.pi*ff*tt+ph) + .12*np.sin(6*np.pi*ff*tt+ph)
            pan = [0.75, 0.25] if k == 0 else ([0.25, 0.75] if k == 2 else [0.5, 0.5])
            for c in range(2):
                place(pad[:, c], w * e * pan[c] * 0.12, ci * 4.0)
for c in range(2):
    pad[:, c] = lp(pad[:, c], 3200)

# ritmo
k0, k1 = (CUES[0] + 0.5), END - 0.4
kick_times = [k0 + b * BEAT for b in range(400) if k0 + b * BEAT < k1] + [END]
kn = int(0.45 * SR)
kt = np.arange(kn) / SR
kf = 45 + 85 * np.exp(-kt * 30)
kshape = np.sin(2*np.pi*np.cumsum(kf)/SR) * np.exp(-kt*9) + 0.15*rng.standard_normal(kn)*np.exp(-kt*120)
kick = np.zeros(N)
for a in kick_times:
    place(kick, kshape * 0.42, a)
duck = np.ones(N)
dn = int(0.35 * SR)
dsh = 1 - 0.55 * np.exp(-np.arange(dn) / SR * 9)
for a in kick_times:
    i = int(a * SR); j = min(N, i + dn)
    duck[i:j] = np.minimum(duck[i:j], dsh[: j - i])
pad *= duck[:, None]

sub = np.zeros(N)
for ci in range(nch):
    r = prog[ci % 4][0] - 12
    for b in range(8):
        a = ci * 4.0 + b * BEAT
        if not (k0 <= a < k1):
            continue
        n = int(BEAT * SR)
        place(sub, np.sin(2*np.pi*midi(r)*np.arange(n)/SR) * env(n, .02, .1, .7, .12) * 0.13, a)

hat = np.zeros(N)
hn = int(0.08 * SR)
hsh = hp(rng.standard_normal(hn), 7000) * np.exp(-np.arange(hn) / SR * 60)
h0 = CUES[1] if len(CUES) > 1 else k0
for b in range(int(DUR / BEAT) * 2):
    a = b * BEAT / 2
    if h0 <= a < k1:
        place(hat, hsh * (0.30 if b % 2 else 0.12), a)

# campanitas en cada escena y en el cierre
root = prog[0][0] + 24
pluck = np.zeros(N)
notes = []
for i, c in enumerate(CUES):
    notes.append((c, root + SCALE[(i * 2) % 7] + 12 * ((i * 2) // 7)))
for j, d in enumerate([0, 3, 7, 12]):
    notes.append((END + j * 0.25 + (0.25 if j == 3 else 0), root - 12 + d + 12))
for a, m in notes:
    n = int(1.2 * SR)
    tt = np.arange(n) / SR
    f = midi(m)
    w = (np.sin(2*np.pi*f*tt) + .4*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*6)) * np.exp(-tt*4.5)
    place(pluck, w * 0.2, a)

fx = np.zeros(N)
cn = int(0.05 * SR)
click = hp(rng.standard_normal(cn), 2500) * np.exp(-np.arange(cn) / SR * 160) * 0.25
for a in CUES[1:]:
    place(fx, click, a)


def sweep(a, b, f0, f1, gain):
    n = int((b - a) * SR)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    seg = 512
    for i in range(0, n, seg):
        fc = f0 * (f1 / f0) ** (i / n)
        out[i:i+seg] = sosfilt(butter(2, [fc*.7, fc*1.3], 'band', fs=SR, output='sos'), x[i:i+seg])
    place(fx, out * np.sin(np.linspace(0, np.pi, n)) ** 2 * gain, a)


sweep(0.0, 0.8, 400, 5000, 0.30)
sweep(END - 0.7, END, 6000, 500, 0.30)

irn = int(1.6 * SR)
ir = rng.standard_normal(irn) * np.exp(-np.arange(irn) / SR * 3.2)
ir /= np.sqrt(np.sum(ir ** 2))
wsrc = pluck + fx * 0.6
wl, wr = fftconvolve(wsrc, ir)[:N], fftconvolve(wsrc, np.roll(ir, 331))[:N]
mix = pad.copy()
for c, w in enumerate([wl, wr]):
    mix[:, c] += kick + sub + hat + pluck + fx + 0.35 * w
fo = int(1.4 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
fi = int(0.05 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix /= np.max(np.abs(mix)) / 0.89
wavfile.write(sys.argv[2], SR, (mix * 32767).astype(np.int16))
print('ok', sys.argv[2])
