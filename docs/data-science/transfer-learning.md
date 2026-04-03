---
title: Transfer Learning
category: techniques
tags: [data-science, deep-learning, transfer-learning, fine-tuning, pretrained]
---

# Transfer Learning

Use knowledge from one task (source) to improve learning on another (target). The dominant paradigm in modern deep learning - almost never train from scratch.

## Core Idea

Pre-trained models learn general features on large datasets. Lower layers capture universal patterns (edges, textures, word frequencies). Higher layers become task-specific.

## Strategies

### Feature Extraction
Freeze all pre-trained layers. Replace and train only the final classification head.

```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet50(pretrained=True)
for param in model.parameters():
    param.requires_grad = False  # freeze everything
model.fc = nn.Linear(2048, num_classes)  # replace head
```

**Use when**: small dataset (< 1000 samples), target task similar to source.

### Fine-Tuning
Unfreeze some layers and train with low learning rate.

```python
# Unfreeze last block
for param in model.layer4.parameters():
    param.requires_grad = True

# Lower LR for pre-trained layers, higher for new head
optimizer = torch.optim.Adam([
    {'params': model.layer4.parameters(), 'lr': 1e-5},
    {'params': model.fc.parameters(), 'lr': 1e-3}
])
```

**Use when**: moderate dataset, target task somewhat different from source.

### Full Fine-Tuning
Unfreeze all layers, very low learning rate throughout.

**Use when**: large dataset, task significantly different from source.

## Vision Transfer Learning

**Source**: ImageNet (1.2M images, 1000 classes). Most torchvision models provide pre-trained weights.

**Rule of thumb**: smaller target dataset = freeze more layers; larger = fine-tune more.

**Standard normalization** (ImageNet stats):
```python
from torchvision import transforms
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

## NLP Transfer Learning

**Source**: large text corpora (Wikipedia, BooksCorpus, Common Crawl).

**Pre-training objectives:**
- BERT: Masked Language Model + Next Sentence Prediction
- GPT: Autoregressive language modeling
- T5: text-to-text (all tasks framed as generation)

**Fine-tuning with HuggingFace:**
```python
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
args = TrainingArguments(
    output_dir='./results',
    learning_rate=2e-5,  # much lower than training from scratch
    num_train_epochs=3,
    per_device_train_batch_size=16
)
trainer = Trainer(model=model, args=args, train_dataset=train_ds)
trainer.train()
```

## When Transfer Learning Helps

| Source/Target Similarity | Target Data Size | Strategy |
|--------------------------|-----------------|----------|
| Similar, small data | < 1K | Feature extraction |
| Similar, moderate data | 1K-10K | Fine-tune last layers |
| Different, large data | > 10K | Full fine-tuning |
| Very different, small data | < 1K | May not help; try anyway |

## Domain Adaptation

When source and target domains differ (e.g., photos -> medical images):
- **Gradual unfreezing**: unfreeze one layer at a time from top
- **Discriminative LR**: lower LR for earlier layers
- **Data augmentation**: bridge domain gap
- **Domain-specific pre-training**: pre-train on in-domain unlabeled data first

## Gotchas
- Pre-trained model expects specific input format (size, normalization, tokenization)
- Fine-tuning LR too high destroys pre-trained features ("catastrophic forgetting")
- Always use the matching tokenizer for NLP models
- Transfer from ImageNet may not help for non-natural images (medical, satellite)
- For tabular data, transfer learning rarely helps - gradient boosting usually wins

## See Also
- [[neural-networks]] - foundation architectures
- [[cnn-computer-vision]] - vision architectures for transfer
- [[nlp-text-processing]] - BERT and transformer fine-tuning
- [[model-evaluation]] - evaluating fine-tuned models
