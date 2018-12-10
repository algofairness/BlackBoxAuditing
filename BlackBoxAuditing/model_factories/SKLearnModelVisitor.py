import numpy as np
from BlackBoxAuditing.model_factories.AbstractModelVisitor import AbstractModelVisitor

class SKLearnModelVisitor(AbstractModelVisitor):
    def __init__(self, trained_classifier, label_index):
        super(SKLearnModelVisitor,self).__init__("SKLearn_trained")
        self.classifier = trained_classifier
        self.label_index = label_index

    def get_Xy(self, test_set):
        X = np.matrix([row[:self.label_index] + row[self.label_index+1:] for row in test_set])
        y = np.asarray([row[self.label_index] for row in test_set])
        return X, y

    def test(self, test_set, test_name = ""):
        X, y = self.get_Xy(test_set)
        predictions = self.classifier.predict(X)
        predictions_str = [str(x) for x in predictions]
        return list(zip(y, predictions))

def test():
    test_basic_model()

def test_basic_model():
    mock = MockModel()
    model = SKLearnModelVisitor(mock, 0)
    output = model.test([[0,2],[0,2]])
    output_list = [ x for x in output ]
    correct = zip([0, 0], [1, 1])
    correct_list = [ x for x in correct ]
    print("correct basic pre-trained model? -- ", output_list == correct_list)

class MockModel():
    def predict(self, X):
        return [1 for x in X]

if __name__=='__main__':
    test()
