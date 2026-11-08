# Congressional stock network: SNA

Sean Ryan · DSA 295 (003), Introduction to Social Network Analysis · November 23, 2026

**Research question:** Which stocks connect the most U.S. House disclosure filers, and how does shared purchasing connect filers to one another?

This repository adapts my congressional disclosure and data-wrangling project for a 3–4 minute SNA presentation. It includes the presentation, frozen input data, reproducible calculations, and limitations.

## View the project

- [Presentation and project page](https://strokeofluck.github.io/congressional-stock-network-sna/)
- [Original interactive network](https://strokeofluck.github.io/congressional-stock-network-2025/)
- [Data portfolio](https://strokeofluck.github.io/sean-data-portfolio/)
- [Methods and findings](METHODS.md)
- [Data provenance](DATA_PROVENANCE.md)

The site has a **Present** button and optional speaker notes. Use left/right arrows to move between sections and **N** to toggle notes. It works as a local HTML file, with no external libraries required for the presentation itself.

## Findings from the frozen 2025 extract

- 3,179 accepted public-stock purchase records, with 55 distinct politician names and 855 tickers.
- The shared-stock graph contains 45 filers, 355 stocks, and 1,291 distinct filer–ticker ties.
- AMZN has the highest stock degree, connecting 19 filers.
- The politician projection contains 494 ties, or 49.9% of the 990 possible pairs. All 45 filers belong to one connected component.

These results describe reported purchase overlap. They do not establish coordination, privileged information, investment performance, or wrongdoing.

## Reproduce

Python 3.11+:

```sh
python -m pip install -r requirements.txt
python scripts/build.py
python -m http.server 8000 --directory site
```

Open `http://localhost:8000/`, or open `site/index.html` directly. The build checks the input scope and independently verifies the projected edge count. Results are saved in `site/analysis.json`.

## Files

| Path | Contents |
|---|---|
| `site/index.html` | Self-contained presentation and research summary |
| `data/PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv` | Frozen input extract |
| `scripts/build.py` | Reproducible graph calculations and page build |
| `site/analysis.json` | Machine-readable findings |
| `METHODS.md` | Node/tie definitions, measures, findings, interpretation |
| `DATA_PROVENANCE.md` | Original sources, scope, limitations |

## Course delivery

The instructions request a 3–4 minute oral presentation covering the topic/questions, data, and analysis results with interpretation. HTML, PDF, PowerPoint, or Google Slides are accepted. Upload the presentation document to Moodle by 1 PM on November 23. The repository link supports the presentation and does not replace the required Moodle upload. Confirm the separate final-project rubric before submitting the final project.

## Relationship to my other projects

`house-ptr-scraper` owns data extraction and cleaning. `congressional-stock-network-2025` owns the original interactive analysis, including historical committee context. This repository owns the SNA presentation and the shared-stock calculations shown here. The portfolio links to these projects.

Prepared with AI assistance. Sean Ryan should review the analysis and rehearse the presentation before submission.
