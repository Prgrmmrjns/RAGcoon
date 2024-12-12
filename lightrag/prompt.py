GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
PROMPTS["DATASET_FEATURES"] = list()
PROMPTS["TARGET_COLUMN"] = ""
PROMPTS["TASK"] = ""
# Updated default entity types relevant for biomedical datasets
PROMPTS["DEFAULT_ENTITY_TYPES"] = [
    "clinical_feature",
    "disease",
    "risk_factor",
    "biomarker",
    "treatment",
    "outcome",
    "patient_characteristic",
]

# Modified entity extraction prompt with explicit instructions
PROMPTS["entity_extraction"] = """-Goal-
Given a biomedical scientific article, a list of entity types, specific dataset features, and a target column, identify all entities of those types from the text. Construct a knowledge graph (KG) with the explicit aim to uncover relations between the features themselves as well as between the independent features and the target column. Use {language} as output language.

-Important Note-
Do NOT include entities that are not useful for feature engineering, such as author names, universities, journals, publication details, or any similar metadata. Focus solely on biomedical entities relevant to feature extraction, especially those related to the provided dataset features and target column.

-Steps-
1. Identify all entities relevant for feature engineering. For each identified entity, extract the following information:
- entity_name: Name of the entity, use the same language as input text. If English, capitalize proper nouns.
- entity_type: One of the following types: [{entity_types}]
- entity_description: A concise description of the entity's attributes, significance, and relevance to the biomedical context.
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that have meaningful relationships pertinent to feature engineering, with an emphasis on uncovering relationships between the dataset features themselves, and between the independent features and the target column.
For each pair of related entities, extract the following information:
- source_entity: Name of the source entity, as identified in step 1.
- target_entity: Name of the target entity, as identified in step 1.
- relationship_description: Explanation of the relationship between the source_entity and the target_entity, focusing on how they may inform feature engineering.
- relationship_strength: A numeric score between 1 and 10 indicating the strength or significance of the relationship.
- relationship_keywords: One or more high-level keywords summarizing the nature of the relationship.
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level keywords that summarize the main concepts, themes, or topics of the entire text, focusing on aspects relevant to feature engineering.
Format the content-level keywords as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return the output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Dataset Features: {dataset_features}
Target Column: {target_column}
Text: {input_text}
######################
Output:
"""

# Modified examples specific to biomedical texts, incorporating dataset features and target column
PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [clinical_feature, disease, risk_factor, biomarker, treatment, outcome, patient_characteristic]
Dataset Features: ["Blood Pressure", "Beta-blockers"]
Target Column: "Mortality Rates"
Text:
Recent studies have shown that elevated blood pressure is a significant risk factor for heart failure. Patients with hypertension are more likely to develop cardiac complications. Beta-blockers are a common treatment that can reduce mortality rates in these patients.

