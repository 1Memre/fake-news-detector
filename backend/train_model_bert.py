import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    DistilBertTokenizer, 
    DistilBertForSequenceClassification,
    get_linear_schedule_with_warmup
)
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
from tqdm import tqdm
import numpy as np

# Configuration
DATA_PATH = "backend/data/fake_or_real_news.csv"
MODEL_SAVE_PATH = "backend/models/distilbert_fake_news"
MAX_LENGTH = 512  # DistilBERT max sequence length
BATCH_SIZE = 8    # Smaller batch size for memory efficiency
EPOCHS = 3        # 3 epochs is usually enough for fine-tuning
LEARNING_RATE = 2e-5

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

class NewsDataset(Dataset):
    """Custom Dataset for news articles."""
    
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        # Tokenize
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def load_data():
    """Load and prepare dataset."""
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # Combine title and text for better context
    df['full_text'] = df['title'] + " " + df['text']
    
    # Convert labels to binary (0=FAKE, 1=REAL)
    df['label_binary'] = (df['label'] == 'REAL').astype(int)
    
    print(f"Loaded {len(df)} articles")
    print(f"REAL: {sum(df['label_binary'])}, FAKE: {len(df) - sum(df['label_binary'])}")
    
    return df['full_text'].values, df['label_binary'].values

def train_epoch(model, data_loader, optimizer, scheduler, device):
    """Train for one epoch."""
    model.train()
    losses = []
    correct_predictions = 0
    total_predictions = 0
    
    progress_bar = tqdm(data_loader, desc='Training')
    
    for batch in progress_bar:
        optimizer.zero_grad()
        
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        
        loss = outputs.loss
        logits = outputs.logits
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        
        losses.append(loss.item())
        
        # Calculate accuracy
        preds = torch.argmax(logits, dim=1)
        correct_predictions += torch.sum(preds == labels)
        total_predictions += labels.size(0)
        
        progress_bar.set_postfix({
            'loss': np.mean(losses),
            'acc': (correct_predictions.double() / total_predictions).item()
        })
    
    return np.mean(losses), (correct_predictions.double() / total_predictions).item()

def eval_model(model, data_loader, device):
    """Evaluate model."""
    model.eval()
    losses = []
    predictions = []
    true_labels = []
    
    with torch.no_grad():
        for batch in tqdm(data_loader, desc='Evaluating'):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            logits = outputs.logits
            
            losses.append(loss.item())
            
            preds = torch.argmax(logits, dim=1)
            predictions.extend(preds.cpu().numpy())
            true_labels.extend(labels.cpu().numpy())
    
    accuracy = accuracy_score(true_labels, predictions)
    
    return np.mean(losses), accuracy, predictions, true_labels

def train():
    """Main training function."""
    # Load data
    texts, labels = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Load tokenizer and model
    print("Loading DistilBERT model...")
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForSequenceClassification.from_pretrained(
        'distilbert-base-uncased',
        num_labels=2  # Binary classification
    )
    model = model.to(device)
    
    # Create datasets
    train_dataset = NewsDataset(X_train, y_train, tokenizer, MAX_LENGTH)
    test_dataset = NewsDataset(X_test, y_test, tokenizer, MAX_LENGTH)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)
    
    # Setup optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    total_steps = len(train_loader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )
    
    # Training loop
    best_accuracy = 0
    
    for epoch in range(EPOCHS):
        print(f'\nEpoch {epoch + 1}/{EPOCHS}')
        print('-' * 50)
        
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, scheduler, device)
        print(f'Train Loss: {train_loss:.4f}, Train Accuracy: {train_acc:.4f}')
        
        test_loss, test_acc, predictions, true_labels = eval_model(model, test_loader, device)
        print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_acc:.4f}')
        
        # Save best model
        if test_acc > best_accuracy:
            best_accuracy = test_acc
            print(f'Saving model (accuracy: {test_acc:.4f})...')
            os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
            model.save_pretrained(MODEL_SAVE_PATH)
            tokenizer.save_pretrained(MODEL_SAVE_PATH)
    
    # Final evaluation
    print('\n' + '='*50)
    print('Training Complete!')
    print(f'Best Test Accuracy: {best_accuracy:.4f}')
    print('\nClassification Report:')
    print(classification_report(true_labels, predictions, target_names=['FAKE', 'REAL']))
    
    return model, tokenizer

if __name__ == "__main__":
    print("Starting DistilBERT training for Fake News Detection")
    print("=" * 60)
    train()
    print("\nModel saved to:", MODEL_SAVE_PATH)
