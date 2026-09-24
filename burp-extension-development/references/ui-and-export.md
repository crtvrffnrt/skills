# UI and request export engineering

Read this reference when building Burp dialogs that edit, transform, or export a selected HTTP message.

## Selection and state

- Use `messageEditorRequestResponse()` for the currently displayed editor and `selectedRequestResponses()` for table selections. Prefer the editor when both exist. Test an empty table, a single row, multiple rows, and an editor whose request differs from an old table selection.
- Request and response editor selections are different contexts. Do not apply response selection offsets to request bytes.
- Montoya selection offsets refer to message byte positions. Swing text selections use character indices; multibyte UTF-8 text needs an explicit conversion. Keep the original bytes until that conversion is complete.
- Snapshot the request and response associated with the user's action. Label a captured response as a snapshot when the dialog permits later request edits. Do not imply that it reflects the edited request.
- Invalidate stale previews and disable Copy/Export immediately when an input changes. Debounce the more expensive regeneration. Revalidate dependent files at the final action.
- Dispose dialogs and owned file pickers on extension unload. Cancel their workers and timers. Clearing a text component is not a promise of secure memory erasure.

## Preserve semantics deliberately

The connection's scheme/host/port and the HTTP Host header can differ. Keep those concepts separate. IPv6 literal destinations need brackets when rendered as URLs.

Parse the header/body boundary without replacing line endings throughout the body. Make encoding support explicit: using a platform-default charset or silently replacing undecodable bytes changes the request. Reject unsupported data with a specific explanation.

Check the receiving tool's limitations before conversion. A tool that stores headers in a map cannot preserve duplicate header lines. A client that recalculates body framing should not receive a stale Content-Length value. Connection-specific headers may nominate additional headers that need special treatment. Compressed, chunked, binary, and unusual HTTP/2 requests require explicit support or a clear rejection.

Decide what counts as a substitution marker using the receiving tool's actual matching behavior. Distinguish repeated occurrences of one marker from multiple independent inputs. If one marker is a prefix of another, check whether replacement order changes the meaning; deterministic aliasing can prevent that ambiguity. Show any alias in the preview rather than silently changing the user's model.

## Commands and filters

Build a list of executable arguments before rendering shell text. Keep flags under program control and quote every user-derived argument for the stated shell. For POSIX shells, close/reopen single quotes around an embedded single quote; double quotes alone do not disable all shell expansion.

Test quotes, dollar signs, backticks, line breaks, backslashes, Unicode, and paths containing spaces. Use an inert executable to capture received arguments and compare them byte-for-byte with the intended vector. This verifies the rendered command without running its target operation.

NUL cannot be represented in a process argument. Large inline bodies can exceed terminal or operating-system argument limits. Define and report the supported size rather than promising arbitrary binary or large-body exports.

Escaping selected response text as a literal regex is different from accepting a regex written by the user. Escape for the receiving regex engine. Java, JavaScript, Python, and Go regex syntax are not interchangeable. Make filter toggles opt-in when filtering changes which results the user sees.

## Filesystem and clipboard UI

For a large local collection, list categories first and index only the chosen subtree. Show relative paths, provide filename search, and offer a direct file chooser. Index names without loading all file contents. Use cancellable background workers, ignore stale worker completions after a category switch, and bound the number of entries retained.

Persist only useful preferences such as a collection root; avoid recording request bodies or generated commands. Handle missing folders, unreadable files, and a busy clipboard visibly. A read-only selectable preview provides a manual copy fallback.

Theme Swing components through Burp and test ordinary window resizing. A GUI test should exercise the real marking, selection, validation, and clipboard controls, not just instantiate a dialog. Synthetic fixtures and an isolated display avoid exposing project traffic during testing.
