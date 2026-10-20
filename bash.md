# Bash: From Command-Line Fundamentals to Advanced Shell Scripting

A detailed, example-driven reference for interactive Bash, file and process management, programmatic shell scripting, automation, debugging, and robust scripting practices.

**Target:** GNU Bash (not generic POSIX `sh`). Examples assume a Unix-like environment with common external utilities installed. Bash 4+ and Bash 4.4+ features are identified when relevant; some macOS systems still ship Bash 3.2 by default.

---

# Part I — Working in the Terminal

## 1. Bash, the Shell, and the Terminal

### 1.1 Distinguish the layers

| Component | Role |
|---|---|
| Terminal emulator | Displays text and forwards keyboard input; e.g. Terminal, iTerm, Windows Terminal |
| Shell | Parses your commands, expands arguments, launches programs, manages jobs |
| Bash | **Bourne Again SHell**, a specific shell with scripting features |
| Kernel / OS | Manages processes, permissions, filesystems, and devices |
| External command | Separate executable such as `python`, `grep`, or `find` |
| Shell builtin | Command implemented inside Bash, such as `cd`, `read`, or `export` |

A Bash command line is **not** interpreted like Python. Parsing, quoting, expansion, and redirection happen before or alongside command execution.

### 1.2 Check which shell you are using

```bash
bash --version
printf '%s\n' "$SHELL"
printf '%s\n' "$BASH_VERSION"
printf '%s\n' "$0"
ps -p $$ -o comm=
```

`$SHELL` normally records the user's login shell preference, not necessarily the currently executing shell. `$BASH_VERSION` is a more specific test of an active Bash session.

### 1.3 Run a command or a script

```bash
printf 'Hello, Bash!\n'
bash script.sh
./script.sh
```

Running `bash script.sh` invokes Bash explicitly and does not require execute permission. Running `./script.sh` requires execute permission and normally uses the interpreter named in the shebang.

### 1.4 Bash vs POSIX shell

Bash supports arrays, `[[ ... ]]`, arithmetic `(( ... ))`, process substitution, associative arrays, and several other constructs that are not portable to `/bin/sh`. Use `#!/usr/bin/env bash` for scripts that intentionally require Bash. `#!/bin/sh` should be reserved for POSIX-compatible scripts.

**Platform note:** macOS `/bin/bash` has historically been Bash 3.2. Associative arrays require Bash 4+, and some `mapfile` features require later versions. Check your runtime instead of assuming the newest Bash.

## 2. Getting Help and Understanding Commands

### 2.1 Discover what a name resolves to

```bash
type cd
type python
type -a grep
command -v python
which python
help read
man find
```

`type` and `command -v` are shell-aware. `which` may be external or shell-defined and can be less reliable for aliases/functions. Use `help` for Bash builtins, `man` for installed manual pages, and `command --help` when the utility supports it.

### 2.2 Command syntax

```text
command [options] [arguments]
```

Example:

```bash
ls -lah /tmp
```

`-l`, `-a`, and `-h` are short options recognized by many `ls` implementations. Their precise availability and formatting can vary by OS.

### 2.3 Aliases vs functions

```bash
alias ll='ls -lah'
type ll
unalias ll
```

Aliases mainly help interactive shells; functions are usually better for reusable logic, arguments, error handling, and scripts.

### 2.4 Shell history and shortcuts

```bash
history
history 10
```

Useful interactive keys:

| Shortcut | Action |
|---|---|
| `Ctrl+C` | Send interrupt to foreground job |
| `Ctrl+D` | End input / signal EOF |
| `Ctrl+Z` | Suspend foreground job (if job control enabled) |
| `Ctrl+A` | Move to beginning of line (Emacs keybindings) |
| `Ctrl+E` | Move to end of line |
| `Ctrl+R` | Reverse-search history |
| `Tab` | Attempt completion |

Shell history can retain secrets typed into commands. Do not paste tokens/passwords directly onto command lines without assessing exposure.

## 3. Paths, Directories, and Files

### 3.1 Navigate

```bash
pwd
ls
ls -la
cd /tmp
cd ..
cd ~
cd -
```

- **Absolute path:** starts at `/`, e.g. `/home/ada/project`.
- **Relative path:** interpreted from the current directory, e.g. `src/train.py`.
- `.` means current directory; `..` means parent; `~` expands to your home directory in applicable shell contexts.
- Hidden names conventionally begin with `.`, but are not encrypted or protected simply by being hidden.

### 3.2 Create and copy

```bash
mkdir project
mkdir -p project/{src,tests,data}
touch project/README.md
cp project/README.md project/README-copy.md
cp -R project/src project/src-backup
mv project/README-copy.md project/NOTES.md
```

`touch` creates an empty file if absent or updates timestamps if present. `cp` and `mv` can overwrite destinations; `-i` asks before overwriting on common implementations.

### 3.3 Delete with caution

```bash
rmdir empty-directory
rm unneeded.txt
rm -i important.txt
```

`rm -r` recursively removes directories and files; `rm -rf` is especially destructive and generally does not offer a reliable undo. Inspect paths before automating deletion.

### 3.4 Inspect file metadata and storage

```bash
file README.md
stat README.md
du -sh .
df -h
ls -lh
```

`stat` option formats differ across GNU/Linux and BSD/macOS. `du` measures disk usage; `df` reports filesystem availability.

### 3.5 Find files

```bash
find . -type f -name '*.py'
find . -type d -name '.venv'
find . -type f -mtime -7
find . -type f -size +10M
find . -type f -name '*.log' -print
```

- `-type f`: regular files.
- `-type d`: directories.
- `-name`: filename glob pattern interpreted by `find`, not the calling shell.
- `-mtime -7`: modified less than seven 24-hour periods ago (with implementation-specific rounding semantics).
- `-size +10M`: bigger than 10 units of 1 MiB on GNU and commonly compatible `find` implementations; check the target OS.

Quote patterns such as `'*.py'` to prevent premature Bash glob expansion.

## 4. Viewing and Transforming Text

### 4.1 Basic file inspection

```bash
cat README.md
less README.md
head -n 10 output.log
tail -n 25 output.log
tail -f output.log
wc -l output.log
wc -w README.md
```

`tail -f` follows an actively written file, useful for inspecting logs. Some variants provide `tail -F` for name-following across rotation; check your platform.

### 4.2 Search and filter

```bash
grep 'ERROR' app.log
grep -n 'ERROR' app.log
grep -i 'warning' app.log
grep -R 'TODO' src/
grep -E 'ERROR|WARNING' app.log
grep -v '^$' data.txt
```

`grep` uses regular expressions by default; `grep -F` searches fixed literal text. A non-match usually produces exit status **1**, which is not necessarily a script failure.

### 4.3 Sorting, uniqueness, field extraction

```bash
sort names.txt
sort -u names.txt
sort -nr scores.txt
uniq sorted-names.txt
cut -d ',' -f 1 results.csv
tr '[:lower:]' '[:upper:]' < names.txt
```

`uniq` only groups **adjacent** duplicates; often use `sort | uniq -c` for frequency counts. `cut -d ','` is not a correct general-purpose CSV parser when fields can contain quoted commas or embedded newlines.

