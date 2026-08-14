SUMMER 2026 PHOTO FOLDER
========================
147 photos + 1 video, live on summer-2026.html

WHAT'S IN HERE
--------------
  *.webp          full-size (max 1800px) - shown in the lightbox when clicked
  thumbs/*.webp   small (max 640px)      - shown in the photo grid
  *.mp4           videos - play in the lightbox (see VIDEOS below)
  *.mov           YOUR ORIGINAL VIDEOS - not used by the page, don't upload them
  *.jpeg / *.jpg  YOUR ORIGINALS - safe to delete, backed up in ../_originals/

SECTIONS (in the order they appear on the page)
-----------------------------------------------
  arrival        10     waterwars      20 + movie
  orientation     1     waterslide     19
  woodchop        4     freetime       15
  firebuild      10     teacher         4
  cooking        18     groupphoto      1
  curry          18
  monster        16     TOTAL         147
  bonfire        11

TO ADD OR REMOVE PHOTOS
-----------------------
Numbers must run 1..N with no gaps. Add the next number in the sequence
(e.g. bonfire-12.webp) to BOTH this folder and thumbs/, then bump the
"count" for that section in the GALLERY_CONFIG block in summer-2026.html.

Easier: drop new photos in and ask Claude to process them.

VIDEOS
------
waterwars-movie.mp4 plays as the first tile in the Water Wars section.
Three files make it work:
    waterwars-movie.mp4          the video (H.264 mp4 - plays everywhere)
    waterwars-movie.webp         poster still, full size
    thumbs/waterwars-movie.webp  poster still, small (the grid tile)
and one entry in the "videos" list in GALLERY_CONFIG in summer-2026.html.

Phone videos are usually .mov and often HEVC, which Chrome and Firefox
cannot play - they must be converted to H.264 .mp4 first. Drop the .mov
in here and ask Claude to do it. The original .mov can stay in the folder;
the page ignores it, just don't upload it to the host.

CAPTIONS
--------
In summer-2026.html, find the "captions" object in GALLERY_CONFIG:
    captions: {
      'bonfire-3.webp': 'Marshmallow time!',
    }
Videos carry their caption in the "videos" list instead.

UPLOADING TO YOUR HOST
----------------------
Upload:      summer-2026.html, summer-2026/*.webp, summer-2026/*.mp4,
             summer-2026/thumbs/
Do NOT upload: ../_originals/  (610 MB of full-size photos)
               summer-2026/*.mov  (54 MB original, the .mp4 replaces it)
