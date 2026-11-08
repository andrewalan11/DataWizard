---
title: YAML Schema
type: protocol
created: '2026-06-13'
updated: 2026-11-08
origin: 'DW-S182 2026-06-13; DW-S484 2026-11-08 - sectioned into a shell and four section files in YAML Schema/ (Conventions Registry 7.0); the edit_log up to the split is in the pre-split copy, xArchive - DataWizard/Seed/Protocols/YAML Schema.md.pre-S484.bak'
operator: Andrew
priority: high
maturity: working
---

# YAML Schema

The frontmatter field schema for DataWizard vaults. Layout: one section file per theme, read in number order. Edit the section files in `YAML Schema/`, never this shell. New fields go in the section of their theme; when a section passes about 30 KB, start a continuation file (Conventions Registry 7.0).

![[1.0 YAML Schema - Core Fields]]

![[2.0 YAML Schema - Harvest and Federation]]

![[3.0 YAML Schema - Holonic Records and Tool Evaluation]]

![[4.0 YAML Schema - Dates, Provenance and AI Content]]
