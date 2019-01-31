class EvalResult:    
    def __init__(self, precision=None, recall=None, r_precision=None, avg_precision=None, ndcg_at_10=None, ndcg_at_20=None):
        self.Precision = precision
        self.Recall = recall
        self.RPrecision = r_precision
        self.AveragePrecision = avg_precision
        self.nDCGat10 = ndcg_at_10
        self.nDCGat20 = ndcg_at_20
        return


