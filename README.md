# JSON Editor App for Medical Annotations

This is a Streamlit-based application that helps users annotate medical records by providing tools to modify, save, and track changes to JSON data. It is designed to handle medical annotations that include information about sentences, concerned persons, negations, and HPO (Human Phenotype Ontology) annotations.

## Features
- **Load and edit JSON files** containing medical annotations.
- **Track modifications**: The app keeps track of any changes made to the annotations.
- **Add or remove annotations**: You can add new annotations or remove existing ones.
- **Download modified JSON**: Once modifications are made, you can download the updated JSON file.
- **Easy interface**: It provides a user-friendly interface to interact with the JSON data and make modifications.

## Requirements

- Python 3.7 or higher
- Streamlit
- JSON library

To install the required libraries, use the following command:

```bash
pip install streamlit
```

## How to Use

### 1. **Upload a JSON File**
   - Click the **"Charger un fichier JSON"** button to upload a JSON file containing medical annotations. 
   - The file must be in the correct format with annotations, sentences, concerned persons, negations, and HPO annotations.

### 2. **Edit Annotations**
   - Each annotation will be displayed in the app with fields for the sentence, concerned person, negation checkbox, and HPO annotations.
   - Modify the fields as needed. You can also modify HPO annotations directly.

### 3. **Track Modifications**
   - Any modification in the annotations (e.g., changes in sentence, person, or HPO) will be tracked.
   - The "Modifications" field will be updated accordingly to reflect whether changes have been made.

### 4. **Add New Annotations**
   - You can insert a new annotation at any point in the list of annotations by clicking **"Insérer Annotation Après"**.

### 5. **Download the Modified JSON File**
   - Once you're done editing, click the **"Télécharger le JSON modifié"** button to download the updated JSON file with your modifications.

### 6. **Clean Temporary File and Refresh**
   - To clean up any temporary files, use the **"Nettoyer le fichier temporaire et actualiser la page"** button. This will delete temporary files created during the process and refresh the page.

### 7. **Return to Top**
   - Use the **"Retour au début de page"** button to quickly navigate back to the top of the page.

## How the Application Works

1. **Loading Data**: The uploaded JSON file is read and its annotations are parsed.
   - Each annotation contains a sentence, concerned person, negation field, and HPO annotations.
   
2. **Modifications Tracking**: When a field (sentence, concerned person, negation, or HPO annotation) is modified, the `modifications` flag for that annotation is set to `True`.
   - If no modifications are detected, it remains `False`.

3. **Annotations Editing**: The user can edit the sentence, concerned person, negation, and HPO annotations for each entry.
   - HPO annotations are shown in the form of `hpoId` and `hpoName`, and the user can modify them as needed.

4. **Saving Changes**: The modified annotations are stored, and the modified JSON can be downloaded.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/json-editor-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd json-editor-app
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## Folder Structure

The project contains the following structure:

```bash
json-editor-app/
├── app.py            # Main Streamlit app file
├── requirements.txt  # Dependencies
├── README.md         # Project documentation
├── temp_*.json       # Temporary files created during the app session
└── data/             # (Optional) Example JSON files
```

## Example JSON Format

Here is an example of how the JSON should be structured for the application to work properly:

```json
{
  "annotations": [
    {
      "sentence": "encéphalopathie épileptique néonatale",
      "concerned_person": "Patient",
      "negated": false,
      "modifications": false,
      "hpoAnnotations": [
        {
          "hpoId": "HP:0200134",
          "hpoName": "Convulsive encephalopathy"
        },
        {
          "hpoId": "HP:0032807",
          "hpoName": "neonatal"
        }
      ]
    }
  ]
}
```

### Fields in the JSON:
- **sentence**: The medical sentence to be annotated.
- **concerned_person**: Person associated with the medical annotation (e.g., "Patient").
- **negated**: A boolean value indicating whether the annotation is negated (e.g., "no evidence of").
- **modifications**: A boolean flag to track changes (set automatically when a modification is detected).
- **hpoAnnotations**: A list of HPO annotations, each containing `hpoId` and `hpoName`.

## Contributing

Feel free to contribute to the project by forking the repository, making changes, and submitting pull requests. If you encounter any issues or have ideas for improvements, open an issue in the GitHub repository.
