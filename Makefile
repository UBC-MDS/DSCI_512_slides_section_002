# Image generation needs a .env with OPENAI_API_KEY (see .env.example)
# and the images dependency group: uv sync --group images

.PHONY: images render

images:  ## generate every missing image in the lecture 2 prompt CSV
	uv run --group images python scripts/generate_images.py --csv website/slides/lec02_image_prompts.csv

render:  ## render one deck, e.g. make render DECK=slides_02
	cd website && quarto render slides/$(DECK).qmd
