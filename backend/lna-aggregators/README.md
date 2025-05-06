```bash
unzip -l dist/lna_aggregators-0.1.0-py3-none-any.whl | grep '\.dist-info/METADATA$'

unzip -p dist/lna_aggregators-0.1.0-py3-none-any.whl \
  'lna_aggregators-0.1.0.dist-info/METADATA' \
  | grep '^Requires-Dist'
```