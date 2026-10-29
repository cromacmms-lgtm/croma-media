#!/bin/bash
# Renderiza, pone música y codifica cada reel del plan: reels/render_lote.sh <carpeta-temporal> <slug>...
TMP=$1; shift
export NODE_PATH=${NODE_PATH:-/home/claude/croma/scripts/node_modules}
for S in "$@"; do
  F=$TMP/$S; rm -rf $F; mkdir -p $F/frames
  node reels/render-reel.js reels/$S/index.html $F/frames || { echo "FALLO render $S"; continue; }
  python3 reels/musica_gen.py reels/$S/musica.json $F/musica.wav >/dev/null
  mkdir -p media/$S
  ffmpeg -y -loglevel error -framerate 30 -i $F/frames/f%04d.jpg -i $F/musica.wav -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
    -profile:v high -level 4.1 -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart media/$S/reel.mp4
  P=$(python3 -c "import sys;sys.path.insert(0,'reels');import plan;print([r for r in plan.REELS if r['slug']=='$S'][0]['portada'])")
  N=$(python3 -c "print('%04d' % int($P*30))")
  cp $F/frames/f$N.jpg media/$S/portada.jpg
  ffmpeg -y -loglevel error -i media/$S/reel.mp4 -vf scale=540:960 -c:v libx264 -crf 30 -preset veryfast -c:a aac -b:a 96k -movflags +faststart $TMP/$S-preview.mp4
  rm -rf $F/frames
  echo "listo $S $(du -h media/$S/reel.mp4 | cut -f1)"
done
