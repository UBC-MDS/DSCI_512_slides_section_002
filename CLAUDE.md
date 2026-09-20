# DSCI 512 slides (Section 002)

Lecture slides for DSCI 512 (Algorithms and Data Structures, UBC MDS).
Students see these decks live in class and study from them afterwards, so everything visible on a slide is teaching material.

## Layout

- `website/` is the Quarto website. Decks live in `website/slides/slides_NN.qmd`.
- Decks use the `live-revealjs` format (quarto-live) with `engine: jupyter`:
  - ```` ```{python} ```` cells run once at render time in the virtual environment.
  - ```` ```{pyodide} ```` cells run in the student's browser, so students can edit and rerun them.
  - ```` ```{ojs} ```` cells are the interactive charts and sliders, always hidden from students.
- `website/slides/assets/slides.css` holds shared styles, including `.ojs-readout`, `.notify`, `.match`, `.scan-row` and `.scan-box`. Reuse these before adding new ones.
- Releases are controlled in `website/_quarto.yml`. Read its header comment before adding a deck to `project: render:`.
- `scripts/generate_images.py` generates slide images via the OpenAI image API, from a prompt
  or from `website/slides/lecNN_image_prompts.csv` (`make images`). Needs a gitignored `.env`
  with `OPENAI_API_KEY` and the `images` dependency group. Prompts live in the CSV's `prompt`
  column and are sent as-is; `example.png` and `example2.png` are attached as style references.
- `_site/`, `_freeze/` and `.quarto/` are gitignored build output.

## Render and check

```bash
cd website && quarto render slides/slides_NN.qmd   # about 1–2 min; the profiling demos really sleep
```

Before saying a deck works:
1. Run every `{python}` cell in order (IPython, with a stand-in `ojs_define`) and check that none fail and that no `ojs_define` name is defined twice.
2. Render the deck.
3. When a browser is available, click through the interactive slides. OJS errors only appear at runtime.

Say plainly which of these steps you ran and which you couldn't.

## Code on slides: Python computes, OJS only draws

This is the most important rule for this repo.

- **All computation happens in Python**: measurements, formulas, curves, counts, ratios, percentages, search results and readable labels. The instructor checks the logic in Python, so it must not be hidden in JavaScript.
- **OJS only does visualization**: inputs (sliders, radios, checkboxes), filtering or looking up the precomputed data for the current input, layout, colours, and `Plot` marks.
  - Don't put formulas in OJS (`n => n ** 2`, `Math.log2`, break-even maths, and so on).
  - Don't build data arrays in OJS loops.
- Pass data from Python with `ojs_define(name = value)`, using lists of dicts or dicts keyed by the input value (e.g. `readout[n_zoom]`).
- Define each OJS name **once**, since defining a name twice is an error. OJS is reactive, so one `ojs_define` placed after the last measurement also feeds charts earlier in the deck.
- Precompute data for every value a slider can take. Keep the embedded data small: use a dense grid only where the curve bends, then a sparser one (e.g. `range(1, 201)` plus every 10th or 20th value), and round long floats.
- Charts of measured results must use the **same** numbers students see printed. For example, `record_runtime(lp, ...)` reads the total out of the visible `LineProfiler` instead of timing the call a second time.

## What students see vs. what is hidden

- **Visible (`echo: true`)**: only code students need to analyse, run or memorise, such as the algorithm, the profiling calls (`%timeit`, `cProfile`, `LineProfiler`) and runnable pyodide exercises.
- **Hidden (`#| echo: false` for Python/OJS, `#| include: false` for pyodide setup)**: everything that only supports a visualization, including helper functions, re-measurements, data prep and every OJS cell.
- Keep the visible code exactly as students would write it themselves. Don't add bookkeeping to it for the sake of a chart; put that in a hidden cell right after it.
- Hidden cells should end with statements, not bare expressions, so nothing unexpected is printed on the slide.
- Hidden Python cells share the kernel with visible ones. Don't overwrite variables students rely on (e.g. use `size` rather than `n` as a loop variable).

## Comments and annotations

- Visible code gets short teaching comments, such as `# n iterations` and `# constant time (k)`, so students can count steps and understand each line of the code.
- Every hidden cell starts with a comment saying what it prepares and for which slide. Each OJS cell has a one-line comment saying its data comes from Python.
- Comments must match the code. For example, "repeat 7 times" must go with `repeat=7`.

## Story line and teaching style

- Each lecture follows **one real-world story** that connects every concept, and all code examples come from that story. Lecture 1 uses Uber: a rider logging in (list vs. set lookup), notifying drivers (one loop, O(n)) and matching riders with drivers (nested loop, O(n²)). Future lectures may use a different story. Keep the new one consistent within its deck, and never teach a concept without a concrete application.
- Interactive charts should make the key contrast obvious at a glance, for example side-by-side panels against a shared baseline with a big "2.0×" vs. "4.0×" label. Colours must match the words in the slide text.
- Colours used so far: blue `#2a78d6` (linear / notify / constant factor), orange `#eb6834` (quadratic / match / growth with n), grey `#b8b6b0` (baseline). Chart text is 16px on a transparent background.
- Keep slide text short. Use `::: {.fragment}` / `::: {.incremental}` to reveal things step by step. Put explanations, answers to questions and live-demo cues in `::: {.notes}`.
- Emoji section markers: 🚗 story, ⏱️ profiling, 📈 complexity, 🧮 counting steps, ⚠️ caveats, 🎯 cases.
- Credit AI-generated images in a `::: footer` ("Image generated by …") and cite sources in footers.

## Classroom tools

- **Never use Agora.** It belongs to a previous instructor of this course. This section uses
  **iClicker**: [join.iclicker.com/AGFP](https://join.iclicker.com/AGFP), QR code at
  `images/iclicker_qr.png`. If you find an Agora link, code, QR or heading in a deck, convert
  it to the iClicker equivalent; student question round-ups are headed "Student Questions".

## Working with the instructor

- The instructor often edits the deck while you are working. Re-read the file before editing and keep their changes; don't revert them.
- Keep changes to the scope asked for. Mention small issues you notice elsewhere (typos in notes, etc.) instead of fixing them unasked.
- Don't commit or push unless asked.
