# Cut out portraits

Drop a background-free `.webp` (or `.png`) here, named for the card key, and the
tile and the card both switch from Belle to the photograph automatically. Remove
it and they switch back. Nothing needs rebuilding except `site.py`.

    assets/people/hinton.webp
    assets/people/altman.webp
    assets/people/amodei.webp
    assets/people/hassabis.webp
    assets/people/bengio.webp

Portrait orientation, background removed, roughly 700px tall, saved as WebP.
They are rendered black and white in CSS, so colour originals are fine.

Every one needs a credit. The credit lines live in `photosrc` on each spec in
`social/carousels.py`, and are already written for the five above. If you use a
different photograph, change the line to match it.

## Verified sources, all reusable with attribution

| person   | source                                                    | licence      |
|----------|-----------------------------------------------------------|--------------|
| Hinton   | flickr.com/photos/collisionconf/53803072514               | CC BY 2.0    |
| Altman   | flickr.com/photos/techcrunch/36522988343                  | CC BY 2.0    |
| Amodei   | flickr.com/photos/techcrunch/53201955583                  | CC BY 2.0    |
| Hassabis | flickr.com/photos/dullhunk/53272768070                    | CC BY 2.0    |
| Bengio   | flickr.com/photos/117994717@N06/36864664805               | CC BY-SA 2.0 |

CC BY 2.0 asks for the photographer credited and a note that the image was
changed. Cutting out a background and desaturating both count as changing it.
Bengio's is **share alike**, which additionally means the modified image has to
carry the same licence. Open each page and copy the credit line yourself before
publishing: uploaders do change licences.

**Not resolved.** No reusable photograph was found for Yann LeCun or Emily
Bender. The ACM Turing Award photographs of LeCun are all rights reserved, and
Bender's university headshot carries no licence, which means the same thing.
Those two cards keep Belle until somebody asks them directly.
