import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Load data and train a simple model 
iris = load_iris()
X, y = iris.data, iris.target
model = RandomForestClassifier()
model.fit(X, y)

# Save the model as model.pkl [cite: 25]
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved as model.pkl")