### 4.4 `sed` and `awk`

```bash
sed -n '1,5p' data.txt
sed 's/old/new/g' data.txt
awk '{print $1, $3}' table.txt
awk -F '\t' '{sum += $2} END {print sum}' metrics.tsv
```

`sed` performs stream editing; `awk` is a powerful record/field processing language. `sed -i` flags vary between GNU and BSD versions; avoid assuming a portable in-place edit syntax.

## 5. Command Structure and Exit Status

### 5.1 Commands are processes or shell builtins

```bash
python -m pytest -q
printf 'finished\n'
```

The shell expands words and launches the command. Most external programs are separate processes; builtins execute within the shell.

### 5.2 Exit statuses

```bash
true
printf '%s\n' "$?"
false
printf '%s\n' "$?"
```

By convention, **0 = success**; **nonzero = failure or another program-specific outcome**. `$?` refers to the status of the most recently completed foreground pipeline/command and is immediately overwritten by the next command.

### 5.3 Command chaining

```bash
mkdir -p results && printf 'ready\n'
grep -q 'ERROR' app.log && printf 'found errors\n'
grep -q 'ERROR' app.log || printf 'no match or grep failed\n'
printf 'one\n'; printf 'two\n'
```

| Operator | Behavior |
|---|---|
| `;` | Run next command regardless of previous status |
| `&&` | Run right side if left side succeeds |
| `||` | Run right side if left side fails |
| `|` | Pipe standard output of left command into right command's standard input |
| `&` | Start an asynchronous background job |

`cmd1 && cmd2 || cmd3` is **not** a fully equivalent substitute for an `if/else`: `cmd3` will run if `cmd2` fails even when `cmd1` succeeds.

### 5.4 Use conditions to classify statuses

```bash
if grep -q 'ERROR' app.log; then
    printf 'found errors\n'
else
    status=$?
    if (( status == 1 )); then
        printf 'no errors found\n'
    else
        printf 'grep failed with status %s\n' "$status" >&2
    fi
fi
```

Distinguish a useful negative result from an actual command error.

---

# Part II — Variables, Expansion, and Control Flow

## 6. Variables, Environment, and Scope

### 6.1 Assign variables

```bash
name='Ada'
project_dir="$HOME/projects/model-evaluation"
printf '%s\n' "$name"
printf '%s\n' "${project_dir}"
```

No spaces around the assignment operator. `name = 'Ada'` is parsed as a command named `name` with arguments, not as an assignment.

### 6.2 Shell vs environment variables

```bash
DATASET='train'
export DATASET
export EXPERIMENT='baseline'
printenv EXPERIMENT
unset DATASET
```

An exported variable is inherited by subsequent child processes through their environment. Normal child processes cannot change their parent's environment.

One-command environment override:

```bash
OMP_NUM_THREADS=2 python train.py
```

This passes an environment setting to that command without persisting it in the parent shell's environment (unless already separately set).

### 6.3 Constants and local variables

```bash
readonly ROOT_DIR="$HOME/projects"

show_target() {
    local target="$1"
    printf 'Target: %s\n' "$target"
}

show_target 'dataset-A'
```

`local` is Bash-specific and scopes variables to the function call (including dynamic scope through nested Bash function calls). Avoid collisions with exported environment names.

### 6.4 Important special parameters

