- <https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html#load-java.io.Reader->

- Behaviours in corner cases, based on handling by OpenJDK 1.8 (Confirm that
  Oracle Java does the same things!):

    - [comment after a line continuation]
        - The comment's comment-ness is ignored.  This applies even if the
          first line is blank/all-whitespace.
    - [blank line after a line continuation]
        - The blank line is not ignored.
    - [whitespace at the start of a line after a line continuation]
        - discarded
    - [line with a line continuation that's otherwise all whitespace]
        - The whitespace is discarded, and the line continuation is processed
          normally.  If the line is still all-whitespace after processing the
          line continuations, the line is discarded.
    - [EOF after line continuation]
        - The line continuation is discarded & ignored ?  (What if there's no
          final newline?)
    - [multiple occurrences of the same key]
        - Only the last occurrence is used
    - [first character in a line is a colon or =]
        - empty key
    - [first nonblank character in a line is a colon or =]
        - empty key
    - [writing a comment containing a backslash followed by a non-Latin-1
      character]
        - The comment will contain `\\uXXXX` (i.e., two literal backslashes)

- Terminating newlines are discarded, but not other trailing whitespace.

cf. <http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/src/share/classes/java/util/Properties.java>?
