# Judge report — branch `rehearsal-pr` vs `main`

- **Verdict: SHIP-READY for this branch** — both Done-when items are met; recommend merge.
- Repository: https://git.pit.local/pit-crew.git
- Branch HEAD: `dbf7422` (docs: tie the Switch section to the actual run)
- Base `main`: `f11fa02` (the merge base)
- Clean room: `clean-room-202611050036` (`git clone --filter=blob:none --branch rehearsal-pr`, then `fetch ... main`)
- Diff: `git diff FETCH_HEAD...HEAD` — 2 commits, 3 files, +19 / -73
- Kit: `pit-crew-kit` pulled before the review; `judge-kit/check.py --mode hygiene --changed-since FETCH_HEAD`
- Date: 2026-11-05 00:37 UTC

> Note: the server ignored `--filter=blob:none` ("filtering not recognized by server, ignoring"); the clone and the merge-base fetch still worked.

## Done-when items

| # | Item | Answer | Evidence |
|---|---|---|---|
| 1 | `evidence/judge-kit-self-check.json` is removed and nothing still links to it | **MET** | The file is deleted in `f026b9b` (69 lines removed). Its row is removed from `evidence/README.md`, and the README's Evidence paragraph no longer mentions "the judge kit's check of this repository". `grep -rn judge-kit-self-check` over the whole tree at `dbf7422` returns no hits; `evidence/` holds only `README.md` and `template-lint.txt`. |
| 2 | The README's Switch section ties the run to real commit hashes | **MET** | New paragraphs under `README.md` "How Switch is used (and why it breaks without it)" cite `42981e9` (the countdown CLI), `e8d5f9f` (the `--version` flag) and `f11fa02` (the reproduce-step clone URL). All three exist in the repository: `git cat-file -t <hash>` returns `commit` for each, with the matching subjects. They read as the run's history, not placeholders. |

## Rubric extras

| Criterion | Answer | Evidence |
|---|---|---|
| Correct | Yes | Both items are fully satisfied; no dangling references to the deleted file. |
| Small | Yes | 2 commits, 3 files, +19/-73; `f026b9b` is the deletion plus its two mentions, `dbf7422` is the 17-line Switch paragraph. |
| Readable | Yes | Two short paragraphs; the existing feature table and all other README text are untouched. |
| In the style of the code around it | Yes | Prose matches the section; commit subjects follow the repo's `docs:` convention. |
| Tested | Yes (docs-only) | `check.py --mode hygiene` passes (secrets, local files, large files on the 2 changed files); the project's `python3 -m unittest discover -s tests` still runs 12 tests OK. No code changed, so no new test is warranted. |
| Nothing unrelated | Yes | The only edits besides the two Done-when changes are the README Evidence wording and the `evidence/README.md` row, both solely about removing the deleted file. |

## Minor nit (non-blocking)

- `README.md` in the Evidence paragraph has one over-long line: `build log go there as the crew produces them. See [evidence/README.md](evidence/README.md) for what each`. Worth wrapping to the file's ~80-column style next time that section is touched, but it does not affect either Done-when item.

## Scope note

This clears the branch, not the repository's overall submission. `main` is still **BLOCKED** for the main verdict until the demo video link replaces `TODO(video-link)`; that is unchanged by this branch.
