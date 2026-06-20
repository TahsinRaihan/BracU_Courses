# Multi-Cancer Classification Using Machine Learning

## Overview

This project demonstrates that traditional machine learning algorithms (SVM, Random Forest, Neural Networks) combined with dimensionality reduction (PCA) can effectively classify multiple cancer types from gene expression data, achieving faster and simpler performance compared to complex deep learning models.

The project analyzes 7 different cancer datasets, comparing baseline models trained on full feature sets against PCA-reduced models, showing significant computational efficiency gains while maintaining high accuracy.

## Key Features

- **Multiple Datasets**: Analysis of 7 diverse cancer datasets ranging from 31 to 56,907 features
- **Multiple Algorithms**: Implementation of Support Vector Classifier (SVC), Random Forest, and Multi-Layer Perceptron (MLP)
- **Dimensionality Reduction**: PCA ablation study showing 5-1200x speedup with minimal accuracy loss
- **Comprehensive Metrics**: Evaluation using accuracy, precision, recall, Matthews Correlation Coefficient (MCC), and training time
- **Visualization**: MLP loss curves and comparative performance tables

## Datasets

The project uses the following datasets:

1. **CuMiDa Breast Cancer** (Microarray): 62 samples, 54,675 genes, binary classification
2. **GSE280902 Breast Cancer** (RNA-Seq): 51 samples, 28,279 genes, chemotherapy response prediction
3. **PANCAN Multi-Cancer** (RNA-Seq): 644 samples, 20,531 genes, BRCA vs others
4. **Wisconsin Diagnostic Breast Cancer**: 569 samples, 31 clinical measurements, binary classification
5. **TCGA-LUSC Lung Cancer** (RNA-Seq): 551 samples, 56,907 transcripts, tumor vs healthy
6. **Prostate Cancer Genomics**: ~300 samples, ~10,000 genes, 3-class classification
7. **Leukemia Gene Expression**: 64 samples, 22,000+ genes, 5 leukemia subtypes

## Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- matplotlib

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TahsinRaihan/multi-cancer-classification.git
   cd multi-cancer-classification
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Jupyter notebook `Multi_Cancer_Classification.ipynb` to execute the complete analysis pipeline.

The notebook performs:
1. Data loading and preprocessing
2. Baseline model training on full feature sets
3. PCA dimensionality reduction
4. Ablation study with reduced features
5. Performance comparison and visualization

## Results

The project demonstrates:
- **Average Accuracy**: 89.4% across all datasets and models
- **Speed Improvement**: 5-1200x faster training with PCA reduction
- **Accuracy Retention**: >95% accuracy maintained after dimensionality reduction
- **Robustness**: Consistent performance across diverse cancer types and data formats

## Project Structure

```
├── Multi_Cancer_Classification.ipynb  # Main analysis notebook
├── Dataset/                           # Cancer datasets
│   ├── dataset1.csv
│   ├── dataset2.csv
│   ├── dataset3.csv
│   ├── dataset4.csv
│   ├── dataset5.csv
│   ├── dataset6.csv
│   └── dataset7.csv
├── diagrams/
│   └── PROJECT_DOCUMENTATION.md       # Detailed project documentation
└── README.md                          # This file
```

## Contributing

This project was developed by:
- Tahsin Raihan (https://github.com/TahsinRaihan)

To add a team member:
1. Go to your GitHub repository
2. Navigate to Settings > Collaborators
3. Add the team member's GitHub username
4. Assign appropriate permissions (e.g., Write access for contributors)

## License

This project is for educational and research purposes.

## Citation

If you use this work, please cite the project repository.