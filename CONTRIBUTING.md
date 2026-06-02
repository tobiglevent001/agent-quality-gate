# Contributing to Agent Quality Gate

Thanks for your interest! This project aims to standardize **completion verification** in AI agent operations — making sure that when an agent says "done", it actually is.

## How to Contribute

### Reporting Issues

- **Bug reports**: Open an issue describing what happened vs. what should happen
- **Feature requests**: Describe the gap and why it matters
- **Protocol improvements**: If you've encountered a failure mode CADVP doesn't cover, that's valuable

### Pull Requests

1. Fork the repository
2. Create a branch: `git checkout -b feat/your-feature` or `fix/your-bugfix`
3. Make your changes
4. Run the verification script against a target profile to confirm nothing is broken:
   ```bash
   python3 scripts/cadvp-verify.py <your-test-profile>
   ```
5. Commit with a clear message (see commit conventions below)
6. Push and open a PR

### Commit Conventions

We use conventional commits:
- `feat:` — new feature or protocol dimension
- `fix:` — bug fix or correctness improvement
- `docs:` — documentation changes
- `refactor:` — code restructuring without functional change
- `test:` — adding or updating tests
- `ci:` — CI configuration changes

### Adding a New Verification Dimension

If you discover a verification gap (like we did with CC-0):

1. Update `protocol/index.md` — add the dimension with documentation
2. Update `scripts/cadvp-verify.py` — implement the check function
3. Update templates — add the dimension to all three checklists
4. Update `CHANGELOG.md`
5. Run `python3 scripts/cadvp-verify.py` against a target to confirm integration

## Code of Conduct

Be constructive. This is a protocol, not a competition. If you find a gap, document it and help close it.
