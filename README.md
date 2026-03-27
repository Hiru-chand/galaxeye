🔭 GalaxEye: Multimodal Celestial Classifier
GalaxEye is a full-stack Machine Learning application designed to automate the classification of celestial objects—Stars, Galaxies, and Quasars—using a combination of Optical (SDSS) and Infrared (WISE) photometric data.

The system leverages a microservices architecture, separating the high-performance ML inference engine (FastAPI) from the interactive research dashboard (Streamlit).

🏗️ System Architecture
The project is decoupled into three primary layers to ensure scalability and maintainability:

Frontend (Streamlit): An intuitive UI for researchers to perform single-object lookups via Simbad/SkyCoord or process bulk CSV catalogs.

Backend (FastAPI): A RESTful API that handles feature engineering, anomaly detection, and model inference.

ML Engine (Scikit-Learn): A Random Forest Classifier trained on multimodal data, achieving high accuracy in distinguishing compact stars from distant quasars.

🚀 Getting Started
Prerequisites

Docker and Docker Compose installed.

The model artifact (astro_classifier_model.pkl) must be located in the model_artifacts/ directory.

Installation & Deployment

Clone the repository and run the following command to spin up the entire ecosystem:
docker-compose up --build

Frontend Access: http://localhost:8501

API Documentation (Swagger UI): http://localhost:8000/docs

🛠️ Key Features
1. Multimodal Classification (FR04)

The system does not rely on single-band light. It calculates "colors" (differences in magnitudes) across the electromagnetic spectrum:

Optical (u, g, r, i, z): Captures surface temperature and redshift.

Infrared (W1, W2): Essential for identifying the dust signatures of Quasars.

2. Anomaly Detection (FR11)

If the model's highest confidence score falls below 50%, the system flags the object as a potential anomaly. These may represent rare transients like supernovae or data artifacts requiring human review.

3. Interactive Sky Explorer (FR10)

Integrates the Legacy Survey Viewer via IFrame components, allowing researchers to visually verify the target coordinates resolved by the system.

4. Admin Portal & Re-training

Authorized partners can upload new survey data to trigger a background re-training cycle, ensuring the model evolves with new astronomical discoveries.

📊 Technical Stack
Language: Python 3.9+ 

ML Framework: Scikit-Learn (Random Forest) 

APIs: FastAPI, Uvicorn

UI: Streamlit 

Astrophysics Libraries: Astropy, Astroquery (Simbad Name Resolution) 

DevOps: Docker, Docker Compose

📂 Project Structure
Plaintext
galaxeye/
├── backend/            # FastAPI Inference Service
├── frontend/           # Streamlit UI Service
├── model_artifacts/    # Pickled ML models & scalers
├── research/           # Jupyter Notebooks (EDA & Training)
└── tests/              # Automated API & Logic tests