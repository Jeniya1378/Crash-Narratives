import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
import joblib
import tkinter as tk
from tkinter import messagebox
import os
import subprocess

# === Reconstruct the original multi-head model ===
class CrashBERTMultiHead(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        hidden = self.bert.config.hidden_size
        self.fc1 = nn.Linear(hidden, num_classes['unit_1_direction'])
        self.fc2 = nn.Linear(hidden, num_classes['unit_1_movement'])
        self.fc3 = nn.Linear(hidden, num_classes['unit_2_direction'])
        self.fc4 = nn.Linear(hidden, num_classes['unit_2_movement'])
        self.fc5 = nn.Linear(hidden, num_classes['unit_at_fault'])
        self.fc6 = nn.Linear(hidden, num_classes['crash_type'])

    def forward(self, input_ids, attention_mask):
        pooled = self.bert(input_ids=input_ids, attention_mask=attention_mask).pooler_output
        return {
            'unit_1_direction': self.fc1(pooled),
            'unit_1_movement': self.fc2(pooled),
            'unit_2_direction': self.fc3(pooled),
            'unit_2_movement': self.fc4(pooled),
            'unit_at_fault': self.fc5(pooled),
            'crash_type': self.fc6(pooled)
        }

# === Load model and encoders ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
labels = ['unit_1_direction', 'unit_1_movement', 'unit_2_direction', 'unit_2_movement', 'unit_at_fault', 'crash_type']
encoders = {}
num_classes = {}

for label in labels:
    encoders[label] = joblib.load(f"multihead_saved_encoders/{label}_encoder.pkl")
    num_classes[label] = len(encoders[label].classes_)

model = CrashBERTMultiHead(num_classes)
model.load_state_dict(torch.load("crash_bert_multi_output.pt", map_location=device))
model.to(device)
model.eval()

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# === Prediction ===
last_prediction = {}

def predict(description):
    global last_prediction
    tokens = tokenizer(description, return_tensors="pt", padding=True, truncation=True, max_length=128)
    input_ids = tokens['input_ids'].to(device)
    attention_mask = tokens['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        result = {}
        for key, logits in outputs.items():
            pred_idx = torch.argmax(logits, dim=1).item()
            result[key] = encoders[key].classes_[pred_idx]
        last_prediction = result
        return result

# === GUI ===
def on_predict():
    text = entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter a crash description.")
        return
    result = predict(text)
    result_text = "\n".join([f"{k}: {v}" for k, v in result.items()])
    messagebox.showinfo("Prediction", result_text)

    # Save to config.py
    unit_at_fault = last_prediction['unit_at_fault'].replace(" ", "")
    with open("config.py", "w") as f:
        f.write("sample_diagram = {\n")
        f.write(f"    'unit1_dir': '{last_prediction['unit_1_direction']}',\n")
        f.write(f"    'unit1_mov': '{last_prediction['unit_1_movement']}',\n")
        f.write(f"    'unit2_dir': '{last_prediction['unit_2_direction']}',\n")
        f.write(f"    'unit2_mov': '{last_prediction['unit_2_movement']}',\n")
        f.write(f"    'unit_at_fault': '{unit_at_fault}',\n")
        f.write(f"    'crash_type': '{last_prediction['crash_type']}'\n")
        f.write("}\n")

def on_draw():
    subprocess.run(["python", "draw.py"])

# === Build UI ===
root = tk.Tk()
root.title("Crash Predictor - Multi-Head Model")
root.geometry("600x400")

label = tk.Label(root, text="Enter Crash Description:")
label.pack(pady=10)

entry = tk.Text(root, height=6, width=70)
entry.pack()

button = tk.Button(root, text="Predict", command=on_predict)
button.pack(pady=10)

draw_button = tk.Button(root, text="Draw Diagram", command=on_draw)
draw_button.pack(pady=10)

root.mainloop()
