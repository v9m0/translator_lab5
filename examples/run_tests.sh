#!/usr/bin/env bash
# run_tests.sh — прогоняет все примеры через анализатор пятой лабораторной

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
VALID_DIR="${PROJECT_DIR}/examples/valid"
INVALID_DIR="${PROJECT_DIR}/examples/invalid"
TRANSLATOR=(python3 "${PROJECT_DIR}/main.py")

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

passed=0
failed=0
total=0

run_test() {
  local file="$1"
  local expect_success="$2"
  local label
  local stdout_file
  local stderr_file
  local code
  local has_stderr=0

  label="$(basename "$file")"
  stdout_file="$(mktemp)"
  stderr_file="$(mktemp)"

  total=$((total + 1))

  if "${TRANSLATOR[@]}" "$file" >"$stdout_file" 2>"$stderr_file"; then
    code=0
  else
    code=$?
  fi

  if [[ -s "$stderr_file" ]]; then
    has_stderr=1
  fi

  if [[ "$expect_success" -eq 1 ]]; then
    if [[ "$code" -eq 0 && "$has_stderr" -eq 0 ]] && grep -q "Symbol table" "$stdout_file"; then
      echo -e "  ${GREEN}PASS${NC}  valid/${label}"
      passed=$((passed + 1))
    else
      echo -e "  ${RED}FAIL${NC}  valid/${label}  <- ожидался успешный разбор"
      failed=$((failed + 1))
    fi
  else
    if [[ "$has_stderr" -eq 1 ]]; then
      echo -e "  ${GREEN}PASS${NC}  invalid/${label}"
      passed=$((passed + 1))
    else
      echo -e "  ${RED}FAIL${NC}  invalid/${label}  <- ожидалась ошибка"
      failed=$((failed + 1))
    fi
  fi

  rm -f "$stdout_file" "$stderr_file"
}

echo ""
echo "Анализатор: python3 ${PROJECT_DIR}/main.py"
echo "──────────────────────────────────────────"

if [[ -d "$VALID_DIR" ]]; then
  valid_files=("$VALID_DIR"/*.*)
  if [[ "${#valid_files[@]}" -gt 0 && -f "${valid_files[0]}" ]]; then
    echo -e "${YELLOW}Положительные примеры (valid/):${NC}"
    for f in "${valid_files[@]}"; do
      run_test "$f" 1
    done
  fi
fi

echo ""

if [[ -d "$INVALID_DIR" ]]; then
  invalid_files=("$INVALID_DIR"/*.*)
  if [[ "${#invalid_files[@]}" -gt 0 && -f "${invalid_files[0]}" ]]; then
    echo -e "${YELLOW}Негативные примеры (invalid/):${NC}"
    for f in "${invalid_files[@]}"; do
      run_test "$f" 0
    done
  fi
fi

echo ""
echo "──────────────────────────────────────────"
echo -e "Итог: ${GREEN}${passed} прошло${NC} / ${RED}${failed} упало${NC} / ${total} всего"
echo ""

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi
