import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw
import base64
from io import BytesIO
from PIL import Image
import joblib

# Load your trained cancer drug prediction model (make sure this is the right model)
clf = joblib.load('DDEM')  

# Function to predict and visualize
def predict_and_visualize(smiles):
    # Convert SMILES string to RDKit molecule
    molecule = Chem.MolFromSmiles(smiles)

    if molecule is not None:
        # Extract molecular descriptors (features)
        # Add more molecular descriptors that are relevant to cancer drug discovery
        features = [Descriptors.MolWt(molecule), Descriptors.MolLogP(molecule)]

        # Make a prediction using the loaded model
        prediction = clf.predict([features])[0]

        # Visualize the SMILES structure
        img = Draw.MolToImage(molecule)

        # Convert PIL Image to Base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Display the image using st.image()
        st.image(img, caption='Molecular Structure of the Compound', use_column_width=True)

        # Return the prediction result for cancer drug candidate
        return {'prediction': 'Potential Cancer Drug Candidate' if prediction == 1 else 'Not a Cancer Drug Candidate', 'image': img_str}
    else:
        return {'error': f'Invalid SMILES string: {smiles}'}

# Streamlit App
st.sidebar.image('1675831922306.gif')
st.markdown("""
    <style>
        /* Animate the sidebar text with a fade-in effect */
        .sidebar-text {
            animation: fadeIn 3s ease-in-out;
            font-family: 'Arial', sans-serif;
            color: #4CAF50;
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 10px;
            padding-left: 10px;
        }

        /* Keyframes for fade-in effect */
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        /* Style for the title in the sidebar */
        .sidebar .sidebar-content {
            font-family: 'Verdana', sans-serif;
            font-size: 18px;
            color: #2F4F4F;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar description with custom animation and styling
st.sidebar.markdown("""
    <div class="sidebar-text">
        This app uses machine learning to predict whether a chemical compound could be a potential <strong>cancer drug candidate</strong>.
        By inputting a SMILES string of a compound, the model will predict its effectiveness in fighting cancer.
    </div>
""", unsafe_allow_html=True)


def main():
    # Title of the Streamlit app
    st.title("Cancer Drug Discovery Predictor")
    st.image('SS.png')

   

    # Input SMILES string
    smiles = st.text_input("Enter the SMILES string of a chemical compound:")

    # Prediction button
    if st.button("Predict"):
        result = predict_and_visualize(smiles)

        # Check for errors or display prediction results
        if 'error' in result:
            st.error(result['error'])
        else:
            st.success(f"Prediction: {result['prediction']}")

if __name__ == "__main__":
    main()
