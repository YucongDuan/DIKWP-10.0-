# Final Lab Manual

## Run sequence

1. Run `python experiments/run_ccl10z_suite_10_0.py`.
2. Inspect `outputs/final_summary_10_0.json`.
3. Inspect `outputs/null_to_form_to_null_trace_tail_10_0.csv`.
4. Inspect `outputs/semantic_birth_death_events_10_0.csv`.
5. Re-run with modified seeds in `configs/ccl10z_config.json` if needed.

## Evaluation questions

- Did the null start actually begin with zero semantic objects?
- Did proto-semantons appear from field coupling rather than imported labels?
- Did generated semantics return to null?
- Did the static boundary audit pass?
- Did the system preserve Phenomenal Residual?

## Interpretation rule

Do not read high proto-semanton counts as truth. They are field events. Only after semantic collapse, de-falsification and return-to-null can they be interpreted as reversible semantic traces.
