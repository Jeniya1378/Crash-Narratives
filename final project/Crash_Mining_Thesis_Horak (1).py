import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset

# Load your dataset
df = pd.read_csv("Intersection_crashData_Clean_4.27.csv")

# Select and clean relevant columns
df = df[['description', 'CrashType']].dropna()

# Encode labels
le = LabelEncoder()
df['CrashType'] = le.fit_transform(df['CrashType'])

# Train-test split
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['description'].tolist(), df['CrashType'].tolist(), test_size=0.2, random_state=42
)

# Tokenization
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

# Dataset class
class CrashDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self): return len(self.labels)

    def __getitem__(self, idx):
        return {
            'input_ids': torch.tensor(self.encodings['input_ids'][idx]),
            'attention_mask': torch.tensor(self.encodings['attention_mask'][idx]),
            'labels': torch.tensor(self.labels[idx])
        }

train_dataset = CrashDataset(train_encodings, train_labels)
val_dataset = CrashDataset(val_encodings, val_labels)

# Load model
num_labels = len(set(train_labels))
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Train the model
trainer.train()

# Evaluate
preds_output = trainer.predict(val_dataset)
pred_labels = preds_output.predictions.argmax(-1)

print(classification_report(val_labels, pred_labels, target_names=le.classes_))
