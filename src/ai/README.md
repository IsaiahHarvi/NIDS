# Training Anomaly Models for NIDS Integration

This document explains how to train Network Intrusion Detection System (NIDS) models for modular integration in our ML-based product. It includes details about the required setup, feature generation, checkpoints, and integration with the neural network service.
By following this guide, you can train and integrate NIDS models efficiently while maintaining modularity and compatibility with our product's neural network service.

---

## **1. Overview**

Our NIDS module is designed for modularity and flexibility. Our training pipeline processes network traffic data, generates statistical features, and trains machine learning models to detect anomalies and intrusions. The trained models can be integrated seamlessly into our neural network service for deployment.

---

## **2. Key Components**

### **a. Feature Generation Using NFStream**
We utilize [NFStream](https://github.com/nfstream/nfstream) for network traffic feature generation. NFStream extracts statistical and flow-based features from packet capture (PCAP) files. These features are essential for training and include:
- **Flow statistics:** Byte and packet counts, duration, and rates.
- **Protocol analysis:** Flags and type-based distributions.
- **Statistical measures:** Min, max, mean, and standard deviation of inter-packet arrival times.

The features are preprocessed using standard scaling and fed into the training pipeline. Ensure your data adheres to this structure.

---

### **b. Checkpoints and Model Integration**
- **Checkpoints Directory:**
  - Store trained model checkpoints in the `data/checkpoints` directory.
  - Checkpoint files should be named clearly to indicate the model type, date, and version (e.g., `mlp_nids_v1_2024-12-01.ckpt`).

- **Parameterization in Neural Network Service:**
  - Define the path to the checkpoint in the `neural network` service configuration. This ensures the correct model is loaded during deployment.
  - Example configuration parameter:
    ```yaml
    model_checkpoint: "data/checkpoints/mlp_nids_v1_2024-12-01.ckpt"
    ```

---

## **3. Training Pipeline**

### **a. Dataset Preparation**
1. Collect network traffic in PCAP format and preprocess it using NFStream to extract statistical features.
2. Ensure class labels are clean, balanced, and merged appropriately. For instance, combine similar classes (e.g., `portscan` and `port_scan`) to maintain consistency.

### **b. Model Training Steps**
1. **Set Up Environment:**
   - Ensure dependencies are installed:
     ```bash
     pip install -r requirements.txt
     ```
   - Include necessary tools such as PyTorch, Lightning, Pandas, and NFStream.

2. **Prepare the Data Module:**
   - Define paths to input data.
   - Use stratified sampling for train-test splits.
   - Apply undersampling and oversampling strategies to balance classes as needed.

3. **Train the Model:**
   - Use the `train.py` script to initiate the training:
     ```bash
     python train.py --lr 0.001 --batch_size 64 --early_stop_patience 10 --ckpt_name nids_model --constructor MLP --all_data
     ```

4. **Monitor Training:**
   - Track training and validation metrics using tools like WandB.

5. **Save Checkpoints:**
   - Store the best-performing model checkpoint in `data/checkpoints`.

---

## **4. Best Practices**

### **Modularity**
- Use parameterized configurations for paths and model parameters to make the system modular and reusable.
- Ensure all key components are decoupled, e.g., feature extraction, model training, and evaluation.

### **Feature Engineering**
- Features from NFStream are the core input for our models. Avoid adding unsupported features to ensure compatibility with the existing pipeline.

### **Reproducibility**
- Always log hyperparameters, seed values, and configurations to replicate results effectively.

---

## **5. Integration Checklist**

1. Ensure the checkpoint file is placed in `data/checkpoints`.
2. Verify that the feature generation pipeline outputs are compatible with the model's input layer.
3. Parameterize the checkpoint path in the neural network service configuration.
4. Test the trained model's performance on a validation set before deployment.
