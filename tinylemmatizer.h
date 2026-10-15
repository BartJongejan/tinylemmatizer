// tinylemmatizer.h : Include file for standard system include files,
// or project specific include files.

#ifndef TINYLEMMATIZER_H
#define TINYLEMMATIZER_H

// A loaded flexrules rule set. Read-only once created, so one rule set can be
// used from several threads at the same time.
typedef struct tlRules tlRules;

// Create a rule set from the full contents of a flexrules file.
// Returns 0 if the data is too short or memory runs out.
extern tlRules* tlNewRules(const char* data, long size);
// Read a rule set from a flexrules file.
// Returns 0 on success, 1 if the file cannot be opened, 2 if reading fails.
extern int tlReadRules(const char* filename, tlRules** out);
extern void tlFreeRules(tlRules* rules);
// Lemmatize a word. Returns a 0-terminated array of lemmas, or 0 if there are
// none. Free the result with tlFreeLemmas.
extern char** tlLemmas(const tlRules* rules, const char* word);
extern void tlFreeLemmas(char** lemmas);

// Old single-instance API, using one global rule set.
extern void startProc(const char* flexrulesFileName, int* err);
extern void stringEval(const char* s, const char** out, int* err);
extern void endProc(void);

#endif
