#!/usr/bin/env python3
"""Bases instrumentales originales en distintos estilos (sintetizadas acá, sin material de terceros).
Uso: python3 reels/musica_estilos.py <estilo> <musica.json | segundos> salida.wav
Estilos: house, lofi, corporativo."""
import sys, json
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
estilo = sys.argv[1]
src = sys.argv[2]
if src.endswith('.json'):
    cfg = json.load(open(src))
else:
    d = float(src)
    cfg = dict(dur=d, end=d - 2.2, cues=[0, d * .3, d * .6], seed=3)
DUR, END, CUES = cfg['dur'], cfg['end'], cfg['cues']
N = int(SR * DUR)
rng = np.random.default_rng(cfg.get('seed', 3) + 100)
BPM = {'house': 122, 'lofi': 84, 'corporativo': 108}[estilo]
BEAT = 60 / BPM


def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)


def place(buf, sig, at, gain=1.0):
    i = int(at * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf):
        buf[i:j] += sig[: j - i] * gain


def env(n, a, r):
    e = np.ones(n)
    ai = max(1, int(a * SR)); e[:ai] = np.linspace(0, 1, ai)
    e *= np.exp(-np.arange(n) / SR / max(r, 1e-3))
    return e


def kick(dec=9, f0=130, f1=45):
    n = int(.4 * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * dec)


def snare(n_dec=22, tone=190):
    n = int(.25 * SR); t = np.arange(n) / SR
    return bp(rng.standard_normal(n), 1500, 7000) * np.exp(-t * n_dec) * .7 + np.sin(2 * np.pi * tone * t) * np.exp(-t * 30) * .4


def clap():
    n = int(.22 * SR); t = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 900, 5000)
    e = np.zeros(n)
    for k, off in enumerate([0, .011, .022]):
        i = int(off * SR); e[i:] += np.exp(-(t[: n - i]) * (60 if k < 2 else 18))
    return x * e * .6


def hat(dec=55, open_=False):
    n = int((.25 if open_ else .07) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7500) * np.exp(-t * (14 if open_ else dec))


def tone(f, n, kind='saw', bright=1.0):
    t = np.arange(n) / SR
    if kind == 'saw':
        x = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9))
    elif kind == 'rhodes':
        x = np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 3)) * (1 + .08 * np.sin(2 * np.pi * 5 * t))
    elif kind == 'marimba':
        x = np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 20)
    elif kind == 'piano':
        x = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2 + k)) / k for k in range(1, 6))
    else:
        x = np.sin(2 * np.pi * f * t)
    return x


L, R = np.zeros(N), np.zeros(N)
bus = dict(drums=np.zeros(N), bass=np.zeros(N), keys=np.zeros(N), lead=np.zeros(N), fx=np.zeros(N))
start, stop = CUES[0] + .4, END - .3
nbeats = int(DUR / BEAT) + 2

