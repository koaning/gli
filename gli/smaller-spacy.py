nlp  = spacy.load("en_core_web_sm")
nlp.disable_pipes("parser")
nlp.to_disk("no-parser")