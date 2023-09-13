def read_dna(dna_file):
    """
    Read a DNA string from a file.
    the file contains data in the following format:
    A <-> T
    G <-> C
    G <-> C
    C <-> G
    G <-> C
    T <-> A
    Output a list of touples
    [
        ('A', 'T'),
        ('G', 'C'),
        ('G', 'C'),
        ('C', 'G'),
        ('G', 'C'),
        ('T', 'A'),
    ]
    Where either (or both) elements in the string might be missing:
    <-> T
    G <->
    G <-> C
    <->
    <-> C
    T <-> A
    """
    pairs = []
    with open(dna_file) as dna_strand:
        # return [tuple(pair.rstrip().split("<->")) for pair in dna_strand]
        for pair in dna_strand:
            bases = pair.rstrip().split("<->")
            pairs.append((bases[0].strip(), bases[1].strip()))
    # print(pairs)
    return pairs

def is_rna(dna):
    """
    Given DNA in the aforementioned format,
    return the string "DNA" if the data is DNA,
    return the string "RNA" if the data is RNA,
    return the string "Invalid" if the data is neither DNA nor RNA.
    DNA consists of the following bases:
    Adenine  ('A'),
    Thymine  ('T'),
    Guanine  ('G'),
    Cytosine ('C'),
    RNA consists of the following bases:
    Adenine  ('A'),
    Uracil   ('U'),
    Guanine  ('G'),
    Cytosine ('C'),
    The data is DNA if at least 90% of the bases are one of the DNA bases.
    The data is RNA if at least 90% of the bases are one of the RNA bases.
    The data is invalid if more than 10% of the bases are not one of the DNA or RNA bases.
    Empty bases should be ignored.
    """
    bases = {
        'A' : 0,
        'T' : 0,
        'G' : 0,
        'C' : 0,
        'U' : 0,
    }
    for pair in dna:
        for base in pair:
            if base in bases.keys():
                bases[base.strip()] += 1
    total_bases = sum([bases[base] for base in bases.keys()])
    # print(total_bases)
    if (bases['A']+bases['T']+bases['G']+bases['C'])/total_bases >= 0.9:
        return "DNA"
    elif (bases['A']+bases['U']+bases['G']+bases['C'])/total_bases >= 0.9:
        return "RNA"
    else:
        return "Invalid"


def clean_dna(dna):
    """
    Given DNA in the aforementioned format,
    If the pair is incomplete, ('A', '') or ('', 'G'), ect
    Fill in the missing base with the match base.
    In DNA 'A' matches with 'T', 'G' matches with 'C'
    In RNA 'A' matches with 'U', 'G' matches with 'C'
    If a pair contains an invalid base the pair should be removed.
    Pairs of empty bases should be ignored.
    """
    new_dna = []
    valid_pairs = {
        "DNA" : {
            'A' : 'T',
            'T' : 'A',
            'G' : 'C',
            'C' : 'G',
        },
        'RNA' : {
            'A' : 'U',
            'U' : 'A',
            'G' : 'C',
            'C' : 'G',
        }
    }
    valid_bases = ['A','G','T','C','U']
    dna_type = is_rna(dna)
    for i, pair in enumerate(dna):
        if pair[0] and pair[1] and pair[0] == valid_pairs[dna_type][pair[1]]:
            new_dna.append(pair)
        elif not pair[0] and pair[1] in valid_bases:
            new_dna.append((valid_pairs[dna_type][pair[1]], pair[1]))
        elif pair[0] in valid_bases and not pair[1]:
            new_dna.append((pair[0], valid_pairs[dna_type][pair[0]]))
    return new_dna
            

def mast_common_base(dna):
    """
    Given DNA in the aforementioned format,
    return the most common first base:
    eg. given:
    A <-> T
    G <-> C
    G <-> C
    C <-> G
    G <-> C
    T <-> A
    The most common first base is 'G'.
    Empty bases should be ignored.
    """
    bases = {
        'A' : 0,
        'T' : 0,
        'G' : 0,
        'C' : 0,
        'U' : 0,
    }
    for pair in dna:
        if pair[0] in bases.keys():
            bases[pair[0].strip()] += 1
    return max(bases, key=bases.get)

def base_to_name(base):
    """
    Given a base, return the name of the base.
    The base names are:
    Adenine  ('A'),
    Thymine  ('T'),
    Guanine  ('G'),
    Cytosine ('C'),
    Uracil   ('U'),
    return the string "Unknown" if the base isn't one of the above.
    """
    base_names = {
        'A' : 'Adenine',
        'T' : 'Thymine',
        'G' : 'Guanine',
        'C' : 'Cytosine',
        'U' : 'Uracil',
    }
    return base_names[base.strip()]
