import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: Data Collection
data = pd.read_csv('appearances.csv')

# Step 2: Data Preprocessing
data = data.dropna()  # Drop rows with missing values

# Convert categorical features into numerical representations
label_encoder = LabelEncoder()
data['position_name'] = label_encoder.fit_transform(data['position_name'])

# Separate features and target variable
X = data.drop('position_name', axis=1)
y = data['position_name']

# Step 3: Data Segmentation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Choosing a Classification Model
model = RandomForestClassifier()

# Step 5: Model Training
model.fit(X_train, y_train)

# Step 6: Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1-Score:', f1)

# Step 7: Fine-tuning the Model (optional)
# You can adjust hyperparameters using techniques like grid search or cross-validation

# Step 8: Player Position Prediction
# Apply the trained model to new player data to predict their positions
new_data = pd.DataFrame([[25, 180, 75, 10, 5]], columns=X.columns)  # Example new player data
new_data_pred = model.predict(new_data)
predicted_position = label_encoder.inverse_transform(new_data_pred)
print('Predicted Position:', predicted_position)