| Parameter | Meaning |
|---|---|
| `$0` | Name used to invoke script or shell |
| `$1`, `$2`, ... | Positional parameters |
| `$#` | Number of positional parameters |
| `"$@"` | All positional arguments, preserved as separate words |
| `"$*"` | All positional arguments joined into one word using the first character of `IFS` |
| `$?` | Most recent command/pipeline exit status |
| `$$` | Process ID of invoking shell (can differ from subshell's actual Bash PID) |
| `$BASHPID` | Current Bash process ID, including Bash subshells |
| `$!` | PID of most recent asynchronous job/pipeline as documented by Bash |
| `$_` | Context-dependent last argument / related shell parameter |
| `$-` | Active shell option flags |

```bash
printf 'script=%s, args=%s\n' "$0" "$#"
printf 'arg=<%s>\n' "$@"
```

### 6.5 Script arguments versus options

```bash
bash process.sh input.csv output.csv
```

Inside `process.sh`, `$1` is `input.csv`, `$2` is `output.csv`, and `$#` is `2`.

## 7. Quoting, Expansion, and Word Splitting

This is one of the most important Bash topics. Many subtle bugs come from treating shell strings as if they were automatically one argument.

### 7.1 Three quoting forms

```bash
name='Ada'
printf '%s\n' '$name'
printf '%s\n' "$name"
printf '%s\n' "File: ${name}.txt"
```

| Form | Expansions permitted |
|---|---|
| `'single quotes'` | Almost none; content is literal |
| `"double quotes"` | Parameter, command, arithmetic expansion; generally no word splitting/globbing of their results |
| `unquoted` | Subject to expansion, word splitting, and globbing |

Escapes and special syntaxes such as `$'...\n...'` have their own semantics.

### 7.2 A whitespace bug

```bash
file='model outputs/metrics.csv'
wc -l "$file"
```

`"$file"` passes one pathname. Unquoted `$file` can become multiple arguments and wildcard matches, depending on contents.

### 7.3 Safe arguments with arrays

```bash
files=('input one.csv' 'input two.csv')
printf 'file=%s\n' "${files[@]}"
```

Quoted `"${files[@]}"` expands each array element to one distinct argument. Avoid building commands by concatenating unquoted strings.

### 7.4 Expansion order (conceptual)

Bash expansion stages include:

1. Brace expansion.
2. Tilde expansion, parameter expansion, arithmetic expansion, command substitution, and process substitution (where supported).
3. Word splitting of unquoted expansion results.
4. Filename expansion (globbing).
5. Quote removal.

The precise expansion rules differ by syntactic context (e.g., assignment, `[[ ... ]]`, `case`, arithmetic context). These rules matter more than memorizing one universal list.

### 7.5 Command substitution

```bash
current_dir=$(pwd)
python_version=$(python --version 2>&1)
printf '%s\n' "$current_dir" "$python_version"
```

`$(command)` captures standard output and removes trailing newline characters. It does **not** automatically capture stderr. Prefer `$()` over legacy backticks for readability and nesting.

A failure inside an assignment is not always handled like a standalone failed command when strict-mode options and nested substitutions are involved; test error handling explicitly.

### 7.6 Don't parse structured data by whitespace accidentally

```bash
filename='Quarterly report 2026.csv'
read -r first second <<< "$filename"
printf 'first=%s; remainder=%s\n' "$first" "$second"
```

`read` uses `IFS` splitting. Use safe delimiters or a real parser for paths, CSV/JSON, or arbitrary binary data.

## 8. Globbing, Brace Expansion, and Pattern Matching

### 8.1 Filename globbing

```bash
printf '%s\n' *.py
printf '%s\n' data/*.csv
printf '%s\n' src/test_?.py
```

| Pattern | Matches |
|---|---|
| `*` | Zero or more filename characters (not `/` in ordinary pathname matching) |
| `?` | Exactly one character |
| `[abc]` | One of a, b, c |
| `[0-9]` | One character in the specified range, locale-dependent |
| `**` | Recursive directories only with `globstar` enabled and in supported contexts |

By default, globs generally do not match leading-dot names, and unmatched globs may remain **literal text**.

### 8.2 Nullglob and globstar

```bash
shopt -s nullglob
shopt -s globstar
files=(data/**/*.csv)
printf '%s\n' "${files[@]}"
```

`nullglob` removes unmatched patterns rather than preserving them literally. `globstar` enables recursive `**` patterns (Bash 4+). `shopt` options are shell-state changes; use a subshell when you want the effect limited to one block.

### 8.3 Brace expansion is not filesystem matching

```bash
printf '%s\n' file_{a,b,c}.txt
printf '%s\n' run_{01..05}.log
mkdir -p experiment/{inputs,outputs,logs}
```

Brace expansion generates strings before globbing; the files do not need to exist. Do not assume braces expand values from variables:

```bash
n=5
printf '%s\n' {1..5}
printf '%s\n' {1..$n}
```

The second expression does **not** dynamically generate 1 through `n` as you might expect. Use arithmetic loops for variable bounds.

### 8.4 Extended globbing

```bash
shopt -s extglob
```

Extended patterns include `?(pattern)`, `*(pattern)`, `+(pattern)`, `@(pattern)`, and `!(pattern)` where `pattern` can contain alternatives separated by `|`. Parse-time considerations mean you should enable `extglob` before parsing a script or function definition using those patterns. Use `[[ ... == pattern ]]` for glob-style pattern matching without invoking `grep`.

## 9. Parameter Expansion and String Operations

Parameter expansion often replaces external commands, but its syntax is context-sensitive. Quotes remain important.

### 9.1 Defaults and assignment

| Syntax | Meaning |
|---|---|
| `${x:-fallback}` | Use fallback when x is unset **or empty** |
| `${x-fallback}` | Use fallback only when x is unset |
| `${x:=fallback}` | Assign fallback if unset or empty, then expand |
| `${x=fallback}` | Assign fallback only if unset |
| `${x:?message}` | Error when unset or empty; useful for required inputs |
| `${x?message}` | Error when unset |
| `${x:+alternate}` | Alternate if set and nonempty |
| `${x+alternate}` | Alternate if set, even empty |

```bash
unset LOG_LEVEL
printf '%s\n' "${LOG_LEVEL:-INFO}"
: "${OUTPUT_DIR:?OUTPUT_DIR must be set and nonempty}"
```

The `:` builtin evaluates arguments and returns success; it is often used for validation and parameter side effects.

### 9.2 String length and substring

```bash
value='data-science'
printf '%s\n' "${#value}"
printf '%s\n' "${value:0:4}"
printf '%s\n' "${value:5}"
```

String length depends on locale and character encoding; in a typical UTF-8 locale Bash counts characters rather than raw bytes.

### 9.3 Remove prefix or suffix patterns

```bash
path='reports/2026/metrics.csv'
printf '%s\n' "${path#*/}"
printf '%s\n' "${path##*/}"
printf '%s\n' "${path%.*}"
printf '%s\n' "${path%%/*}"
```

| Operator | Removes |
|---|---|
| `#` | Shortest matching prefix |
| `##` | Longest matching prefix |
| `%` | Shortest matching suffix |
| `%%` | Longest matching suffix |

These use **shell patterns**, not regular expressions.

### 9.4 Replace and change case

```bash
text='alpha-beta-beta'
printf '%s\n' "${text/beta/gamma}"
printf '%s\n' "${text//beta/gamma}"
printf '%s\n' "${text/#alpha/start}"
printf '%s\n' "${text/%beta/end}"
```

Case conversion (Bash 4+):

```bash
name='ExperimentA'
printf '%s\n' "${name,,}"
printf '%s\n' "${name^^}"
```

### 9.5 Variables whose names are stored in variables

```bash
variable_name='HOME'
printf '%s\n' "${!variable_name}"
```

`${!variable_name}` is **indirect expansion**. It can be useful but increases complexity; prefer associative arrays when mapping dynamic keys to values. Avoid indirect expansion of untrusted input.

## 10. Arithmetic and Numerical Expressions

### 10.1 Arithmetic expansion

```bash
x=12
y=5
printf '%s\n' "$((x + y))"
printf '%s\n' "$((x * y))"
printf '%s\n' "$((x / y))"
printf '%s\n' "$((x % y))"
```

Bash arithmetic is primarily **integer arithmetic**. `12 / 5` yields `2`, not `2.4`. Use tools such as Python or `awk` for floating-point work.

### 10.2 Arithmetic commands

```bash
count=0
((count += 1))
((count > 0))
```

Important: `(( expression ))` returns shell status **0 if the numerical result is nonzero**, and **1 if the result is zero**. That can interact surprisingly with `set -e`:

```bash
count=0
((++count))
```

This increments to 1, so the arithmetic command succeeds. In contrast, starting at zero, `((count++))` evaluates to the **old value** 0 and returns status 1 despite incrementing the variable.

### 10.3 Numeric comparison

```bash
if (( x >= 10 && y < 6 )); then
    printf 'condition matched\n'
fi
```

`(( ... ))` is usually clearer than `-gt`, `-lt`, and other test operators for integer expressions.

## 11. Tests, Conditions, and Regular Expressions

### 11.1 `[[ ... ]]`, `[ ... ]`, and `(( ... ))`

| Construct | Use |
|---|---|
| `[[ ... ]]` | Bash conditional: strings, glob matches, regex, file tests |
| `[ ... ]` | Portable `test`-style condition (mind quoting) |
| `(( ... ))` | Arithmetic tests and updates |

```bash
filename='metrics.csv'
if [[ $filename == *.csv ]]; then
    printf 'CSV name\n'
fi
```

On the right of `==` in `[[ ... ]]`, an **unquoted** pattern is treated as a shell pattern; quoting it means a literal string comparison.

### 11.2 Common file tests

| Expression | Tests |
|---|---|
| `-e path` | Path exists |
| `-f path` | Regular file |
| `-d path` | Directory |
| `-s path` | File exists and has positive size |
| `-r path` | Readable |
| `-w path` | Writable |
| `-x path` | Executable/searchable |
| `-L path` | Symbolic link |
| `file1 -nt file2` | `file1` is newer than `file2` |
| `file1 -ot file2` | `file1` is older than `file2` |

```bash
input='data/train.csv'
if [[ -f $input && -r $input ]]; then
    printf 'input is readable\n'
fi
```

`-e` follows symbolic links; for a dangling symlink, `-L` can still be true even when `-e` is false.

### 11.3 String conditions

```bash
value='ready'
[[ -n $value ]]
[[ -z $value ]]
[[ $value == ready ]]
[[ $value != failed ]]
```

Use `-n` for nonempty, `-z` for empty. Lexical `<`/`>` comparisons in `[[ ... ]]` are locale-sensitive and distinct from numeric comparisons.

### 11.4 Bash regular expressions

```bash
filename='report_2026.csv'
if [[ $filename =~ ^report_([0-9]{4})\.csv$ ]]; then
    printf 'year=%s\n' "${BASH_REMATCH[1]}"
fi
```

The `=~` operator uses an extended regular expression, **not** a glob. `BASH_REMATCH[0]` is the full match and later elements contain captured groups. Quoting the whole regex on the right can make it literal; storing it in a variable is often clearer:

```bash
pattern='^run_[0-9]+$'
[[ run_125 =~ $pattern ]]
```

## 12. Loops and Case Statements

### 12.1 `for` loops

```bash
for model in linear forest svm; do
    printf '%s\n' "$model"
done

for ((i = 0; i < 5; i++)); do
    printf 'iteration=%d\n' "$i"
done
```

### 12.2 Loop over files safely

```bash
for file in data/*.csv; do
    [[ -e $file ]] || continue
    printf 'processing %s\n' "$file"
done
```

The existence guard handles the default unmatched-glob behavior. Alternatively enable `nullglob` where appropriate.

### 12.3 `while` and `until`

```bash
count=1
while (( count <= 3 )); do
    printf '%d\n' "$count"
    ((++count))
done

count=0
until (( count >= 3 )); do
    ((++count))
done
```

`until` repeats while a condition is **false**.

### 12.4 `case` statements

```bash
mode='train'
case "$mode" in
    train)
        printf 'training\n'
        ;;
    evaluate|test)
        printf 'evaluation\n'
        ;;
    *)
        printf 'unknown mode\n' >&2
        ;;
esac
```

`case` patterns use shell pattern matching, not extended regular expressions. `break` exits a loop; `continue` skips to the next iteration.

## 13. Functions, Arguments, and Return Values

### 13.1 Define and call functions

```bash
format_name() {
    local first="$1"
    local last="$2"
    printf '%s %s\n' "$first" "$last"
}

format_name 'Ada' 'Lovelace'
```

Function arguments are available through `$1`, `$2`, `"$@"`, and `$#` within the function.

### 13.2 Return status vs output

```bash
is_csv() {
    [[ $1 == *.csv ]]
}

if is_csv 'records.csv'; then
    printf 'recognized CSV filename\n'
fi
```

`return` sets an **integer exit status** (typically 0–255 after shell normalization), not an arbitrary value like Python's `return`.

To return textual data, write it to stdout and capture it:

```bash
basename_without_extension() {
    local filename="${1##*/}"
    printf '%s\n' "${filename%.*}"
}

stem=$(basename_without_extension '/tmp/data.csv')
```

Capture stdout only if it represents the intended result; diagnostic messages should go to stderr.

### 13.3 Source reusable functions

```bash
source ./helpers.sh
. ./helpers.sh
```

`source` executes the file **in the current shell**, sharing variables/functions and potentially affecting shell options. Do not source untrusted files. Executing `bash helpers.sh` instead starts a separate Bash process.

### 13.4 Exit from a script

```bash
fail() {
    printf 'error: %s\n' "$1" >&2
    exit 1
}
```

Use `return` to return from a function and `exit` to stop the running shell/script process. A sourced script that invokes `exit` can terminate the caller's shell.

## 14. Indexed and Associative Arrays

### 14.1 Indexed arrays

```bash
models=('linear regression' random_forest xgboost)
printf '%s\n' "${models[0]}"
printf '%s\n' "${models[@]}"
printf 'count=%d\n' "${#models[@]}"
models+=('gradient boosting')
```

| Syntax | Meaning |
|---|---|
| `arr=(a b c)` | Create indexed array |
| `${arr[0]}` | Element zero |
| `"${arr[@]}"` | Expand all elements as distinct words |
| `${#arr[@]}` | Count assigned elements |
| `${!arr[@]}` | List indices |
| `arr+=(value)` | Append |
| `unset 'arr[1]'` | Remove index 1, leaving a potentially sparse array |

Avoid `"${arr[*]}"` when you need one argument per element: quoted `[*]` joins into one word.

### 14.2 Associative arrays (Bash 4+)

```bash
declare -A scores=([linear]=0.81 [forest]=0.88 [svm]=0.84)
printf '%s\n' "${scores[forest]}"
printf 'model=%s\n' "${!scores[@]}"
printf 'score=%s\n' "${scores[@]}"
```

Keys are strings; iteration order is not guaranteed. Do not depend on positional ordering of associative-array entries.

### 14.3 Populate arrays from lines

```bash
mapfile -t rows < metrics.txt
printf '%s\n' "${rows[@]}"
```

`mapfile` / `readarray` are Bash builtins (Bash 4+). `-t` strips record-delimiting newlines. A file with embedded newline-containing logical fields needs a different record representation.

### 14.4 Safe argument forwarding

```bash
run_tests() {
    python -m pytest "$@"
}

run_tests -q 'tests/test metrics.py'
```

Always prefer `"$@"` for passing arguments through wrapper functions without losing argument boundaries.

## 15. Reading Input and Processing Files Safely

### 15.1 Read a value interactively

```bash
read -r -p 'Project name: ' project
printf 'Project: %s\n' "$project"
```

`-r` prevents backslash interpretation. `read -s` suppresses terminal echo for secrets, but process execution and storage still require appropriate handling.

### 15.2 Read a file line by line

```bash
while IFS= read -r line || [[ -n $line ]]; do
    printf 'line=<%s>\n' "$line"
done < input.txt
```

The `IFS=` plus `-r` pattern avoids trimming leading/trailing whitespace and interpreting backslashes. The final check handles an unterminated last line.

### 15.3 Read whitespace-delimited fields

```bash
while read -r user score; do
    printf 'user=%s score=%s\n' "$user" "$score"
done < simple-records.txt
```

This is suitable only for input that actually follows the assumed field rules, **not** general CSV/TSV with quoting/escaping requirements.

### 15.4 Process filenames safely with NUL separators

```bash
find data -type f -name '*.csv' -print0 |
while IFS= read -r -d '' file; do
    printf 'file=%s\n' "$file"
done
```

NUL bytes cannot appear inside Unix filenames, so NUL-delimited streams avoid ambiguity from spaces, tabs, and newlines. In Bash, the right side of a pipeline often executes in a subshell; variables changed in the loop usually do not persist in the parent shell.

### 15.5 Preserve state with process substitution

```bash
count=0
while IFS= read -r -d '' file; do
    ((++count))
done < <(find data -type f -print0)
printf 'count=%d\n' "$count"
```

With the redirection `< <(...)`, the `while` loop runs in the current shell rather than a pipeline subshell, so `count` persists. Process substitution has different error-propagation characteristics from a normal pipeline; failures in the producer may need explicit handling.

### 15.6 Batch file processing with `find -exec`

```bash
find data -type f -name '*.tmp' -exec rm -i -- {} +
```

`-exec ... {} +` batches pathnames safely as arguments, avoiding fragile textual parsing. Verify matched paths with `find ... -print` before destructive operations. Some utility option conventions vary across systems.

---

# Part III — Input/Output and Processes

## 16. Redirection, Pipelines, and File Descriptors

### 16.1 Standard streams

| Descriptor | Name | Default |
|---|---|---|
| `0` | stdin | Keyboard or inherited input |
| `1` | stdout | Terminal output |
| `2` | stderr | Terminal diagnostics |

### 16.2 Redirect output and input

```bash
printf 'first\n' > report.txt
printf 'second\n' >> report.txt
cat < report.txt
python train.py > training.log
python train.py 2> errors.log
python train.py > all.log 2>&1
```

`>` truncates or creates the destination; `>>` appends. `2>&1` duplicates the **current** destination of stdout into stderr.

### 16.3 Redirection order matters

```bash
python train.py > all.log 2>&1
python train.py 2>&1 > only-stdout.log
```

In the first command, both streams go to the file. In the second, stderr inherits the original stdout (normally terminal) before stdout is redirected to the file.

Bash shortcut:

```bash
python train.py &> all.log
python train.py &>> all.log
```

`&>` and `&>>` are Bash conveniences, not POSIX `sh` syntax.

### 16.4 Pipes

```bash
grep 'ERROR' app.log | sort | uniq -c
find . -type f -name '*.py' | wc -l
```

A pipe connects stdout from one command to stdin of the next. The second example counts newline-delimited output, which is not reliable for filenames containing newlines; choose NUL-aware processing for arbitrary pathnames.

### 16.5 `tee`

```bash
python -m pytest -q 2>&1 | tee test.log
printf 'completed\n' | tee -a events.log
```

`tee` writes to a file and simultaneously forwards to stdout. With a pipeline, the visible pipeline status is normally the last command's status unless `pipefail` is enabled.

### 16.6 Pipefail and pipeline statuses

```bash
set -o pipefail
false | cat
printf 'status=%d\n' "$?"
```

With `pipefail`, the pipeline status is that of the **rightmost nonzero** command, or 0 if all succeed. Without it, Bash normally uses the status of the last command.

Immediately after a pipeline, read individual statuses:

```bash
false | true
statuses=("${PIPESTATUS[@]}")
printf 'individual=%s\n' "${statuses[@]}"
```

Reading `$?` or doing another command can overwrite `PIPESTATUS`, so capture it right away.

### 16.7 Here-documents and here-strings

```bash
cat <<'EOF_MESSAGE'
Hello $USER
This content is not expanded by Bash.
EOF_MESSAGE

cat <<< 'single line input'
```

Unquoted delimiters allow several shell expansions within a here-document; quoted delimiters suppress them. `<<<` feeds a string plus a newline to stdin (Bash extension).

### 16.8 Extra file descriptors

```bash
exec 3> output.txt
printf 'written using descriptor 3\n' >&3
exec 3>&-
```

`exec` with redirections but no command modifies the current shell's descriptors. Close custom descriptors when finished.

## 17. Subshells, Grouping, and Process Substitution

### 17.1 `( ... )` vs `{ ...; }`

```bash
value='outside'
(value='inside'; printf '%s\n' "$value")
printf '%s\n' "$value"

{ value='changed'; printf '%s\n' "$value"; }
printf '%s\n' "$value"
```

- `( ... )` runs commands in a **subshell environment**, isolating variable and directory changes.
- `{ ...; }` groups commands in the **current shell**. The spaces around braces and command terminator before `}` matter.

### 17.2 Group redirections

```bash
{
    printf 'title\n'
    printf 'result\n'
} > report.txt
```

Redirect the whole group without repeating `> file` for each command.

### 17.3 Process substitution

```bash
diff <(sort before.txt) <(sort after.txt)
```

`<(...)` provides a filename-like path for a command's output. `>(...)` provides a filename-like destination that feeds another command. Process substitution depends on OS support such as FIFOs or `/dev/fd` and is not POSIX `sh`.

Example writing a copy of logs through a program:

```bash
printf 'message\n' | tee >(sed 's/message/event/' > transformed.log) > original.log
```

Because process substitutions run asynchronously, downstream completion and errors require deliberate synchronization if their result is critical.

### 17.4 Pipeline subshell pitfall

```bash
count=0
printf '%s\n' a b c | while IFS= read -r line; do
    ((++count))
done
printf 'count=%d\n' "$count"
```

On typical Bash settings, `count` still prints `0` after the pipeline. Use input redirection or process substitution if loop-side state needs to persist. Bash's `lastpipe` option can modify certain cases, so don't rely on one platform's incidental behavior.

## 18. Processes, Jobs, Signals, and Traps

### 18.1 View processes

```bash
ps aux
top
jobs -l
pgrep -fl python
```

`pgrep`, `top`, and `ps` formats/options are platform dependent. `jobs` concerns processes known to the current shell's job table.

### 18.2 Run in background and wait

```bash
sleep 3 &
pid=$!
printf 'pid=%s\n' "$pid"
wait "$pid"
```

Use `wait` to retrieve child-job completion status. Job-control operations such as `fg`, `bg`, and `%1` are primarily for interactive sessions with job control enabled.

### 18.3 Signals

```bash
kill -TERM "$pid"
```

Signals communicate with a process; `TERM` requests termination and can be handled, while `KILL` cannot be caught or ignored. Do not target unknown PIDs, broad process groups, or production processes without verification.

### 18.4 Cleanup with traps

```bash
tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT
printf 'temporary content\n' > "$tmpdir/work.txt"
```

`EXIT` traps normally run when the shell exits; they do not cover uncatchable termination (e.g. `SIGKILL`). Validate any path used in `rm -rf`; here it comes from a successful `mktemp -d` allocation.

### 18.5 Capture interrupts

```bash
on_interrupt() {
    printf 'interrupted\n' >&2
    exit 130
}

trap on_interrupt INT
```

`SIGINT` usually corresponds to Ctrl+C in an interactive foreground process group. Exit status 130 is a conventional representation of interruption by signal 2.

## 19. Writing Executable Scripts

### 19.1 A minimal script

Save as `greet.sh`:

```bash
#!/usr/bin/env bash

name="${1:-world}"
printf 'Hello, %s!\n' "$name"
```

Run with:

```bash
chmod +x greet.sh
./greet.sh Ada
```

The shebang must be the first line for direct execution. `/usr/bin/env bash` finds Bash via `PATH`; a fixed interpreter path can be more appropriate in controlled environments.

### 19.2 A well-structured script

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

usage() {
    printf 'Usage: %s INPUT OUTPUT\n' "$0" >&2
}

main() {
    if (( $# != 2 )); then
        usage
        return 2
    fi

    local input="$1"
    local output="$2"

    if [[ ! -f $input ]]; then
        printf 'Missing input: %s\n' "$input" >&2
        return 1
    fi

    cp -- "$input" "$output"
    printf 'Wrote %s\n' "$output"
}

main "$@"
```

`cp --` is common on GNU/BSD systems but not universal on all Unix-like platforms. `main "$@"` keeps top-level orchestration clear; the `return` statements express command status.

### 19.3 Determine script directory

```bash
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
printf '%s\n' "$script_dir"
```

This resolves the directory of the currently running/sourced file under typical circumstances, though symbolic links, paths with newline characters, and portability constraints complicate fully general resolution.

## 20. Error Handling, Strict Mode, and Debugging

### 20.1 Strict-mode options

```bash
set -Eeuo pipefail
```

| Setting | What it does | Caution |
|---|---|---|
| `-e` / `errexit` | Exit on certain unhandled nonzero statuses | Has exemptions in conditions, `&&`, `||`, and other contexts |
| `-u` / `nounset` | Error on many unset-variable expansions | Use `${x:-}` for optional values |
| `-o pipefail` | Surface failures from pipeline components | Some pipelines intentionally terminate producers early |
| `-E` / `errtrace` | Inherit `ERR` traps in functions, substitutions, and subshells | `ERR` follows much of `errexit`'s conditional behavior |

**Strict mode is a helpful discipline, not a formal guarantee of correctness.** In particular, `set -e` is not equivalent to exception handling in a programming language.

### 20.2 Handle expected failures explicitly

```bash
if grep -q 'ERROR' app.log; then
    printf 'error text present\n'
else
    status=$?
    if (( status == 1 )); then
        printf 'not found\n'
    else
        exit "$status"
    fi
fi
```

### 20.3 Validate assumptions early

```bash
: "${INPUT_PATH:?INPUT_PATH is required}"
[[ -f $INPUT_PATH ]] || { printf 'Not a file: %s\n' "$INPUT_PATH" >&2; exit 1; }
command -v python >/dev/null 2>&1 || { printf 'Python is required\n' >&2; exit 1; }
```

### 20.4 Debugging modes

```bash
bash -n script.sh
bash -x script.sh
bash -v script.sh
```

| Flag | Meaning |
|---|---|
| `-n` | Parse/check syntax without executing commands (not proof of runtime correctness) |
| `-x` | Trace commands after expansions |
| `-v` | Print shell input lines as read |

You can enable and disable tracing inside a script:

```bash
set -x
printf 'debug section\n'
set +x
```

Traces can expose credentials and sensitive data. Never enable indiscriminately in production logs.

### 20.5 Line-numbered failure reporting

```bash
trap 'printf "failure at line %s: status %s\n" "$LINENO" "$?" >&2' ERR
```

For complex failure reporting, capture the status as the first action of the trap and carefully test behavior around functions, subshells, and conditionals. Logging `$LINENO` inside a trap has context-specific semantics; it may identify the trap site rather than the exact origin in nested cases.

### 20.6 External quality tools

- **ShellCheck:** static analyzer for quoting, expansion, and scripting pitfalls.
- **shfmt:** formatter for shell scripts.
- **Bats-core:** a testing framework for Bash scripts.

```bash
shellcheck script.sh
shfmt -d script.sh
bats tests/
```

These tools require installation and are not Bash builtins.

## 21. Command-Line Argument Parsing

### 21.1 `getopts` for short flags

```bash
#!/usr/bin/env bash

set -euo pipefail

verbose=false
output='result.txt'

while getopts ':vo:' opt; do
    case "$opt" in
        v)
            verbose=true
            ;;
        o)
            output="$OPTARG"
            ;;
        :)
            printf 'Missing argument for -%s\n' "$OPTARG" >&2
            exit 2
            ;;
        \?)
            printf 'Unknown option: -%s\n' "$OPTARG" >&2
            exit 2
            ;;
    esac
