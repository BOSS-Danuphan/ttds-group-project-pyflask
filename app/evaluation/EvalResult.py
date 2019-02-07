class EvalResult:    
    def __init__(self, precision=0.0, recall=0.0, r_precision=0.0, avg_precision=0.0, ndcg_at_10=0.0, ndcg_at_20=0.0, ndcg_at_30=0.0):
        self.Precision = precision
        self.Recall = recall
        self.RPrecision = r_precision
        self.AveragePrecision = avg_precision
        self.nDCGat10 = ndcg_at_10
        self.nDCGat20 = ndcg_at_20
        self.nDCGat30 = ndcg_at_30
        return