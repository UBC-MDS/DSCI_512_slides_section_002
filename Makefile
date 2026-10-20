# Image generation needs a .env with OPENAI_API_KEY (see .env.example)
# and the images dependency group: uv sync --group images

.PHONY: images images-index render slide

images:  ## generate every missing image in the lecture 2 prompt CSV
	uv run --group images python scripts/generate_images.py --csv website/slides/lec06_image_prompts.csv

images-index:  ## regenerate specific CSV rows, e.g. make images-index INDEX=3 or INDEX=1,4-6
	uv run --group images python scripts/generate_images.py --csv website/slides/lec06_image_prompts.csv --index $(INDEX) --overwrite

render:  ## render one deck, e.g. make render DECK=slides_02
	cd website && quarto render slides/$(DECK).qmd

slide:  ## render one deck by its lecture number, e.g. make slide N=2
	cd website && quarto render slides/slides_$(shell printf '%02d' $(N)).qmd
