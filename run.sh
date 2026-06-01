#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

PROGRAM_FILE="$PROJECT_DIR/verison.py"
INBOX_DIR="$PROJECT_DIR/data/inbox"
OUTBOX_DIR="$PROJECT_DIR/data/outbox"
TESTS_DIR="$PROJECT_DIR/tests"

if command -v uv >/dev/null 2>&1; then
    PYTHON_RUN="uv run python"
    PYTEST_RUN="uv run pytest"
else
    PYTHON="$PROJECT_DIR/.venv/bin/python"

    if [ ! -f "$PYTHON" ]; then
        PYTHON="python3"
    fi

    PYTHON_RUN="$PYTHON"
    PYTEST_RUN="$PYTHON -m pytest"
fi

setup() {
    echo "[LOADING] Установка зависимостей..."

    if command -v uv >/dev/null 2>&1; then
        uv pip install -r "$PROJECT_DIR/requirements.txt"
    else
        "$PYTHON" -m pip install -r "$PROJECT_DIR/requirements.txt"
    fi

    echo "[OK] Зависимости установлены"
}

run_program() {
    echo "[LOADING] Запуск программы..."

    if [ ! -d "$INBOX_DIR" ]; then
        echo "[ERROR] Папка data/inbox не найдена"
        echo "[OK] Создай папку data/inbox и положи туда письма"
        exit 1
    fi

    mkdir -p "$OUTBOX_DIR"

    cd "$PROJECT_DIR"
    $PYTHON_RUN "$PROGRAM_FILE"

    echo "[OK] Программа завершила работу"
}

clean_outbox() {
    echo "[LOADING] Возвращаем письма из data/outbox обратно в data/inbox..."

    mkdir -p "$INBOX_DIR"

    if [ -d "$OUTBOX_DIR" ]; then
        find "$OUTBOX_DIR" -type f | while read file; do
            filename="$(basename "$file")"
            destination="$INBOX_DIR/$filename"

            if [ -e "$destination" ]; then
                name="${filename%.*}"
                ext="${filename##*.}"

                if [ "$name" = "$ext" ]; then
                    destination="$INBOX_DIR/${filename}_restored"
                else
                    destination="$INBOX_DIR/${name}_restored.${ext}"
                fi
            fi

            mv "$file" "$destination"
        done
    fi

    echo "[LOADING] Очищаем папку data/outbox..."

    rm -rf "$OUTBOX_DIR"
    mkdir -p "$OUTBOX_DIR"

    echo "[OK] Письма возвращены в inbox, outbox очищен"
}

run_tests() {
    echo "[LOADING] Запуск тестов..."

    if [ ! -d "$TESTS_DIR" ]; then
        echo "[ERROR] Папка tests пока не создана"
        exit 1
    fi

    cd "$PROJECT_DIR"
    $PYTEST_RUN "$TESTS_DIR" -q

    echo "[OK] Тесты успешно пройдены"
}

case "$1" in
    setup)
        setup
        ;;
    run)
        run_program
        ;;
    clean)
        clean_outbox
        ;;
    test)
        run_tests
        ;;
    all)
        clean_outbox
        run_tests
        run_program
        ;;
    *)
        echo "[HELP] Использование:"
        echo "./run.sh setup   - установить зависимости"
        echo "./run.sh run     - запустить программу"
        echo "./run.sh clean   - очистить data/outbox"
        echo "./run.sh test    - запустить тесты"
        echo "./run.sh all     - очистить outbox, запустить тесты и программу"
        exit 1
        ;;
esac