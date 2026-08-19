# Stage 24 — Independent final assurance

Governing inputs: all sources, all final outputs, all ADRs, and all quality checklists.

## Work

- Delegate the complete final package to `assurance_reviewer` with no authorship task.
- Review source fidelity, instruction coverage, requirement traceability, internal consistency, implementability, security, reliability, ML correctness, runtime order, diagrams, roadmap, and anti-overengineering.
- Resolve every Critical and High defect by returning to the owning stage, repairing downstream artifacts, and re-running assurance.
- Record Medium/Low accepted risks with owner and rationale.
- Run `scripts/validate_workspace.sh --final`.

Output: `outputs/stages/24-final-assurance.md`.

Gate: no unresolved Critical/High findings, every source-prompt instruction mapped, validation passes, and `STATUS.md` becomes `COMPLETE`.
