CWD - CURRENT WORKING DIRECTORY

CWD
[FH=file_handle_name]
[TYPE={DATA*|SYNTAX}]
[CD={YES*|NO}]
[MACRO={YES*|NO}]
[/HELP].

Create a FILE HANDLE based on either the data file location or the syntax location.
This makes it easier to restore the old SPSS behavior that allowed the user to work
with relative paths. In newer versions of SPSS, the current working directory is by default
the SPSS installation directory.

TYPE specifies whether the designated syntax or the designated data file should be use to
define the FILE HANDLE.

CD specifies whether the current working directory should be changed to the dir of <TYPE>

MACRO specifies whether a macro !<file_handle_name> of the file location should also be defined.
Such a macro is useful for embedding file paths in e.g. GET DATA connect strings

/HELP prints this help and does nothing else.