import streamlit as st
import json
import os
import uuid
from streamlit_js_eval import streamlit_js_eval
import copy
import glob
import tempfile


def load_json(file_path):
    """Load JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_json(file_path, data):
    """Save JSON data to a file with UTF-8 encoding."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        st.success(f"File saved successfully as {file_path}")
    except Exception as e:
        st.error(f"Error saving file: {e}")

def get_modifications_state(annotation):
    """Return the correct radio button index based on the modification state"""
    return 1 if annotation.get("modifications", False) else 0


for temp_file in glob.glob("temp_*.json"):
    os.remove(temp_file)

# Streamlit UI
st.markdown('<a id="top"></a>', unsafe_allow_html=True)
st.title("JSON Editor App")
st.text("Cette application vous aidera à annoter les compte-rendus médicaux électroniques simulés. Vous pouvez modifier chaque entrée ou ajouter de nouvelles sections d'annotation. Le bouton pour enregistrer le nouveau fichier modifié se trouve tout en bas de la page. Pour passer au fichier suivant, veuillez utiliser soit le bouton en bas de page pour nettoyer les fichiers temporaires soit la croix pour retirer le fichier déjà présent mais surtout ne pas utiliser le bouton browse files avec un fichier déjà chargé. Sinon, il vous faudra recharger la page.")

author_name = st.text_input("Saisir initiale de l'auteur", "")

uploaded_file = st.file_uploader("Charger un fichier JSON", type=["json"])

data = {}
temp_file = None

if uploaded_file is not None:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json", prefix="temp_", mode='wb')
    temp_file.write(uploaded_file.getbuffer())
    temp_file.close()
    file_path = temp_file.name
    file_name = uploaded_file.name
    file_basename = os.path.splitext(file_name)[0]
    data = load_json(file_path)
    st.success("File loaded successfully!")

elif temp_file and os.path.exists(temp_file.name):
    os.remove(temp_file.name)
    temp_file = None

# Define final_data outside button logic
final_data = {}

