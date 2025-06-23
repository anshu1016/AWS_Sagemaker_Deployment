# AWS Sagemaker Model Deployment

This project demonstrates how to train and deploy a machine learning model using AWS SageMaker, starting from data preprocessing to real-time inference via a hosted endpoint.

---

## 📦 Project Overview

This repository includes:

- Preprocessing scripts and training notebook
- Model training using a built-in or custom estimator
- Deployment via SageMaker endpoint
- Real-time predictions
- Integration with external tools (e.g., `boto3`, `sklearn`, etc.)

---

## 📁 Repo Structure

| File/Folder         | Description                                                |
|---------------------|------------------------------------------------------------|
| `train_model.ipynb` | Jupyter notebook to train and deploy model on SageMaker    |
| `inference.py`      | Script to send test data to deployed endpoint              |
| `utils/`            | Helper scripts for preprocessing, evaluation, etc.         |
| `model/`            | Saved model artifacts (if committed)                       |
| `README.md`         | This documentation                                         |

---

## ✅ Setup & Prerequisites

### 1. AWS Account & IAM Role

- An AWS account with Sagemaker permissions
- A SageMaker Execution Role with:
  - `AmazonSageMakerFullAccess`
  - Access to S3 for input/output

### 2. Install Required Libraries

You can use SageMaker Studio or a local Jupyter environment:

```bash
pip install boto3 sagemaker pandas scikit-learn
```

---

## 🚀 How to Run

### Step 1: Launch SageMaker Studio or Notebook Instance

1. Create or use an existing SageMaker Notebook instance
2. Upload the repo or clone it:
   ```bash
   git clone https://github.com/anshu1016/AWS_Sagemaker_Deployment.git
   ```

---

### Step 2: Prepare and Upload Data

- Clean and preprocess your dataset
- Upload to S3:
```python
s3 = boto3.client('s3')
s3.upload_file('yourfile.csv', 'your-bucket-name', 'yourfile.csv')
```

---

### Step 3: Train the Model

In `train_model.ipynb`:
- Use a built-in SageMaker Estimator (e.g., `LinearLearner`, `XGBoost`) or custom container
- Define training script and input channels
- Call `.fit()` to begin training

```python
estimator.fit({'train': s3_input_path})
```

---

### Step 4: Deploy the Model

```python
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.m4.xlarge',
    endpoint_name='custom-endpoint'
)
```

---

### Step 5: Run Inference

Run the `inference.py` script:

```bash
python inference.py
```

Or use:

```python
response = predictor.predict([[value1, value2, value3]])
print(response)
```

---

## 🔍 Monitor & Delete Endpoint

```python
sagemaker_client.delete_endpoint(EndpointName='custom-endpoint')
```

Always delete endpoints to avoid charges.

---

## 🧪 Testing in Local Environment

You can simulate the endpoint call using `boto3`:

```python
client = boto3.client('sagemaker-runtime')
response = client.invoke_endpoint(
    EndpointName='custom-endpoint',
    Body=json.dumps(payload),
    ContentType='application/json'
)
```

---

## 📈 Future Improvements

- CI/CD deployment via CodePipeline
- Auto-scaling endpoints
- Model versioning with Model Registry
- Integration with Streamlit or FastAPI for UI

---

## 📊 Author

**Anshu Shukla**  
GitHub: [anshu1016](https://github.com/anshu1016)

---

## 📄 License

MIT License
