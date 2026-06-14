# Model Directory

This directory contains pre-trained machine learning models.

## safety_classifier.pkl

A scikit-learn trained classifier model for safety classification.

To generate this model:
```python
import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Train a sample model (replace with actual training)
X = np.random.rand(100, 20)
y = np.random.randint(0, 2, 100)
clf = RandomForestClassifier()
clf.fit(X, y)

# Save model
with open('safety_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)
```
