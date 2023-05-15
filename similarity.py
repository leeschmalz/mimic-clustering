import math
import pandas as pd

def similarity(patient1, patient2):
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

def make_list_of_possible_edges(data, condition):
    '''
    input data is DIAGNOSES_ICD.csv from MIMIC-III
    '''
    
    from tqdm import tqdm # pip3 install tqdm

    # filter to patients with condition of interest
    data.HADM_ID = data.HADM_ID.astype(str)
    hadm_list = list(data[data.ICD9_CODE == condition]['HADM_ID'])
    data = data[data.HADM_ID.isin(hadm_list)]

    # create a dictionary of patients and their diagnoses
    codes = { hadm: list(data[data.HADM_ID == hadm].sort_values(by='SEQ_NUM')['ICD9_CODE'])
              for hadm 
              in data.HADM_ID.unique() }

    # list of possible edges is similarity of all unique pairs of patients
    possible_edges = []
    for i,hadm1 in tqdm(enumerate(hadm_list), total=len(hadm_list)):
        for j,hadm2 in enumerate(hadm_list):
            if i < j: # only need to calculate similarity once for each pair
                possible_edges.append( [hadm1, hadm2, similarity(codes[hadm1], codes[hadm2])] )

    return pd.DataFrame(possible_edges, columns=['hadm1', 'hadm2', 'similarity'])

if __name__ == "__main__":
    # test functions using example from Alcaide et. al. 
    # Patient A: '115057'
    # Patient B: '117154'
    # similarity: 0.56

    # test similarity function
    patientA = ['99662', '99591', '5990', '4019']
    patientB = ['4329', '43491', '99702', '99591', '5990', '4019']
    test1 = round(similarity(patientA, patientB), 2)

    # test make_list_of_possible_edges function
    df = pd.read_csv('./DIAGNOSES_ICD.csv')
    possible_edges = make_list_of_possible_edges(df, condition='99591') # 99591 is sepsis
    
    test2 = round(possible_edges[(possible_edges.hadm1 == '115057') & (possible_edges.hadm2 == '117154') |
                                 (possible_edges.hadm1 == '117154') & (possible_edges.hadm2 == '115057')].
                  similarity.values[0], 2)
    
    print(f'Test 1: {test1} | passed: {test1==0.56}' )
    print(f'Test 2: {test2} | passed: {test2==0.56}' )
