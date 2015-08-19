import os.path
import SpssClient, spss 
from extension import Template, Syntax, processcmd

debug = False

__author__ = "Albert-Jan Roskam"
__date__ = "2013-05-31"
__version__ = "1.0.1"


def spssCwd(fh=None, theType=None, cd=None, macro=None):
    """ Get the path name of the designated data file or syntax file """
    
    SpssClient.StartClient()
    path = "."
    try:
        if fh is None:
            fh = "syntaxdir"

        if theType == "syntax" or theType is None:
            if SpssClient.GetDesignatedSyntaxDoc() is not None:
                path = SpssClient.GetDesignatedSyntaxDoc().GetDocumentPath()
        elif theType == "data":
            if SpssClient.GetActiveDataDoc() is not None:
                path = SpssClient.GetActiveDataDoc().GetDocumentPath()
    finally:
        SpssClient.Exit()

    if not path:
        path = os.path.abspath(".")
        print "\nWarning # No path defined. This means that your %s has not been saved yet.\nUsing '%s'\n" % \
              ("syntax file" if theType == "syntax" or theType is None else "data file", path)
    else:
        path = os.path.dirname(path)

    cmds = ["FILE HANDLE %(fh)s /NAME='%(path)s'." % locals()]
    if cd or cd is None:
        cmds.append("CD '%s'." % path)
    if macro or macro is None:
        cmds.append("DEFINE !%s () '%s' !ENDDEFINE." % (fh, path))
    if debug:
        print "\n".join(cmds)
    if path:
        spss.Submit(cmds)

    return path

helptext = r"""CWD
[FH=file_handle_name]
[TYPE={DATA*|SYNTAX}]
[CD={YES*|NO}]
[MACRO={YES*|NO}]
[/HELP].

CWD - CURRENT WORKING DIRECTORY

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

"""

def Run(args):
        """Execute the CWD command"""

        args = args[args.keys()[0]]
        ###print args   #debug
        oobj = Syntax([
                Template("FH", subc="",  ktype="str", var="fh", islist=False),
                Template("TYPE", subc="",  ktype="str", var="theType", islist=False),
                Template("CD", subc="",  ktype="bool", var="cd", islist=False),
                Template("MACRO", subc="",  ktype="bool", var="macro", islist=False),
                Template("HELP", subc="", ktype="bool")])

        # A HELP subcommand overrides all else
        if args.has_key("HELP"):
                print helptext
        else:
                processcmd(oobj, args, spssCwd)
    
