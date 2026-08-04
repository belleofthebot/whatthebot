# whatthebot

The code behind **belleofthebot.com**: plain language walkthroughs of things
that are hard to see clearly.

Built by Elizabeth Beier. Static HTML, CSS and JavaScript. No framework, no
build step for the browser, no dependencies, no tracking.

## Structure

```
index.html      the home page. Introduces the project, indexes the explainers.
risk/           explainer one: what people mean when they argue about AI risk
belle.css       design tokens and every component class, shared
belle.js        the widgets, shared, plain JS
build.py        the generator
assets/         finished hero art
```

One folder per explainer. Adding a second one means a new folder and a new card
on the home page, not a new repo.

## Inside `risk/`

| page | what it is | interaction |
|---|---|---|
| `index.html` | the hub for this explainer | |
| `pipeline.html` | How a language model gets made, stage 0 through 5 | stepped walkthrough, a diagram per step |
| `taxonomy.html` | The two axes: how bad, and how it happens | clickable 3 x 4 grid |
| `pdoom.html` | The number, and why it is a weak instrument | definition builder, 24 combinations |
| `words.html` | The vocabulary | 8 question quiz plus a 14 term glossary |

Every page cross links to the others at the foot.

## The one rule the site runs on

Every substantive claim carries one of three flags:

- **measured**: a study, survey or evaluation actually counted something
- **someone's estimate**: a named person said it, which makes the saying a
  fact and the belief still a belief
- **argument**: philosophical, and cannot be settled by data

Letting these three blur together is the usual failure of writing on this
subject, so they are marked everywhere rather than left to tone.

## Editing

Every HTML file is **generated**. Do not edit them by hand, they will be
overwritten. Edit `build.py` and run it:

```
python3 build.py
```

That is the only place page chrome, nav and footer live, so a change there
lands on every page at once. Two page writers:

- `rootpage(...)` writes to the repo root, with `base=""` for asset paths
- `page(...)` writes into `risk/`, with `base="../"`

A future explainer wants its own writer on the same pattern.

`belle.css` carries design tokens and every component class. `belle.js` carries
the widgets. Each widget degrades to readable static content if JavaScript does
not run, and all animation is switched off under `prefers-reduced-motion`.

## Hero illustrations

Both the home page and the risk hub carry a placeholder Belle figure drawn in
inline SVG, marked `hero illustration placeholder`. The `belle()` function in
`build.py` takes the three lines of terminal text, so each placeholder can say
something different. Replacing one means dropping the finished image into
`assets/` and swapping the SVG block.

## Deploying

It is a static folder, so any host works. No build command, no output
directory.

**Vercel:** import the repo, framework preset "Other", leave build and output
settings empty. Then add `belleofthebot.com` under the project's domain
settings and follow the DNS instructions. Note that the domain currently 302
forwards to elizabethbportfolio.com, so that forward has to come off at the
registrar first.

**GitHub Pages:** Settings, then Pages, then Source: Deploy from a branch,
`main` / root.

## Design system

Colour, type and spacing follow the belleofthebot design system. Three rules
that matter if you extend it: rose appears at two depths only, mint is a pulse
and never a fill, and long prose sits in ivory wells rather than on the dark
ground.
