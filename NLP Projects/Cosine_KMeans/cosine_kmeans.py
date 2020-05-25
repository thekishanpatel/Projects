import numpy as np

class cosine_kmeans:
    def __init__(self, num_clusters, max_iter=50, verbose = True, random_state=1837):
        self.K = num_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.verbose = verbose
        
    def initialize_means(self, vecs):
        np.random.RandomState(self.random_state)
        idx = np.random.permutation(vecs.shape[0]) # Shuffle row_ids
        cents = vecs[idx[:self.K]] # Select the first K rows as centroids using the shuffled row_ids
        return cents

    def cosine_similarity(self, vecs, mean):
        ''' The Distance Measure '''
        sims = np.zeros((vecs.shape[0], self.K))
        v_norm = np.sum(vecs**2, axis = 1)**(0.5)
        m_norm = np.sum(mean**2, axis = 1)**(0.5)
        for i in range(self.K):    
            sims[:,i] = np.dot(vecs, mean[i])/(v_norm * m_norm[i])
        return sims

    def get_mean(self, vecs, idx):
        ''' Cluster Centroid '''
        cents = np.zeros((self.K, vecs.shape[1]))
        for i in range(self.K):
            cents[i,:] = np.mean(vecs[idx == i, :], axis = 0)
        return cents

    def find_cluster(self, sims):           
        ''' unlike traditional K-Means, where you want to minimize the distance--
            here you want to maximize  the cosine similarity
        '''
        return np.argmax(sims, axis = 1)    # argmax returns indices (axis = 1 means along rows)

    def get_intertia(self, vecs, mean, idx):
        sims = np.zeros(vecs.shape[0])
        v_norm = np.sum(vecs**2, axis = 1)**(0.5)
        m_norm = np.sum(mean**2, axis = 1)**(0.5)
        
        for i in range(self.K):
            sims[idx == i] = np.dot(vecs[idx == i], mean[i])/(v_norm[idx == i] * m_norm[i])
        
        return np.sum(sims**2)

    def cluster(self, vecs):
        assert (len(vecs) >= self.K)
        self.means = self.initialize_means(vecs)
        for i in range(self.max_iter):
            old_means = self.means
            sims = self.cosine_similarity(vecs, old_means)
            self.idx = self.find_cluster(sims)
            self.means = self.get_mean(vecs, self.idx)
            inertia = self.get_intertia(vecs, self.means, self.idx)
            if self.verbose:
                print("Iterations: \t\t {}".format(i))
                print(self.idx)
                print("Inertia: \t\t{}".format(inertia))
            if np.all(old_means == self.means):
                break
            

    def predict(self, vecs):
        sims = self.cosine_similarity(vecs, self.means)
        return self.find_cluster(sims)
