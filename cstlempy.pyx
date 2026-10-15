# cstlempy.pyx - Python Module, this code will be translated to C by Cython.

"""Lemmatizer that uses the same lemmatization rules ('flexrules') as CSTlemma."""

cdef extern from "tinylemmatizer.h":
    ctypedef struct tlRules:
        pass
    tlRules* tlNewRules(const char* data, long size) nogil
    void tlFreeRules(tlRules* rules) nogil
    char** tlLemmas(const tlRules* rules, const char* word) nogil
    void tlFreeLemmas(char** lemmas) nogil


cdef class Lemmatizer:
    """Lemmatizer(path)

    Load the flexrules file at 'path' (a str or os.PathLike).
    Raises OSError if the file cannot be read and ValueError if it is not a
    flexrules file. A Lemmatizer can be shared between threads.
    """
    cdef tlRules* _rules

    def __cinit__(self, path):
        with open(path, 'rb') as f:
            data = f.read()
        # Flexrules files start with the version marker '\rV3\r'
        if len(data) <= 4 or data[:4] != b'\rV3\r':
            raise ValueError(f"{path!r} is not a flexrules file")
        self._rules = tlNewRules(data, len(data))
        if self._rules is NULL:
            raise MemoryError()

    def __dealloc__(self):
        tlFreeRules(self._rules)

    def lemmatize(self, str word):
        """Return the list of lemmas of 'word'. An ambiguous word has more than one lemma."""
        cdef bytes encoded = word.encode('UTF-8')
        cdef const char* w = encoded
        cdef char** lemmas
        with nogil:
            lemmas = tlLemmas(self._rules, w)
        if lemmas is NULL:
            return []
        try:
            result = []
            i = 0
            while lemmas[i] is not NULL:
                result.append(lemmas[i].decode('UTF-8'))
                i += 1
            return result
        finally:
            tlFreeLemmas(lemmas)


# Old API, kept for backward compatibility. It uses one module-wide Lemmatizer.

_lemmatizer = None

# Function to be called once, before the first call to lemmatize()
# Returns 0 on success, 1 if the file cannot be opened, 2 if reading fails.
def init(Str):
    global _lemmatizer
    try:
        _lemmatizer = Lemmatizer(Str)
    except OSError:
        return 1
    except (ValueError, MemoryError):
        return 2
    return 0

# Function to lemmatize a full form
# Returns the lemmas as one string, each lemma followed by a blank.
def lemmatize(Str):
    if _lemmatizer is None:
        raise RuntimeError("call cstlempy.init() before cstlempy.lemmatize()")
    return ''.join(lemma + ' ' for lemma in _lemmatizer.lemmatize(Str))

# Function to be called after the last call to lemmatize()
def final():
    global _lemmatizer
    _lemmatizer = None
