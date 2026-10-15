# launch.py - Python 3 stub loader, loads the 'cstlempy' module that was made by Cython.

# This code is always interpreted, like normal Python.
# It is not compiled to C.

import cstlempy

filename = "flexrules"
print("Create a lemmatizer with the call 'cstlempy.Lemmatizer(\""+filename+"\")'.\n")
try:
    lemmatizer = cstlempy.Lemmatizer(filename)
except OSError as e:
    print("Cannot open '" + filename + "': " + str(e) + "\n")
except ValueError as e:
    print(str(e) + "\n")
else:
    print("Initialization succeeded.\n")
    cstlempyFullForm = "køer"
    print("Going to call lemmatize(<full form>).\n\nThe full form is this one: "+cstlempyFullForm)
    answer = lemmatizer.lemmatize(cstlempyFullForm)
    print('Answer from cstlempy:      '+str(answer)+'\n')
