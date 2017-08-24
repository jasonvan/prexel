# Prexel



WINDOWS — %APPDATA%\Sublime Text 3\Packages
LINUX — ~/.config/sublime-text-3/Packages
MAC/OSX — ~/Library/Application Support/Sublime Text 3/Packages

# Execution

Run this small command-line application to test current code

    prexel/plugin/cli.py

## Testing

Currently there is a test suite available to test the code. This can be found at:

    prexel/plugin/tests/

Running the test can be done from the command line, with the following command:

    python3 -m unittest prexel/plugin/tests/test_pretty_print_encoder.py
    python3 -m unittest prexel/plugin/tests/test_source_code_encoder.py 
    python3 -m unittest prexel/plugin/tests/test_lexer.py
    python3 -m unittest prexel/plugin/tests/test_interpreter.py
    python3 -m unittest prexel/plugin/tests/test_regex.py