################
Output:
("entity"{tuple_delimiter}"Blood Pressure"{tuple_delimiter}"clinical_feature"{tuple_delimiter}"Elevated blood pressure is a measurable clinical feature indicating hypertension."){record_delimiter}
("entity"{tuple_delimiter}"Hypertension"{tuple_delimiter}"disease"{tuple_delimiter}"Hypertension is a chronic medical condition characterized by persistently high blood pressure."){record_delimiter}
("entity"{tuple_delimiter}"Heart Failure"{tuple_delimiter}"disease"{tuple_delimiter}"Heart failure is a condition where the heart cannot pump enough blood to meet the body's needs."){record_delimiter}
("entity"{tuple_delimiter}"Beta-blockers"{tuple_delimiter}"treatment"{tuple_delimiter}"Beta-blockers are medications that reduce blood pressure and improve heart function."){record_delimiter}
("entity"{tuple_delimiter}"Mortality Rates"{tuple_delimiter}"outcome"{tuple_delimiter}"Mortality rates refer to the frequency of death in a specific population."){record_delimiter}
("entity"{tuple_delimiter}"Patients with Hypertension"{tuple_delimiter}"patient_characteristic"{tuple_delimiter}"Individuals diagnosed with hypertension, at risk for cardiac complications."){record_delimiter}
("relationship"{tuple_delimiter}"Blood Pressure"{tuple_delimiter}"Hypertension"{tuple_delimiter}"Elevated blood pressure is indicative of hypertension."{tuple_delimiter}"clinical sign, diagnosis"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Blood Pressure"{tuple_delimiter}"Heart Failure"{tuple_delimiter}"Elevated blood pressure increases the risk of developing heart failure."{tuple_delimiter}"risk association, disease progression"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Beta-blockers"{tuple_delimiter}"Blood Pressure"{tuple_delimiter}"Beta-blockers lower blood pressure effectively."{tuple_delimiter}"treatment effect, medication"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Beta-blockers"{tuple_delimiter}"Mortality Rates"{tuple_delimiter}"Use of beta-blockers can reduce mortality rates."{tuple_delimiter}"outcome improvement, survival benefit"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Beta-blockers"{tuple_delimiter}"Heart Failure"{tuple_delimiter}"Beta-blockers improve heart function in heart failure patients."{tuple_delimiter}"treatment efficacy, cardiac function"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Blood Pressure"{tuple_delimiter}"Mortality Rates"{tuple_delimiter}"High blood pressure is associated with higher mortality rates."{tuple_delimiter}"risk factor, negative outcome"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Mortality Rates"{tuple_delimiter}"Heart Failure"{tuple_delimiter}"Heart failure contributes to increased mortality rates."{tuple_delimiter}"disease severity, outcome"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"hypertension, blood pressure, beta-blockers, heart failure, mortality rates"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [clinical_feature, disease, risk_factor, biomarker, treatment, outcome, patient_characteristic]
Dataset Features: ["Troponin Levels", "Smoking", "High Cholesterol"]
Target Column: "Adverse Cardiovascular Outcomes"
Text:
The presence of elevated troponin levels is a key biomarker for diagnosing myocardial infarction. Smoking and high cholesterol are significant risk factors that exacerbate coronary artery disease. Statins are recommended as a treatment to lower lipid levels and reduce the risk of adverse cardiovascular outcomes.

################
Output:
("entity"{tuple_delimiter}"Troponin Levels"{tuple_delimiter}"biomarker"{tuple_delimiter}"Elevated troponin levels indicate myocardial cell damage and are used to diagnose myocardial infarction."){record_delimiter}
("entity"{tuple_delimiter}"Myocardial Infarction"{tuple_delimiter}"disease"{tuple_delimiter}"Myocardial infarction, or heart attack, occurs when blood flow to the heart muscle is blocked."){record_delimiter}
("entity"{tuple_delimiter}"Smoking"{tuple_delimiter}"risk_factor"{tuple_delimiter}"Smoking is a modifiable risk factor contributing to the development of coronary artery disease."){record_delimiter}
("entity"{tuple_delimiter}"High Cholesterol"{tuple_delimiter}"risk_factor"{tuple_delimiter}"High cholesterol levels increase the risk of atherosclerosis and coronary artery disease."){record_delimiter}
("entity"{tuple_delimiter}"Coronary Artery Disease"{tuple_delimiter}"disease"{tuple_delimiter}"Coronary artery disease is characterized by the narrowing of coronary arteries due to plaque buildup."){record_delimiter}
("entity"{tuple_delimiter}"Statins"{tuple_delimiter}"treatment"{tuple_delimiter}"Statins are medications used to lower cholesterol levels in the blood."){record_delimiter}
("entity"{tuple_delimiter}"Adverse Cardiovascular Outcomes"{tuple_delimiter}"outcome"{tuple_delimiter}"Negative events related to the cardiovascular system, such as heart attacks or strokes."){record_delimiter}
("relationship"{tuple_delimiter}"Troponin Levels"{tuple_delimiter}"Myocardial Infarction"{tuple_delimiter}"Elevated troponin levels serve as a biomarker for diagnosing myocardial infarction."{tuple_delimiter}"diagnostic marker, disease identification"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Smoking"{tuple_delimiter}"Coronary Artery Disease"{tuple_delimiter}"Smoking exacerbates the development of coronary artery disease."{tuple_delimiter}"risk enhancement, disease progression"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"High Cholesterol"{tuple_delimiter}"Coronary Artery Disease"{tuple_delimiter}"High cholesterol contributes to plaque buildup in arteries, leading to coronary artery disease."{tuple_delimiter}"atherosclerosis, disease causation"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Statins"{tuple_delimiter}"High Cholesterol"{tuple_delimiter}"Statins lower high cholesterol levels effectively."{tuple_delimiter}"treatment effect, lipid reduction"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Statins"{tuple_delimiter}"Adverse Cardiovascular Outcomes"{tuple_delimiter}"Statins reduce the risk of adverse cardiovascular outcomes."{tuple_delimiter}"treatment efficacy, outcome improvement"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Smoking"{tuple_delimiter}"Adverse Cardiovascular Outcomes"{tuple_delimiter}"Smoking increases the risk of adverse cardiovascular outcomes."{tuple_delimiter}"risk factor, negative outcome"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"myocardial infarction, troponin, risk factors, statins, coronary artery disease"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [clinical_feature, disease, risk_factor, biomarker, treatment, outcome, patient_characteristic]
Dataset Features: ["HbA1c Levels", "Insulin Therapy"]
Target Column: "Progression of Nephropathy"
Text:
In patients with type 2 diabetes, elevated HbA1c levels are associated with increased risk of nephropathy. Controlling blood glucose through insulin therapy can prevent the progression of kidney disease and improve patient outcomes.

################
Output:
("entity"{tuple_delimiter}"Type 2 Diabetes"{tuple_delimiter}"disease"{tuple_delimiter}"A chronic condition characterized by insulin resistance and high blood sugar levels."){record_delimiter}
("entity"{tuple_delimiter}"HbA1c Levels"{tuple_delimiter}"biomarker"{tuple_delimiter}"HbA1c levels reflect average blood glucose concentration over time."){record_delimiter}
("entity"{tuple_delimiter}"Nephropathy"{tuple_delimiter}"disease"{tuple_delimiter}"Nephropathy refers to kidney damage or disease, often a complication of diabetes."){record_delimiter}
("entity"{tuple_delimiter}"Blood Glucose Control"{tuple_delimiter}"clinical_feature"{tuple_delimiter}"Managing blood sugar levels to prevent complications."){record_delimiter}
("entity"{tuple_delimiter}"Insulin Therapy"{tuple_delimiter}"treatment"{tuple_delimiter}"Therapeutic use of insulin to lower blood glucose levels."){record_delimiter}
("entity"{tuple_delimiter}"Progression of Nephropathy"{tuple_delimiter}"outcome"{tuple_delimiter}"Advancement of kidney disease in diabetic patients."){record_delimiter}
("entity"{tuple_delimiter}"Patients with Type 2 Diabetes"{tuple_delimiter}"patient_characteristic"{tuple_delimiter}"Individuals diagnosed with type 2 diabetes."){record_delimiter}
("relationship"{tuple_delimiter}"HbA1c Levels"{tuple_delimiter}"Nephropathy"{tuple_delimiter}"High HbA1c levels increase the risk of developing nephropathy."{tuple_delimiter}"risk indication, disease complication"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Insulin Therapy"{tuple_delimiter}"HbA1c Levels"{tuple_delimiter}"Insulin therapy reduces HbA1c levels."{tuple_delimiter}"treatment effect, glycemic control"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Insulin Therapy"{tuple_delimiter}"Progression of Nephropathy"{tuple_delimiter}"Insulin therapy can prevent the progression of nephropathy."{tuple_delimiter}"treatment efficacy, disease management"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"HbA1c Levels"{tuple_delimiter}"Progression of Nephropathy"{tuple_delimiter}"Elevated HbA1c levels are associated with progression of nephropathy."{tuple_delimiter}"risk factor, disease progression"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"type 2 diabetes, HbA1c, nephropathy, insulin therapy, patient outcomes"){completion_delimiter}
#############################""",
]