if estilo == 'house':
    prog = [[57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65], [52, 55, 59, 62]]   # Am7 Fmaj7 G7 Em7
    for b in range(nbeats):
        at = b * BEAT
        if not (start <= at < stop):
            continue
        place(bus['drums'], kick(), at, .5)
        place(bus['drums'], hat(open_=True), at + BEAT / 2, .3)
        if b % 2 == 1:
            place(bus['drums'], clap(), at, .55)
        place(bus['drums'], hat(), at + BEAT / 4, .08); place(bus['drums'], hat(), at + 3 * BEAT / 4, .08)
        ch = prog[(b // 4) % 4]
        n = int(BEAT * .45 * SR)
        place(bus['bass'], lp(tone(midi(ch[0] - 24), n, 'saw'), 500) * env(n, .005, .12), at + BEAT / 2, .16)
        if b % 4 in (0, 2):
            n = int(.35 * SR)
            stab = sum(tone(midi(m), n, 'saw') for m in ch)
            place(bus['keys'], lp(stab, 3200) * env(n, .004, .09), at + (BEAT * .75 if b % 4 == 2 else 0), .2)
    arp_notes = [0, 3, 7, 12]
elif estilo == 'lofi':
    prog = [[50, 53, 57, 60, 64], [55, 59, 62, 65, 69], [48, 52, 55, 59, 62], [57, 60, 64, 67, 71]]   # Dm9 G13 Cmaj9 Am9
    for b in range(nbeats):
        at = b * BEAT
        if not (start <= at < stop):
            continue
        sw = BEAT * .58
        if b % 4 in (0, 2) or (b % 4 == 3 and b % 8 == 7):
            place(bus['drums'], lp(kick(7, 110, 48), 2500), at + (sw if b % 8 == 7 else 0), .42)
        if b % 2 == 1:
            place(bus['drums'], lp(snare(16, 180), 5000), at, .45)
        place(bus['drums'], lp(hat(70), 9000), at, .10); place(bus['drums'], lp(hat(70), 9000), at + sw, .07)
        if b % 4 == 0:
            ch = prog[(b // 4) % 4]
            n = int(BEAT * 4.2 * SR)
            keys = sum(tone(midi(m), n, 'rhodes') for m in ch)
            place(bus['keys'], lp(keys, 3400) * env(n, .02, 2.2), at, .17)
            n2 = int(BEAT * 3.8 * SR)
            place(bus['bass'], tone(midi(ch[0] - 12), n2, 'sine') * env(n2, .01, 1.6), at, .13)
    crack = (rng.random(N) < .0006) * rng.standard_normal(N) * .5 + hp(rng.standard_normal(N), 3000) * .004
    bus['fx'] += crack
    arp_notes = [0, 7, 12, 14]
else:  # corporativo
    prog = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]   # C Am F G
    for b in range(nbeats):
        at = b * BEAT
        if not (start <= at < stop):
            continue
        place(bus['drums'], kick(10, 120, 50), at, .42)
        if b % 2 == 1:
            place(bus['drums'], clap(), at, .5)
        place(bus['drums'], hat(), at + BEAT / 2, .12)
        ch = prog[(b // 4) % 4]
        for k in range(4):     # marimba en semicorcheas
            n = int(.5 * SR)
            m = ch[[0, 2, 1, 3][k]] + 12
            place(bus['lead'], tone(midi(m), n, 'marimba') * env(n, .002, .18), at + k * BEAT / 4, .2)
        n = int(BEAT * .9 * SR)
        place(bus['bass'], lp(tone(midi(ch[0] - 24), n, 'saw'), 700) * env(n, .005, .35), at, .13)
        if b % 4 == 0:
            n = int(BEAT * 4.1 * SR)
            pad = sum(tone(midi(m), n, 'piano') for m in ch)
            place(bus['keys'], pad * env(n, .005, 1.8), at, .15)
    arp_notes = [0, 4, 7, 12]

# acentos en cada escena y cierre
for i, c in enumerate(CUES):
    n = int(.9 * SR)
    root = prog[0][0] + 12
    place(bus['lead'], tone(midi(root + arp_notes[i % 4] + 12), n, 'marimba' if estilo != 'lofi' else 'rhodes') * env(n, .003, .3), c + .02, .16)
for j, d in enumerate(arp_notes):
    n = int(1.4 * SR)
    place(bus['lead'], tone(midi(prog[0][0] + 12 + d), n, 'marimba' if estilo != 'lofi' else 'rhodes') * env(n, .003, .5), END + j * .18, .16)
place(bus['drums'], kick(), END, .9 if estilo != 'lofi' else .6)
# barrido de entrada y de cierre
for a, b, f0, f1 in [(0, .8, 500, 6000), (END - .7, END, 6000, 500)]:
    n = int((b - a) * SR); x = rng.standard_normal(n); out = np.zeros(n)
    for i in range(0, n, 512):
        fc = f0 * (f1 / f0) ** (i / n)
        out[i:i + 512] = bp(x[i:i + 512], fc * .7, fc * 1.3)
    place(bus['fx'], out * np.sin(np.linspace(0, np.pi, n)) ** 2, a, .28)

# mezcla
irn = int(1.3 * SR)
ir = rng.standard_normal(irn) * np.exp(-np.arange(irn) / SR * 3.5); ir /= np.sqrt(np.sum(ir ** 2))
wet = fftconvolve(bus['keys'] * .6 + bus['lead'] + bus['fx'] * .5, ir)[:N]
mono = bus['drums'] + bus['bass'] + bus['keys'] + bus['lead'] + bus['fx']
L = mono + .3 * wet; R = mono + .3 * np.roll(wet, 337)
mix = np.stack([L, R], 1)
fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
fi = int(.03 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix /= np.max(np.abs(mix)) / .89
wavfile.write(sys.argv[3], SR, (mix * 32767).astype(np.int16))
print('ok', estilo, sys.argv[3])
