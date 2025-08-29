'''
Zadanie #4 — Normalizacja ścieżki POSIX (bez pathlib / os.path)

Funkcja: normalize_posix_path(path: str) -> str

Wymagania (zachowanie w stylu posixpath.normpath, ale bez używania bibliotek do ścieżek):

Obsłuż ścieżki absolutne i względne.

Zredukuj wielokrotne ukośniki // do jednego /.

Usuń segmenty ".".

Rozwiąż "..":

dla ścieżek absolutnych — cofnięcie o segment (nie wychodzimy ponad root /),

dla względnych — cofnięcie o segment, a jeśli nie ma już czego cofnąć, zachowaj nadmiarowe ".." na początku (np. "../../a").

Bez ukośnika na końcu wyniku (chyba że wynik to "/").

Pusty input traktuj jako ".". 
'''


def normalize_posix_path(path: str) -> str:
    """
    Normalize a POSIX-style filesystem path string.

    Rules implemented (mimicking Unix `realpath`/`normpath` behavior):
    - Empty string "" -> current directory ("." by convention).
    - Multiple slashes ("//" or more) are collapsed to a single slash.
    - A single "." segment is ignored (represents current directory).
    - A ".." segment removes the previous segment, unless:
        * the path is relative and there's nothing to remove → then ".." is preserved,
        * the path is absolute and there's nothing to remove → ".." is ignored.
    - A trailing slash is removed, unless the result is just the root "/".
    - Absolute paths always start with "/", relative paths never do.

    Examples:
        ""                -> "."
        "/"               -> "/"
        "a//b/./c/../"    -> "a/b"
        "/a/../../b/../c" -> "/c"
        "../../"          -> "../.."
        "../a/..//b/."    -> "../b"

    Args:
        path (str): Input POSIX-style path string.

    Returns:
        str: Normalized path string according to POSIX rules.
    """
    is_absolute = path.startswith('/')
    if not path: 
        return "."
    
    parts = path.split('/')
    stack = []

    for seg in parts:

        if seg == "" or seg == '.':
            continue
        elif seg == "..":
            if is_absolute:
                if stack:
                    stack.pop()
                else:
                    continue
            else:
                if stack and stack[-1] != "..":
                    stack.pop()
                else:
                    stack.append('..')
        else:
            stack.append(seg)
    if is_absolute:
        if not stack:
            return "/"
        else:
            return "/" + "/".join(stack)
    else:
        if not stack:
            return "."
        else:
            return "/".join(stack)
