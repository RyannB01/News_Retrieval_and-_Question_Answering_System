from transformers import pipeline

class QAModel:
    def __init__(self):
        print("Loading models...")

        self.qa_pipeline = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2"
        )

        # NER model
        self.ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple"
        )

        print("Models loaded successfully!")

    def get_answer(self, question, context):
        result = self.qa_pipeline(question=question, context=context)

        answer = result['answer']
        score = result['score']

        #  If QA confident → use it
        if score >= 0.3 and len(answer.strip()) >= 3:
            return answer

        # =========================
        # NER FALLBACK (SMART)
        # =========================
        question_lower = question.lower()

        entities = self.ner_pipeline(context)

        # LOCATION questions
        if any(word in question_lower for word in ["where", "country", "place", "location"]):
            for ent in entities:
                if ent['entity_group'] in ['LOC', 'GPE']:
                    return ent['word']

        # PERSON questions
        if "who" in question_lower:
            for ent in entities:
                if ent['entity_group'] == 'PER':
                    return ent['word']

        # ORGANIZATION questions
        if "company" in question_lower or "organization" in question_lower:
            for ent in entities:
                if ent['entity_group'] == 'ORG':
                    return ent['word']

        return None
