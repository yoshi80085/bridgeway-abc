SUMMER 2026 PHOTO FOLDER
========================
147 photos, live on summer-2026.html

WHAT'S IN HERE
--------------
  *.webp          full-size (max 1800px) - shown in the lightbox when clicked
  thumbs/*.webp   small (max 640px)      - shown in the photo grid
  *.jpeg / *.jpg  YOUR ORIGINALS - safe to delete, backed up in ../_originals/

SECTIONS (in the order they appear on the page)
-----------------------------------------------
  arrival        10     waterwars      20
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

CAPTIONS
--------
In summer-2026.html, find the "captions" object in GALLERY_CONFIG:
    captions: {
      'bonfire-3.webp': 'Marshmallow time!',
    }

UPLOADING TO YOUR HOST
----------------------
Upload:      summer-2026.html, summer-2026/*.webp, summer-2026/thumbs/
Do NOT upload: ../_originals/  (610 MB of full-size photos)
