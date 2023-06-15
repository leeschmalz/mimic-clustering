def similarity_to_distance(similarity_matrix):
    '''
    List of possible edges is similarity b/w all patients. convert to distance.
    '''
    # remove duplicates
    similarity_matrix = similarity_matrix[similarity_matrix['hadm2'] != '2018459-03091'] 
    similarity_matrix = similarity_matrix[similarity_matrix['hadm2'] != '2018459-01583'] 
    similarity_matrix = similarity_matrix[similarity_matrix['hadm2'] != '2018459-02156']
    
    max_s = similarity_matrix.similarity.max()

    similarity_matrix['similarity_norm'] = similarity_matrix.similarity / max_s
    similarity_matrix['distance'] = 1 - similarity_matrix.similarity_norm

    return similarity_matrix