# Submission form specification — The Economic Review at W&M

Spec for rebuilding the Google Form behind the "Open the submission form"
button (`_data/journal.yml → submission_form_url`; update that key if the
form's URL changes). Structure: one common section → track question with
**section branching** → track-specific section(s) → common attestations →
confirmation.

Conventions below: **[req]** = required, *[opt]* = optional. "Help text"
is the grey description under the question.

---

## Section 1 — About you

| # | Field | Type | Req | Help text |
|---|---|---|---|---|
| 1.1 | Full name | Short answer | [req] | As it should appear in print if accepted. |
| 1.2 | W&M email | Short answer, response validation: contains `@wm.edu` | [req] | We correspond only through your W&M address. |
| 1.3 | Class year | Dropdown: 2027 / 2028 / 2029 / 2030 / Graduate student | [req] | — |
| 1.4 | Major(s) | Short answer | [req] | Any major is welcome — this is for our records, not a filter. |
| 1.5 | How did you hear about the Review? | Dropdown: Professor or class announcement / Interest meeting or event / Instagram / A friend / TribeLink / Other… | *[opt]* | Helps us know what's working. |

## Section 2 — Track selection (drives branching)

| # | Field | Type | Req | Help text |
|---|---|---|---|---|
| 2.1 | Which track are you submitting to? | Multiple choice, **"Go to section based on answer"**: Research → Section 3; Perspectives → Section 4 | [req] | Research: a full paper, reviewed double-blind against the semester deadline. Perspectives: a 600–1,200 word op-ed or policy brief, reviewed by editors on a rolling basis. |

## Section 3 — Research submission (branch A)

| # | Field | Type | Req | Help text |
|---|---|---|---|---|
| 3.1 | Paper title | Short answer | [req] | — |
| 3.2 | Abstract | Paragraph | [req] | 250 words maximum. |
| 3.3 | Keywords | Short answer | [req] | 3–5, comma-separated. |
| 3.4 | JEL codes | Short answer | *[opt]* | If you know them (e.g. J38, O15). Leave blank otherwise. |
| 3.5 | Word count | Short answer, numeric validation | [req] | Of the manuscript body, excluding references and tables. |
| 3.6 | Where did this paper come from? | Dropdown: Course paper (name course & professor in the next question) / Independent research / Honors thesis / Other… | [req] | — |
| 3.7 | Course and professor, or other origin detail | Short answer | *[opt]* | E.g. "ECON 456, Prof. McHenry, Fall 2026". |
| 3.8 | Faculty sponsor | Short answer | *[opt]* | A professor who knows the work and is willing to be contacted. Not required. |
| 3.9 | Co-authors | Paragraph | *[opt]* | One per line: name, email, institution. Co-authors from other schools are welcome; the submitting author must be a current W&M student. |
| 3.10 | **Anonymized manuscript** | File upload (PDF or Word, 1 file) | [req] | Remove your name, acknowledgements, and anything identifying from the text — AND from the file's metadata (Word: File → Info → Inspect Document; PDFs inherit the author field from the source file). Referees see only this file. |
| 3.11 | **Title page** | File upload (PDF or Word, 1 file) | [req] | A separate one-page file: title, all authors with emails and class years, acknowledgements if any. Only the Editor-in-Chief sees it. |
| 3.12 | Data and code availability | Paragraph | [req] | What data does the paper use, and can you share the data and code with the editors if asked? A sentence or two. |

## Section 4 — Perspectives submission (branch B)

| # | Field | Type | Req | Help text |
|---|---|---|---|---|
| 4.1 | Title | Short answer | [req] | — |
| 4.2 | Your thesis in one sentence | Short answer | [req] | The single claim the piece argues. |
| 4.3 | The piece | Paragraph | [req] | Paste the full text (600–1,200 words). If you'd rather upload a file, use the next question and write "attached" here. |
| 4.4 | File upload | File upload (PDF or Word, 1 file) | *[opt]* | Only if you didn't paste above. |
| 4.5 | Sources | Paragraph | [req] | Links or citations for the factual claims in the piece. |

## Section 5 — Attestations & consent (both branches converge here)

| # | Field | Type | Req | Help text |
|---|---|---|---|---|
| 5.1 | AI-use disclosure | Checkboxes: "I used no AI tools" / "I used AI tools (describe below)" | [req] | Candid disclosure of how AI tools figured in the research or writing, if at all. |
| 5.2 | AI-use description | Paragraph | *[opt]* | If you checked the second box: what tools, for what. |
| 5.3 | Originality & exclusivity | Checkbox (single, must check): "This is my own work and it is not under consideration at another publication while the Review reviews it." | [req] | — |
| 5.4 | Publication consent | Checkbox (single, must check): "If accepted, I consent to publication on the Review's website and to deposit of the version of record in W&M ScholarWorks." | [req] | ScholarWorks is the university library's permanent open-access repository. |
| 5.5 | **Would you be willing to serve as a reviewer?** | Multiple choice: Yes / Maybe — tell me more / No | [req] | Reviewers read at most two papers a cycle, about 2–3 hours each, with training provided. Authors often make the best referees. |
| 5.6 | Anything else? | Paragraph | *[opt]* | Anything the editors should know. |

## Confirmation message

> Thank you — your submission is in. Research submitted by the semester
> deadline is anonymized, read by two referees, and decided by the dates on
> the website (fall: decisions by 20 November 2026; spring: decisions by
> 12 March 2027). Perspectives are read by the editors, typically within a
> few weeks. Either way you will receive written feedback with the
> decision, at your W&M email.

---

## Mechanics to configure (and their consequences)

- **File uploads require respondents to be signed into a Google account.**
  This is a Google Forms limitation. Consequence for research co-authors
  at other institutions: only the *submitting* W&M author needs to touch
  the form, so uploads should be fine — but a non-W&M co-author cannot
  submit on the team's behalf unless they have some Google account.
  Mention "submitting author must be a W&M student" in the form header.
- **Branching:** use "Go to section based on answer" on Q2.1, and end
  Section 3 with "Go to Section 5" (skipping 4) — otherwise branch A
  respondents fall through into the Perspectives section.
- **Responses → Google Sheet.** Link a response Sheet; it doubles as the
  review tracker (add columns for paper ID, referees, status, decision
  date). Assign internal IDs in the Sheet, never in the form — IDs are
  internal only.
- **Google Forms cannot auto-close on a date.** The 16 October close for
  the fall research cycle is manual: after the deadline, either close the
  form briefly and reopen it, or (better) leave it open — Perspectives are
  rolling anyway — and treat late research submissions as spring-cycle.
  Put "Research received after 16 October 2026 rolls to the spring
  cycle" in the Section 3 description so nobody is surprised.
- Set "Collect email addresses" to verified, and enable response receipts
  — the receipt doubles as the author's proof of the submission date.
