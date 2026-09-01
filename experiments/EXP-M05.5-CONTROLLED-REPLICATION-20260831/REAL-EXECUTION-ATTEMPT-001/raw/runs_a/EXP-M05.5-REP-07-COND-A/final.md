# Baseline de Refinamento de Ideia — EXP-M05.5-REP-07-COND-A

## Ideia Original
> Uma ferramenta de linha de comando simples que recebe um nome de arquivo e cria uma cópia com timestamp antes de alterações manuais, sem banco de dados, interface gráfica ou sincronização.

## Resumo do Modelo
A command‑line utility that creates a timestamped backup copy of a specified file before the user edits it, offering lightweight, manual versioning without a database, GUI, or synchronization features.

## Versão Refinada
cli‑backup --file <path> [--dest <directory>] [--format <timestamp>] [--keep <n>] [--list] [--restore <timestamp>] [--diff <timestamp>]
- Creates a copy with a configurable timestamp format.
- Optional destination directory for all backups.
- "--keep" limits retained backups, pruning older ones.
- "--list" shows available versions; "--restore" copies a selected version back.
- "--diff" displays a line‑by‑line diff between the current file and a chosen backup.
- Configuration can be stored in a simple JSON/YAML file for default options.
- Implemented as a single‑file Python/Go script distributable via pip or a binary.

## Pontos Fortes e Fracos
- **Fortes:** Extremely simple to use and understand, Zero runtime dependencies beyond the standard library, Works offline on any OS with a shell, Minimal footprint – no database or background services, Provides an immediate safety net before manual edits
- **Fracos:** User must remember to run the command before each edit, No automatic detection of file changes, Cannot list, compare, or restore previous versions without additional commands, No built‑in conflict or concurrency handling, Lacks encryption or secure storage options

## Próximos Passos
Define the exact command‑line syntax and help output, Implement core copy‑with‑timestamp functionality, Add optional flags (--dest, --format, --keep, --list, --restore, --diff), Write unit and integration tests for each feature, Create a minimal configuration file format and loading logic, Package the tool for distribution (e.g., PyPI, Homebrew), Draft user documentation and usage examples, Gather early user feedback to prioritize further enhancements
