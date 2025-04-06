

complementoryBases = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
startSequence = input("input sequence: ")
startSequence = startSequence.upper()
complementorySequence = ""
for letter in startSequence:
    complementorySequence += complementoryBases.get(letter)
print(complementorySequence)

