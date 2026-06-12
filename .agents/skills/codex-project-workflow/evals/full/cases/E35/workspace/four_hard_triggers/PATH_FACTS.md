# Independent Path Facts

- User action: run `python app.py --self-test`.
- Formal product entry: `app.py`.
- `app.py` imports `normalize_event` from `src.client`.
- `src.client.normalize_event` is the only production normalization path.
- The self-test payload represents the revised external API envelope.
- The implementation must not move normalization into `app.py`, tests, or an auxiliary script.
