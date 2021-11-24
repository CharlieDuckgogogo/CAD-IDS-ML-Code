from skmultiflow.meta import AdaptiveRandomForestClassifier
from skmultiflow.trees import HoeffdingAdaptiveTreeClassifier
from skmultiflow.meta import AccuracyWeightedEnsembleClassifier
from skmultiflow.lazy import KNNADWINClassifier
from skmultiflow.bayes import NaiveBayes
from skmultiflow.evaluation import EvaluatePrequential
from skmultiflow.data.file_stream import FileStream
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
clf=AdaptiveRandomForestClassifier()
stream = FileStream(r'three2one_15W.csv')
stream.prepare_for_use()
classifier =SGDClassifier()
evaluator = EvaluatePrequential(pretrain_size=200, max_samples=4900, batch_size=1,
                                n_wait=100, max_time=1000, output_file=r'0210909_1.csv',
                                show_plot=False, metrics=['accuracy', 'precision','recall', 'f1'])
evaluator.evaluate(stream=stream, model=classifier)
