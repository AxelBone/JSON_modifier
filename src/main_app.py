import streamlit as st
import json
import os


def load_json(file_path):
    """Load JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_json(file_path, data):
    """Save JSON data to a file with UTF-8 encoding."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Streamlit UI
st.title("JSON Editor App")

author_name = st.text_input("Enter Author Name", "")

uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

data = {}
file_basename = "modified"
if uploaded_file is not None:
    file_basename = os.path.splitext(uploaded_file.name)[0]  # Get original filename without extension
    file_path = os.path.join("temp.json")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    data = load_json(file_path)
    st.success("File loaded successfully!")

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

    modified_data = []
    for i, annotation in enumerate(extracted_data):
        st.markdown(f"### Annotation {i + 1}")
        annotation["sentence"] = st.text_input(f"Sentence {i + 1}", value=annotation["sentence"])
        annotation["concerned_person"] = st.text_input(f"Concerned Person {i + 1}", value=annotation["concerned_person"])
        
        new_hpo_annotations = []
        for j, hpo in enumerate(annotation["hpoAnnotations"]):
            st.markdown(f"#### HPO Annotation {i + 1}")
            hpo["hpoId"] = st.text_input(f"HPO ID {i + 1}-{j + 1}", value=hpo["hpoId"])
            hpo["hpoName"] = st.text_input(f"HPO Name {i + 1}-{j + 1}", value=hpo["hpoName"])
            new_hpo_annotations.append(hpo)
            st.markdown("---")  # Added horizontal separator
        annotation["hpoAnnotations"] = new_hpo_annotations
        modified_data.append(annotation)

    if st.button("Save Changes"):
        author_suffix = f"_{author_name}" if author_name else ""
        save_filename = f"{file_basename}{author_suffix}.json"
        save_json(save_filename, modified_data)
        st.success(f"JSON file updated successfully! Saved as {save_filename}")

    st.download_button(
        label="Download Modified JSON",
        data=json.dumps(modified_data, indent=4, ensure_ascii=False),
        file_name=f"{file_basename}_{author_name}.json" if author_name else f"{file_basename}.json",
        mime="application/json"
    )