done

shift "$((OPTIND - 1))"
printf 'verbose=%s output=%s positional=%s\n' "$verbose" "$output" "$#"
```

Try `bash script.sh -v -o output.csv input.csv`. The leading colon in `':vo:'` requests silent-style error reporting through the `:` and `?` cases. `getopts` natively handles short options, not GNU-style long options.

### 21.2 Manual long-option parser

```bash
input=''
output=''

while (( $# > 0 )); do
    case "$1" in
        --input)
            (( $# >= 2 )) || exit 2
            input="$2"
            shift 2
            ;;
        --output)
            (( $# >= 2 )) || exit 2
            output="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            printf 'Unknown argument: %s\n' "$1" >&2
            exit 2
            ;;
    esac
done

: "${input:?--input is required}"
: "${output:?--output is required}"
```

Real CLI parsers should also define whether `--input=value` is supported, whether option order is flexible, and how extra positional arguments are handled.

## 22. Portable and Secure Shell Practices

### 22.1 Avoid word splitting and command injection

Unsafe approach:

```bash
args='--name example --output report.txt'
python tool.py $args
```

The unquoted expansion is split into words and subject to globbing; it cannot reliably encode arbitrary arguments. A safer approach:

```bash
args=(--name 'example user' --output 'report final.txt')
python tool.py "${args[@]}"
```

Never use `eval` to interpret untrusted input as shell code.

### 22.2 Handle filenames that begin with `-`

```bash
rm -- "$file"
cp -- "$source" "$destination"
```

`--` ends option processing in many Unix utilities, but not all. Alternative: prefix relative paths with `./` where practical.

### 22.3 Don't use `ls` output as input records

Avoid:

```bash
for file in $(ls data); do
    printf '%s\n' "$file"
done
```

Use globs, arrays, `find -exec`, or NUL-delimited streams instead.

### 22.4 Avoid useless parsing and subshells

```bash
for file in data/*.csv; do
    [[ -e $file ]] || continue
    printf '%s\n' "$file"
done
```

This preserves paths with spaces without needing `ls`, `awk`, or `cut`.

### 22.5 Secrets and credentials

- Avoid passing passwords as command-line arguments: process listings or logs may expose them.
- Avoid printing credentials with `set -x` or `env` in logs.
- Prefer credential stores, file descriptors, or managed secret injection where appropriate.
- Review scripts that use `curl`, `ssh`, `sudo`, `eval`, `source`, and destructive filesystem commands.
- Restrict permissions on sensitive files and verify the trust of downloaded scripts before running them.

### 22.6 Permission fundamentals

```bash
ls -l script.sh
chmod u+x script.sh
chmod 600 private.key
umask
```

`r`, `w`, `x` govern permissions for user, group, and others. Directory `x` means traversal/search permission, not “execute the directory.” ACLs, mount options, and platform policies can add nuance.

### 22.7 POSIX/Linux/macOS portability checklist

| Issue | Why it matters |
|---|---|
| Bash 3 vs Bash 4+ | Associative arrays, `mapfile`, and some expansion features |
| GNU vs BSD `sed -i` | Different flags for in-place editing |
| GNU vs BSD `date` | Different date parsing/format flags |
| `readlink -f` | Not universally available |
| `grep -P` | Perl regex support is platform-dependent |
| `stat` flags | OS-specific formats |
| `xargs -r` | Available on GNU; may not exist on BSD/macOS |
| `timeout` | Common on GNU systems, not always installed by default on macOS |
| `flock` | Linux common; may require installation on macOS |

## 23. Advanced Text and Data Pipelines

### 23.1 Count occurrences in logs

```bash
grep -F 'ERROR' app.log | sort | uniq -c | sort -nr
```

This counts identical **matching lines**, not the number of error types unless logs share the same normalized messages.

### 23.2 Extract a field from simple TSV

```bash
awk -F '\t' 'NR > 1 {sum += $3; count++} END {if (count > 0) print sum/count}' metrics.tsv
```

Awk is useful for record-oriented numeric summaries. For data with CSV quoting, escaped delimiters, or complex types, use a real parser such as Python's `csv` module.

### 23.3 Transform with `sed`

```bash
printf '%s\n' 'model=baseline' | sed 's/baseline/production/'
```

Be aware that basic and extended regular-expression modes differ by utility and option (`sed -E` is common on modern GNU/BSD systems).

### 23.4 Combine `find` and `xargs` safely

```bash
find . -type f -name '*.py' -print0 | xargs -0 grep -n 'import pandas'
```

`xargs -0` preserves arbitrary valid Unix filenames. On systems where `xargs` runs the target command even on empty input, this can have undesirable effects. A more portable pathname-safe alternative is:

```bash
find . -type f -name '*.py' -exec grep -n 'import pandas' {} +
```

### 23.5 JSON from command-line tools

```bash
jq -r '.models[] | .name' results.json
```

`jq` is an external JSON processor. Prefer it over grepping JSON when schema-aware extraction is required. Avoid constructing JSON by concatenating raw strings without correct escaping.

### 23.6 `sort` and locale

```bash
LC_ALL=C sort strings.txt
```

Setting the locale can change collation/order, character classes, and case behavior. Set `LC_ALL=C` deliberately when byte-oriented reproducibility is desired; it may not produce human-language sorting.

## 24. Networking, Automation, and Scheduling

### 24.1 Download and inspect URLs

```bash
curl -I https://example.com
curl --fail --location --show-error --silent https://example.com/data.json -o data.json
```

`--fail` treats many HTTP error statuses as failure; it is not a substitute for validating downloaded content. Always assess TLS, authentication, privacy, and rate limits.

### 24.2 SSH and remote execution

```bash
ssh user@example.com
ssh user@example.com 'hostname'
scp report.csv user@example.com:/tmp/
```

`ssh` executes commands remotely; quoting is especially important because a command string may be parsed by both local and remote shells. For reliable production deployment, use carefully designed scripts or argument protocols.

### 24.3 Rsync

```bash
rsync -av --dry-run reports/ backup/reports/
rsync -av reports/ backup/reports/
```

The trailing slash on `reports/` changes what is copied: it means the directory's **contents** in common rsync usage. `--delete` can remove destination files; always preview before using it.

### 24.4 `cron` scheduling

Example crontab expression:

```text
0 7 * * 1-5 /home/ada/scripts/daily_report.sh
```

This generally means 07:00 Monday through Friday in the scheduler's configured timezone. Cron typically uses a minimal environment and its own shell settings; use absolute paths, explicit interpreters, and logging.

### 24.5 Environment and repeatability

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Python virtual environments are separate from Bash; the `activate` script modifies current-shell environment variables and path resolution. For automation you can call `.venv/bin/python` directly without activation.

## 25. Performance, Concurrency, and Advanced Features

### 25.1 Prefer builtins in tight loops when appropriate

```bash
filename='results.csv'
stem="${filename%.csv}"
printf '%s\n' "$stem"
```

Bash parameter expansion avoids spawning `basename`/`sed`/`awk` for trivial string operations. For large datasets, Python/awk or purpose-built utilities typically outperform a Bash loop processing one record at a time.

### 25.2 Run independent commands concurrently

```bash
python train.py --model linear > linear.log 2>&1 &
pid_linear=$!
python train.py --model forest > forest.log 2>&1 &
pid_forest=$!

status_linear=0
status_forest=0
wait "$pid_linear" || status_linear=$?
wait "$pid_forest" || status_forest=$?
printf 'linear=%s forest=%s\n' "$status_linear" "$status_forest"
```

`wait` obtains the actual child statuses. Parallel tasks may compete for CPU, GPU, memory, storage, or external service capacity; more jobs are not always faster.

### 25.3 Bound concurrency

```bash
max_jobs=2
running=0

for dataset in data/*.csv; do
    [[ -e $dataset ]] || continue
    python process.py "$dataset" &
    ((++running))
    if (( running >= max_jobs )); then
        wait -n
        ((running -= 1))
    fi
done

wait
```

`wait -n` is available in Bash 4.3+ and waits for any eligible child job. This is a **teaching sketch**, not a full robust process pool: it does not preserve every background failure status, and uses a count rather than tracking PIDs. For rigorous execution/failure aggregation, consider `xargs -P`, GNU Parallel, Python executors, or a task scheduler.

### 25.4 Named pipes and co-processes

Bash `coproc` supports bidirectional communication with a background command through file descriptors. Named pipes (FIFOs) support IPC between processes. These features are useful for specialized streaming workloads but require careful lifecycle, buffering, and deadlock management.

```bash
mkfifo events.fifo
```

Remove FIFOs when finished, and do not assume reading/writing will proceed without both sides present.

### 25.5 Time operations

```bash
time python -m pytest -q
SECONDS=0
sleep 1
printf 'elapsed=%s\n' "$SECONDS"
```

`SECONDS` is a Bash special variable measuring approximate elapsed seconds from assignment. `time` reports elapsed/user/system resource time; format can vary.

### 25.6 Shell options and execution context

```bash
set -o
shopt
shopt -s nullglob
shopt -u nullglob
```

`set -o` handles shell options such as `pipefail`; `shopt` controls Bash-specific options such as `nullglob`, `globstar`, and `extglob`. Options may propagate to functions, subshells, or child shells differently depending on mode/configuration.

---

# Part IV — Applied Automation and Reference

## 26. Real-World Script Examples

### 26.1 Batch-run Python tests on selected modules

Save as `test_modules.sh`:

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

if (( $# == 0 )); then
    printf 'Usage: %s TEST_PATH [TEST_PATH ...]\n' "$0" >&2
    exit 2
fi

python -m pytest -q "$@"
```

Use:

```bash
bash test_modules.sh tests/unit tests/integration
```

`"$@"` preserves each test-path argument. The script exits with pytest's status, useful in CI.

### 26.2 Process CSV files and collect failures

Save as `process_datasets.sh`:

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

input_dir="${1:-data/input}"
output_dir="${2:-data/output}"

[[ -d $input_dir ]] || { printf 'Missing directory: %s\n' "$input_dir" >&2; exit 2; }
mkdir -p -- "$output_dir"

failed=0
processed=0

for file in "$input_dir"/*.csv; do
    [[ -e $file ]] || continue
    filename="${file##*/}"
    destination="$output_dir/$filename"

    if python transform.py --input "$file" --output "$destination"; then
        ((++processed))
    else
        ((++failed))
        printf 'Failed: %s\n' "$file" >&2
    fi
done

printf 'processed=%d failed=%d\n' "$processed" "$failed"
(( failed == 0 ))
```

Features: accepts optional directories, handles filenames with spaces, deliberately continues on per-file failure, counts outcomes, and returns failure status when any file fails. Assumes `transform.py` exists, handles output conflicts, and has a documented CLI.

### 26.3 Generate a timestamped backup

Save as `backup_project.sh`:

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

source_dir="${1:?Provide source directory}"
backup_dir="${2:?Provide backup directory}"

[[ -d $source_dir ]] || { printf 'Source is not a directory\n' >&2; exit 2; }
mkdir -p -- "$backup_dir"

stamp=$(date '+%Y%m%d_%H%M%S')
archive="$backup_dir/project_$stamp.tar.gz"

tar -czf "$archive" -C "$source_dir" .
printf 'Created %s\n' "$archive"
```

This is a simple local archive, **not** a complete disaster-recovery system. It assumes a stable input tree while the archive is made and does not address retention, encryption, verification, simultaneous runs, or backups stored inside the source.

### 26.4 Run a test suite from a Git repository root

Save as `run_tests.sh` in a repository:

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

python -m pytest -q "$@"
```

This avoids dependence on the directory from which the script is called, as long as it is invoked while inside the intended repository.

### 26.5 Summarize a directory of logs

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

log_dir="${1:-logs}"
[[ -d $log_dir ]] || exit 2

for log in "$log_dir"/*.log; do
    [[ -f $log ]] || continue
    count=$(grep -cF 'ERROR' "$log") || status=$?
    if [[ ${status:-0} -gt 1 ]]; then
        printf 'Could not inspect %s\n' "$log" >&2
        exit "$status"
    fi
    printf '%s: %s\n' "${log##*/}" "$count"
    unset status
done
```

`grep -c` may print `0` while returning status 1 for no matches. This example keeps the count while distinguishing that ordinary outcome from a genuine grep error.

## 27. Reference Tables and Common Pitfalls

### 27.1 Core shell command reference

| Command | Purpose |
|---|---|
| `pwd`, `cd` | Current/change directory |
| `ls`, `find` | List/search filesystem paths |
| `mkdir`, `touch` | Create directories/files |
| `cp`, `mv`, `rm` | Copy/move/remove |
| `cat`, `less`, `head`, `tail` | Inspect file contents |
| `grep`, `sed`, `awk` | Search, edit, and process text |
| `sort`, `uniq`, `cut`, `tr` | Transform fields/lines |
| `wc`, `du`, `df` | Counts and storage usage |
| `chmod`, `umask` | Permissions and defaults |
| `ps`, `pgrep`, `kill`, `jobs`, `wait` | Process/job control |
| `printf`, `read`, `mapfile` | Output and input |
| `export`, `unset`, `readonly`, `local` | Variables and scope |
| `type`, `command -v`, `help`, `man` | Discover/reference commands |
| `set`, `shopt`, `trap` | Shell options and event handling |
| `curl`, `ssh`, `rsync` | Network and file transfer |

### 27.2 Expansion cheat sheet

| Syntax | Meaning |
|---|---|
| `"$x"` | Expand variable as one quoted word |
| `"${arr[@]}"` | Preserve separate array elements |
| `$(cmd)` | Capture stdout of command (trim trailing newlines) |
| `$((a + b))` | Arithmetic value |
| `((a > b))` | Arithmetic test command |
| `${x:-default}` | Default when unset/empty |
| `${x:?message}` | Require set/nonempty value |
| `${#x}` | Length of scalar string |
| `${#arr[@]}` | Array element count |
| `${x#prefix_pattern}` | Remove shortest matching prefix |
| `${x##prefix_pattern}` | Remove longest matching prefix |
| `${x%suffix_pattern}` | Remove shortest matching suffix |
| `${x%%suffix_pattern}` | Remove longest matching suffix |
| `${x/old/new}` | Replace first pattern match |
| `${x//old/new}` | Replace all pattern matches |
| `${x:offset:length}` | Substring |
| `${x,,}` | Lowercase (Bash 4+) |
| `<(cmd)` | Process output as filename-like input |
| `>(cmd)` | Send output to process substitution |

### 27.3 Quote rules: decision guide

| Context | Usually do this | Reason |
|---|---|---|
| Path stored in variable | `"$path"` | Preserve whitespace and wildcard characters |
| Forward function arguments | `"$@"` | Preserve each original argument |
| Pass array to command | `"${arr[@]}"` | Preserve element boundaries |
| Test pattern in `[[ ]]` | `[[ $name == *.csv ]]` | Unquoted RHS is a pattern |
| Test literal string | `[[ $name == 'file*.csv' ]]` | Quoted RHS matches literally |
| Regex in `[[ =~ ]]` | `[[ $value =~ $regex ]]` | Keep regex operators active |
| `find` filename pattern | `-name '*.csv'` | Prevent premature Bash expansion |
| Handle arbitrary filenames | NUL-delimited stream or quoted glob | Newlines defeat ordinary line parsing |

### 27.4 Frequent mistakes

| Mistake | Problem | Prefer |
|---|---|---|
| `var = value` | Not Bash assignment syntax | `var=value` |
| `rm $file` | Word splitting and globbing | `rm -- "$file"` |
| `for f in $(ls ...)` | Breaks unusual filenames | Glob or `find -print0` |
| `cat file | while ...` when updating parent variables | Pipeline loop often in subshell | `while ...; done < file` |
| `((count++))` under `set -e` | Can return status 1 when old value is zero | `((++count))` or assignment |
| Assuming `set -e` catches every failure | Context-dependent exemptions | Explicit checks and tests |
| `echo` for arbitrary data | Options/escape behavior varies | `printf '%s\n' "$value"` |
| `grep | head` with `pipefail` | Producer may exit due to SIGPIPE | Design for expected early termination |
| Treating CSV as comma-split text | Quoted values break parser | Use real CSV parser |
| `source` untrusted script | Executes code in current shell | Only source trusted files |
| `eval` on data | Command injection risk | Arrays and structured parsing |
| Assume Bash works in `/bin/sh` | Bash extensions may fail | Explicit Bash shebang |
| Assume `mapfile` exists on macOS Bash 3.2 | Version mismatch | Check version or use a compatible loop |

### 27.5 Bash or Python?

| Task | A practical choice |
|---|---|
| One-line file discovery, command chaining | Bash |
| Launching existing CLI tools | Bash |
| Setting up developer workflows | Bash |
| General CSV/JSON parsing with types and escaping | Python (or `jq` for JSON) |
| DataFrames/statistics/modeling | Python |
| Complex concurrency/error handling | Python or scheduler |
| Multi-platform business logic | Often Python |
| Tight OS shell integration | Bash |

Use Bash as a **command orchestrator**; use Python when complex data structures, rich parsing, or maintainable application logic are the central requirement.

## 29. Official References

- [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Bash shell expansions](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html)
- [Bash `set` builtin and error behavior](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)
- [Bash arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
- [Bash conditional expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)
- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/)
- [GNU findutils manual](https://www.gnu.org/software/findutils/manual/html_mono/find.html)
- [ShellCheck](https://www.shellcheck.net/)
- [shfmt](https://github.com/mvdan/sh)

**Suggested progression:** Master sections 1–7 (especially quoting), then 9–16, then scripting/error handling in sections 19–22. Use sections 23–26 for practical automation. Review the frequent-mistakes table whenever a command unexpectedly mishandles a pathname or nonzero exit status.
