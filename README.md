# NeurIPS 2025 Paper Template

This directory contains cleaned template files for writing a NeurIPS 2025 conference paper.

## Directory Structure

```
.
├── neurips_2025.tex        # Main paper file (NeurIPS format)
├── arxiv.tex               # ArXiv version (with enhanced formatting)
├── camera_ready.tex        # Camera-ready version
├── appendix.tex            # Appendix content
├── neurips_2025.bib        # Bibliography file
├── arxiv.bib               # Bibliography file (ArXiv version)
├── neurips_2025.sty        # NeurIPS 2025 style file (DO NOT MODIFY)
├── arxiv.sty               # ArXiv style file (DO NOT MODIFY)
└── Fig/                    # Directory for figures (currently empty)
```

## Usage

1. **Main Paper**: Edit `neurips_2025.tex` for your NeurIPS submission
2. **ArXiv Version**: Use `arxiv.tex` for ArXiv preprint (includes additional formatting options)
3. **Figures**: Place all your figures in the `Fig/` directory
4. **References**: Add your bibliography entries to `neurips_2025.bib` or `arxiv.bib`
5. **Appendix**: Add supplementary material to `appendix.tex`

## Compilation

To compile the paper, use:

```bash
pdflatex neurips_2025.tex
bibtex neurips_2025
pdflatex neurips_2025.tex
pdflatex neurips_2025.tex
```

Or for the ArXiv version:

```bash
pdflatex arxiv.tex
bibtex arxiv
pdflatex arxiv.tex
pdflatex arxiv.tex
```

## Template Features

### arxiv.tex includes:
- Multiple colored text boxes (promptblue, promptorange, promptgreen, etc.)
- Enhanced formatting with tcolorbox
- FontAwesome icon support
- Contact line command for email and GitHub

### neurips_2025.tex includes:
- Standard NeurIPS 2025 formatting
- Paper checklist template
- Appendix support

## Notes

- The `.sty` files are style templates and should not be modified
- All content has been cleared - ready for your new paper
- The Fig/ directory is empty and ready for your figures

