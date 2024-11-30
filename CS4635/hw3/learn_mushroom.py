import json
import random
import pandas as pd
from collections import defaultdict, Counter

class LearningSystem(object):
	"""
	Set up a learning system class, i.e., the approach you will apply.
	Feel free to create any functions under the class.

	Two functions are REQUIRED:
	- LearningSystem.fit(train_set, train_labels)
	- LearningSystem.predict(instance)
	"""

	def __init__(self):
		"""
		You can have any other parameters here.
		"""
		self.class_probabilities = {}
		self.feature_probabilities = {}
		self.top_features = [
			'habitat', 'odor', 'stalk-root', 'ring-type', 'cap-color', 
			'population', 'gill-color', 'gill-attachment', 
			'stalk-surface-below-ring', 'cap-surface'
		]


	def fit(self, train_set, train_labels):
		"""
		Train the system with this function.
		Do NOT set any input variable other than train_set and train_labels for this function.
		========
		train_data: training data without labels. It should be a list of dictionaries.
		train_labels: A list of labels of training data. Each label has the same index as its data in train_data.
					  All labels are binary (0, 1).
		"""
		label_counts = Counter(train_labels)
		total_samples = len(train_labels)
		self.class_probabilities = {label: count / total_samples for label, count in label_counts.items()}
		self.feature_probabilities = {label: defaultdict(lambda: defaultdict(int)) for label in label_counts}

		for instance, label in zip(train_set, train_labels):
			for feature in self.top_features:
				value = instance[feature]
				self.feature_probabilities[label][feature][value] += 1

		for label, features in self.feature_probabilities.items():
			for feature, value_counts in features.items():
				total_feature_count = sum(value_counts.values())
				for value, count in value_counts.items():
					self.feature_probabilities[label][feature][value] = count / total_feature_count


	def predict(self, instance):
		"""
		Predict the label of an instance (a single dictionary) given.
		"""
		class_scores = {}
		for label in self.class_probabilities:
			class_scores[label] = self.class_probabilities[label]
			
			for feature in self.top_features:
				value = instance.get(feature)
				if value in self.feature_probabilities[label][feature]:
					class_scores[label] *= self.feature_probabilities[label][feature][value]
				else:
					class_scores[label] *= 1e-6  # Small smoothing factor

		return max(class_scores, key=class_scores.get)


# Then you need to make the separate define_model() function,
# so you can have any initialized parameter defined.
# Autograder will define the model object based on your define_model() function.
def define_model():
	return LearningSystem()


"""
The following codes are for testing with sample data only.
REMEMBER TO REMOVE THEM BEFORE SUBMISSION.
=============================================================================
In this homework, a sample collection of shuffled data is provided.
You might try with the data provided like in the following before submission:
"""

# def test(model, test_set_data, test_labels):
# 	correct = 0
# 	for i in range(len(test_set_data)):
# 		pred = model.predict(test_set_data[i])
# 		if pred == test_labels[i]:
# 			correct += 1
# 	accuracy = correct / len(test_set_data)
# 	return accuracy

# sample_set_data = json.load(open('sample_set_data_multiclass.json'))
# sample_set_labels = json.load(open('sample_set_labels_multiclass.json'))

# train_set = sample_set_data[:-500]
# train_labels = sample_set_labels[:-500]
# test_set = sample_set_data[-500:]
# test_labels = sample_set_labels[-500:]

# model = define_model()
# model.fit(train_set, train_labels)
# print("Accuracy:", test(model, test_set, test_labels))




