# Changelog

## [1.1.0] — 2026-06-03

### Added
- **CADVP v1.1 protocol**: 13-dimension verification framework with CC-0 (Channel Confirmation) as veto-level zero-check
- **Channel decision tree**: Systematic guidance for selecting the correct injection channel (A/B/❌C)
- **Channel availability matrix**: Empirical verification of three injection channels with root cause analysis
- **Inverse verification principle**: Always verify from receiver's read-chain, never from writer's write-chain
- **Channel matching principle**: Do not design processes on channels unavailable at the target end

### Changed
- CADVP expanded from 12 to 13 dimensions (CC-0 + PC×3 + WV×3 + RV×4 + GR×2)
- `cadvp-verify.py` updated with CC-0 channel confirmation check
- All templates updated to include CC-0 checklist entries
- Protocol documentation reorganized with channel confirmation as highest-priority check

### Documentation
- README updated with v1.1 changelog, CC-0 explanation, and related publication section
- Protocol specification (`protocol/index.md`) now includes full channel comparison table
- Hermes SOUL.md integration template updated with CC-0 rules

## [1.0.0] — 2026-06-02

### Added
- **Initial release**: Agent Quality Gate Protocol
- **Three-level completion verification**: L1 Self-Verify → L2 Evidence → L3 Review
- **CADVP v1.0 protocol**: 12-dimension cross-agent delivery verification (PC+WV+RV+GR)
- **Self-verify script**: Automated L1 checklist verification
- **Evidence report generator**: L2 evidence report automation
- **Completion checklist template**: Structured L1-L3 verification workflow
- **Evidence report template**: Standardized delivery evidence format
- **Review assignment template**: L3 reviewer delegation and sign-off
- **Hermes SOUL.md integration**: Ready-to-use SOUL.md snippet for Hermes Agent profiles
- **Basic usage examples**: Three walkthrough examples covering L1, L2, and L3 scenarios
- **MIT License**: Open-source licensing
