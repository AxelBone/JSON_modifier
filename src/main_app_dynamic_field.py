import streamlit as st
import json
import os
import uuid


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


# Streamlit UI

st.markdown('<a id="top"></a>', unsafe_allow_html=True)

st.title("JSON Editor App")

st.text("This app will help you annotate CR simulated. There is a commentary section at the end to put more information. You can modify each entry or add new sections.")

author_name = st.text_input("Enter Author Name", "")

uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

data = {}
file_basename = "modified"
if uploaded_file is not None:
    file_basename = os.path.splitext(uploaded_file.name)[0]  # Get original filename without extension
    file_path = os.path.join(f"temp_{uuid.uuid4().hex}.json")  # Unique temp file name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    data = load_json(file_path)
    st.success("File loaded successfully!")
    
    # Reset the commentary section when a new file is uploaded
    st.session_state.commentary = ""  # This line will clear the previous commentary


# Define `final_data` outside button logic
final_data = {}

if data:
    st.subheader("Edit JSON Data")

    def extract_relevant_fields(json_obj):
        """Extract only the required fields from all annotations."""
        extracted_data = []
        try:
            annotations = json_obj.get("annotations", [])
            for annotation in annotations:
                entry = {
                    "sentence": annotation.get("sentence", ""),
                    "concerned_person": annotation.get("concerned_person", ""),
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

    if "annotations" not in st.session_state:
        st.session_state.annotations = extracted_data
    
    if "commentary" not in st.session_state:
        st.session_state.commentary = ""

    for i, annotation in enumerate(st.session_state.annotations):
        st.markdown(f"### Annotation {i + 1}")
        annotation["sentence"] = st.text_input(f"Sentence {i + 1}", value=annotation["sentence"])
        annotation["concerned_person"] = st.text_input(f"Concerned Person {i + 1}", value=annotation["concerned_person"])
        
        new_hpo_annotations = []
        for j, hpo in enumerate(annotation.get("hpoAnnotations", [])):
            st.markdown(f"#### HPO Annotation {i + 1}")
            hpo["hpoId"] = st.text_input(f"HPO ID {i + 1}-{j + 1}", value=hpo["hpoId"])
            hpo["hpoName"] = st.text_input(f"HPO Name {i + 1}-{j + 1}", value=hpo["hpoName"])
            new_hpo_annotations.append(hpo)
            st.markdown("---")  # Added horizontal separator
        annotation["hpoAnnotations"] = new_hpo_annotations
        
        if st.button(f"Insert Annotation After {i + 1}"):
            new_annotation = {
                "sentence": "",
                "concerned_person": "",
                "hpoAnnotations": [{"hpoId": "", "hpoName": ""}]
            }
            st.session_state.annotations.insert(i + 1, new_annotation)
            st.rerun()

    # Add commentary zone
    st.subheader("Add Commentary")
    st.session_state.commentary = st.text_area("Enter any comments about the annotations", value=st.session_state.commentary, height=200)

    # Include commentary in the final data structure
    final_data = {
        "annotations": st.session_state.annotations,
        "commentary": st.session_state.commentary  # Add the commentary to the JSON data
    }

    # Save button
    st.download_button(
        label="Download Modified JSON",
        data=json.dumps(final_data, indent=4, ensure_ascii=False),
        file_name=f"{file_basename}_{author_name}.json" if author_name else f"{file_basename}.json",
        mime="application/json"
    )

    st.markdown("""
    <style>
        .scroll-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
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
    <a class="scroll-top" href="#top">Back to Top</a>
""", unsafe_allow_html=True)
    

    
    # Clean up the temp file
    os.remove(file_path)
