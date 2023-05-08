import math

def distance(patient1, patient2):
    '''
    Calculate the similarity between the diagnosis codes of two patient encounters. 
    Weights contribution of ICD code similarity by line order.

    See Alcaide et. al.
    '''
    similarity = 0

    for ix1, dx1 in enumerate(patient1):
        if dx1 not in patient2:
            continue

        ix2 = patient2.index(dx1)
        similarity += math.log( 1 + 1/max(ix1+1, ix2+1) )

    return similarity

if __name__ == "__main__":
    # Example from Alcaide et. al. Similarity should be 0.56.
    patient1 = ['99662', '99591', '5990', '4019']
    patient2 = ['4329', '43491', '99702', '99591', '5990', '4019']

    print( round(distance(patient1, patient2), 2) )
