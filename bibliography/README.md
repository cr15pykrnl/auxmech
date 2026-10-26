# References cited by the paper

Two final BibTeX files retain all 46 metadata-verified references cited by Paper 1.
No unresolved metadata records remain.

Use the two `.bib` files as the reusable metadata set. A verified identity does
not establish that the work supports a particular scientific claim. Read it
before reuse.

## Files

- [auxmech-verified-01.bib](auxmech-verified-01.bib)
- [auxmech-verified-02.bib](auxmech-verified-02.bib)

Original reference numbers remain in citation keys and entry comments. Each entry
records its metadata-verification source in a BibTeX comment. Corrections are
documented here; no separate CSV index is required.

These two files hold one library, split to meet the shared 500-line source limit.
The [Paper 2 candidate library](../papers/paper-2/bibliography/README.md) is separate
and remains unverified.

## Sources and method

Reviewed 26 October 2026 using the publication DOI landing pages, publisher-
deposited reference arrays from the Crossref REST API and primary publisher,
proceedings, university, government, arXiv or explicitly identified ISBN catalog records. DOI landing-page requests
to ACM and some other publishers were blocked; their deposited reference metadata
provides membership evidence rather than a claim that their full text was read.
Recovered bibliography metadata was used only after
matching it to a published reference slot; uncited manuscript entries are excluded.

DOI metadata was retrieved with `curl -sSL` from
`https://api.crossref.org/works/<doi>` and matched by identifier and title.
Malformed identifiers and conflicting dates/editions are documented below.
BibTeX syntax is checked with `bibtex` using the `plain` style and every key.
Files are split into at most 25 entries to respect the shared source-size limit.
Cross-paper duplicates remain in their separate paper lists; deduplicate by DOI
when combining lists. Citation keys are stable paper/reference-number identifiers.

The bibliography contains citation metadata only. Manuscripts, PDFs, private
archive paths and abstract text are excluded. Verification concerns bibliographic
identity, not study validity, replication or support for a future claim.

## Remaining review

No unresolved metadata records remain in this paper’s reference list.

## Recorded corrections and version choices

- `auxmech_ref002`: Full four-author list confirmed in Asthana’s Griffith thesis publication list; title, pages 10–18 and venue independently match publisher proceedings contents at https://www.proceedings.com/content/074/074141webtoc.pdf. Informit article itself was not accessible.
- `auxmech_ref014`: Publisher-deposited DOI uses a dot before 20000402; corrected to the registered colon form 10.1049/esej:20000402.
- `auxmech_ref040`: Source includes Ernest Davis as an author; selected book authors are Stuart Russell and Peter Norvig, consistent with the official third-edition site.
- `auxmech_ref017`: Book title corrected to Engineering Design Applications III; Advanced Structured Materials retained as series, volume 124, checked on Springer.
- `auxmech_ref025`: Book title corrected to Improved Performance of Materials; Advanced Structured Materials retained as series, volume 72, checked on Springer.
