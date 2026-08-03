# A plain language map of AI risk

Four interconnected walkthroughs that take apart the vocabulary people use when
they argue about AI risk, show where the real disagreements are, and separate
what has been measured from what is being argued.

Built by Elizabeth Beier. Static HTML, CSS and JavaScript. No framework, no
build step for the browser, no dependencies, no tracking.

## The four pieces

| page | what it is | interaction |
|---|---|---|
| `pipeline.html` | How a language model gets made, stage 0 through 5 | stepped walkthrough, a diagram per step |
| `taxonomy.html` | The two axes: how bad, and how it happens | clickable 3 x 4 grid |
| `pdoom.html` | The number, and why it is a weak instrument | definition builder, 24 combinations |
| `words.html` | The vocabulary | 8 question quiz plus a 14 term glossary |

`index.html` is the hub. Every page cross links to the others at the foot.

## The one rule the site runs on

Every substantive claim carries one of three flags:

- **measured**: a study, survey or evaluation actually counted something
- **someone's estimate**: a named person said it, which makes the saying a
  fact and the belief still a belief
- **argument**: philosophical, and cannot be settled by data

Letting these three blur together is the usual failure of writing on this
subject, so they are marked everywhere rather than left to tone.

## Editing

The five HTML files are **generated**. Do not edit them by hand, they will be
overwritten. Edit `build.py` and run it:

```
python3 build.py
```

That is the only place page chrome, nav and footer live, so a change there
lands on all five pages at once.

- `belle.css` carries design tokens and every component class
- `belle.js` carries the four widgets, plain JS, no dependencies

Each widget degrades to readable static content if JavaScript does not run,
and all animation is switched off under `prefers-reduced-motion`.

## Hero illustrations

`index.html` carries a placeholder Belle figure drawn in inline SVG, marked
`hero illustration placeholder`. Each of the four pages has a slot reserved at
the top for finished art. Replacing a placeholder means dropping the image into
`assets/` and swapping the SVG block in `build.py`.

## Deploying

It is a static folder, so any host works.

**GitHub Pages:** push, then Settings → Pages → Source: Deploy from a branch →
`main` / `root`.

**Vercel:** import the repo, framework preset "Other", leave build and output
settings empty.

## Design system

Colour, type and spacing follow the belleofthebot design system. Three rules
that matter if you extend it: rose appears at two depths only, mint is a pulse
and never a fill, and long prose sits in ivory wells rather than on the dark
ground.
