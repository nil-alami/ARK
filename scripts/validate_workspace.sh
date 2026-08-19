#!/usr/bin/env bash
set -euo pipefail

mode="${1:---structure}"
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

required=(
  AGENTS.md WORKFLOW.md STATUS.md SOURCE_MANIFEST.md AGENT-ROSTER.md
  stages/STAGE-CONTRACT.md sources/SHA256SUMS
  sources/normalized/system-design-prompt.md
  sources/normalized/ark-assumptions.md
  templates/stage-output.md templates/adr.md templates/service-contract.md
  templates/component-spec.md templates/execution-flow.md
)

for path in "${required[@]}"; do
  if [[ ! -s "$path" ]]; then
    echo "Missing or empty required file: $path" >&2
    exit 1
  fi
done

stage_count="$(find stages -maxdepth 1 -type f -regextype posix-extended -regex 'stages/[0-9]{2}-.*\.md' | wc -l | tr -d ' ')"
if [[ "$stage_count" != "25" ]]; then
  echo "Expected 25 numbered stage files; found $stage_count" >&2
  exit 1
fi

sha256sum -c sources/SHA256SUMS

if [[ "$mode" == "--final" ]]; then
  final_files=(
    ARK-system-design.md
    ARK-diagrams.md
    ARK-interface-contracts.md
    ARK-execution-flows.md
    ARK-implementation-roadmap.md
    ARK-requirements-traceability.md
    ARK-architecture-decisions.md
    ARK-risks-and-open-questions.md
  )

  for name in "${final_files[@]}"; do
    if [[ ! -s "outputs/final/$name" ]]; then
      echo "Missing or empty final artifact: outputs/final/$name" >&2
      exit 1
    fi
  done

  if rg -n '\| Pending \|' quality/source-instruction-coverage.md >/dev/null; then
    echo "Source-instruction coverage still contains Pending rows" >&2
    exit 1
  fi

  if [[ ! -s quality/source-instruction-atomic-coverage.md ]]; then
    echo "Missing atomic source-instruction coverage register" >&2
    exit 1
  fi

  if rg -n '\| Pending \|' quality/source-instruction-atomic-coverage.md >/dev/null; then
    echo "Atomic source-instruction coverage still contains Pending rows" >&2
    exit 1
  fi

  if rg -n '^- \[ \]' quality/final-acceptance-checklist.md >/dev/null; then
    echo "Final acceptance checklist still contains unchecked items" >&2
    exit 1
  fi

  if [[ ! -s outputs/stages/24-final-assurance.md ]] || ! rg -n '^Status: `COMPLETE`$' outputs/stages/24-final-assurance.md >/dev/null; then
    echo "Stage 24 assurance artifact is missing or not COMPLETE" >&2
    exit 1
  fi

  if ! rg -n '^Workflow state: `COMPLETE`$' STATUS.md >/dev/null; then
    echo "STATUS.md does not record a COMPLETE workflow" >&2
    exit 1
  fi
fi

echo "ARK workspace validation passed ($mode)."
