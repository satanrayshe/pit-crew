<!-- room document 'build-log', created by pit-herald at 2026-11-04 23:45:22.236439+00:00; snapshot taken at the end of the rehearsal -->

891e405 fix: judge pull requests from a blobless clone and tighten the crew's rules — updates the judge kit's blobless-clone check and tightens the template, rules and docs.
42981e9 feat: add a deadline countdown CLI — adds pit_clock.py, its stdlib tests, and the README install/run/example section.
e8d5f9f feat: add a --version flag to pit_clock — prints 0.1.0 and exits, with a test and a README note.
f11fa02 docs: clone the judged repository in the reproduce step — the README now clones https://git.pit.local/pit-crew.git, per the judge's fix 2.
f026b9b docs: remove the stale judge-kit self-check evidence — deletes the old self-check JSON, its evidence README row and the main README mention, per the judge's fix 3.
dbf7422 docs: tie the Switch section to the actual run — keeps the feature/primitive table and adds the herald's two paragraphs citing 42981e9, e8d5f9f and f11fa02, with a why-it-breaks-without-Switch paragraph.