if data:
    st.subheader("Modifier les données JSON")

    def extract_relevant_fields(json_obj):
        """Extract only the required fields from all annotations."""
        extracted_data = []
        try:
            annotations = json_obj.get("annotations", [])
            for annotation in annotations:
                entry = {
                    "sentence": annotation.get("sentence", ""),
                    "concerned_person": annotation.get("concerned_person", ""),
                    "negated": annotation.get("negated", False),
                    "modifications": annotation.get("modifications", False),  # Add modifications field
                    "hpoAnnotations": []
                }
                hpoAnnotations = annotation.get("hpoAnnotation", [])
                for hpo in hpoAnnotations:
                    entry["hpoAnnotations"].append({
                        "hpoId": hpo.get("hpoId", ""),
                        "hpoName": hpo.get("hpoName", "")
                    })
                extracted_data.append(entry)
        except Exception as e:
            st.error(f"Error extracting fields: {e}")
        return extracted_data

    extracted_data = extract_relevant_fields(data)
    # st.write(extracted_data)

    # Initialize session_state variables if they don't exist
    if "annotations" not in st.session_state:
        st.session_state.annotations = extracted_data

    if "original_annotations" not in st.session_state:
        st.session_state.original_annotations = copy.deepcopy(extracted_data)

    for i, annotation in enumerate(st.session_state.annotations):
        st.markdown(f"### Annotation {i + 1}")

        original_annotation = st.session_state.original_annotations[i]

        if "id_annotation" not in annotation:
            annotation["id_annotation"] = str(uuid.uuid4())
        
        # Sauvegarde des informations originales
        original_sentence = original_annotation["sentence"]
        original_concerned_person = original_annotation["concerned_person"]
        original_negated = original_annotation.get("negated", False)
        original_hpo_annotations = [{
            "hpoId": hpo["hpoId"],
            "hpoName": hpo["hpoName"]
        } for hpo in original_annotation.get("hpoAnnotations", [])]

        # Fields where modifications could occur
        annotation["sentence"] = st.text_input(f"Phrase {i + 1}", value=annotation["sentence"])
        annotation["concerned_person"] = st.text_input(f"Personne concernée {i + 1}", value=annotation["concerned_person"])
        
        # Add the negated field (checkbox)
        annotation["negated"] = st.checkbox(f"Négation {i + 1}", value=annotation["negated"])

        new_hpo_annotations = []
        for j, hpo in enumerate(annotation.get("hpoAnnotations", [])):
            st.markdown(f"#### Annotation HPO {i + 1}")
            hpo["hpoId"] = st.text_input(f"ID HPO {i + 1}-{j + 1}", value=hpo["hpoId"])
            hpo["hpoName"] = st.text_input(f"Nom HPO {i + 1}-{j + 1}", value=hpo["hpoName"])
            new_hpo_annotations.append(hpo)
        
        annotation["hpoAnnotations"] = new_hpo_annotations

        modifications_detected = False

        # st.write(annotation["modifications"])
        
        if "modifications" not in annotation:  # Only set modifications if not already set
            annotation["modifications"] = annotation.get("modifications", False)  
        

        # Set modifications to True if any field has changed
        if (annotation["sentence"] != original_sentence or
        annotation["concerned_person"] != original_concerned_person or
        annotation["negated"] != original_negated or
        any(hpo["hpoId"] != orig_hpo["hpoId"] or hpo["hpoName"] != orig_hpo["hpoName"]
            for hpo, orig_hpo in zip(new_hpo_annotations, original_hpo_annotations))):
            modifications_detected = True

        # Only set modifications to True once per annotation
        if not modifications_detected:
            annotation["modifications"] = annotation["modifications"]
        else:
            # Reset to False if no modifications are detected
            annotation["modifications"] = True

        # st.write(annotation["modifications"])

        # Radio for modifications, reflecting the current state of 'modifications'
        modifications_key = f"modifications_radio_{annotation['id_annotation']}"
        radio_index = get_modifications_state(annotation)
        # st.write(radio_index)
        
        annotation["modifications_radio"] = st.radio(
            "Modifications",
            ["Non", "Oui"],
            index=radio_index,
            key=modifications_key
        )

        # Update modifications based on radio input
        annotation["modifications"] = annotation["modifications_radio"] == "Oui"

        st.markdown("---")  # Added horizontal separator

        if st.button(f"Insérer Annotation Après {i + 1}"):
            new_annotation = {
            "id_annotation": str(uuid.uuid4()),  # Assigner un ID unique dès la création
            "sentence": "",
            "concerned_person": "",
            "negated": False,
            "modifications": False,  # Par défaut, pas de modifications
            "hpoAnnotations": [{"hpoId": "", "hpoName": ""}]
        }
            st.session_state.annotations.insert(i + 1, new_annotation)
            st.session_state.original_annotations.insert(i + 1, new_annotation.copy())
            st.rerun()

    final_data = {
        "annotations": [
            {
                "sentence": annotation["sentence"],
                "concerned_person": annotation["concerned_person"],
                "negated": annotation["negated"],
                "modifications": annotation["modifications"],  # Ajout du champ 'modifications'
                "hpoAnnotation": [
                    {
                        "hpoId": hpo["hpoId"],
                        "hpoName": hpo["hpoName"]
                    } for hpo in annotation["hpoAnnotations"]  # Conserver la structure exacte de hpoAnnotations
                ]
            }
            for annotation in st.session_state.annotations
        ]
    }

    # Center the download button using custom HTML
    st.markdown("""
    <style>
        .center-button {
            display: flex;
            justify-content: center;
        }
    </style>
    <div class="center-button">
        """, unsafe_allow_html=True)

    st.download_button(
        label="Télécharger le JSON modifié",
        data=json.dumps(final_data, indent=4, ensure_ascii=False),
        file_name=f"{file_basename}_{author_name}.json" if author_name else f"{file_basename}.json",
        mime="application/json"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Ensure the clean and refresh button is always visible
    st.markdown("""
    <style>
        .clean-refresh-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
    </style>
    <div class="clean-refresh-button">
        """, unsafe_allow_html=True)

    if st.button("Nettoyer le fichier temporaire et actualiser la page"):
        if temp_file and os.path.exists(temp_file.name):
            os.remove(temp_file.name)
            st.success("Temporary file cleaned successfully.")
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <style>
        .scroll-top {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background-color: #f0f0f0;  /* Light gray background */
            color: black;  /* Change text color to black */
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;  /* Remove underline */
            transition: background-color 0.3s;  /* Smooth transition for background color */
        }
        .scroll-top:hover {
            background-color: #d0d0d0;  /* Darker gray on hover */
        }
    </style>
    <a class="scroll-top" href="#top">Retour au début de page</a>
""", unsafe_allow_html=True)