- Description of the .properties format: <https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html#load-java.io.Reader->

- Behaviours in corner cases, based on handling by OpenJDK 1.8:

    - Comment after a line continuation
        - The comment's comment-ness is ignored.  This applies even if the
          first line is blank/all-whitespace.
    - Blank line after a line continuation
        - The blank line is not ignored.
    - Whitespace at the start of a line after a line continuation
        - Whitespace is discarded
    - Line with a line continuation that's otherwise all whitespace
        - The whitespace is discarded, and the line continuation is processed
          normally.  If the line is still all-whitespace after processing the
          line continuations, the line is discarded.
    - EOF after line continuation
        - The line continuation is discarded & ignored ?  (What if there's no
          final newline?)
    - Multiple occurrences of the same key
        - Only the last occurrence is used
    - First character in a line is a colon or =
        - Empty key
    - First nonblank character in a line is a colon or =
        - Empty key
    - Writing a comment containing a backslash followed by a non-Latin-1
      character
        - The comment will contain `\\uXXXX` (i.e., two literal backslashes)
    - Writing a comment containing a character in the 0x80-0x9F range
        - The character is written as-is, not escaped

- Terminating newlines are discarded, but not other trailing whitespace.
