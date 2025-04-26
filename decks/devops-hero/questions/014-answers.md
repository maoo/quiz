# Answers to: What pattern does each Bash script line match?

1. Error handling - Line 7
2. String interpolation - Line 12, 14
3. Default parameters - Line 9
4. Command substitution - Line 10
5. Error redirection - Line 17
6. Conditional checks - Line 17-25
7. Exit codes - Line 19, 24
8. Variable assignment - Line 9, 10, 11
9. Command execution - Line 28-35
10. String literals - Line 11

Notes:
- Line 7: set -e is error handling (exit on error)
- Line 9: ENVIRONMENT=${1:-dev} uses default parameter
- Line 10: VERSION=$(git describe --tags --always) uses command substitution
- Line 11: APP_NAME="myservice" is using a string literal for assignment
- Line 12: Uses string interpolation with ${ENVIRONMENT}
- Line 14: Uses string interpolation for the echo command
- Line 17: >/dev/null 2>&1 is error redirection
- Line 17-25: if statements are conditional checks
- Line 19, 24: exit 1 returns exit codes
- Line 28-35: Various command executions