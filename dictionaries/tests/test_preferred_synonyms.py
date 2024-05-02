import unittest

from dictionaries.preferred_synonyms import PreferredSynonyms


class TestPreferredSynonyms(unittest.TestCase):
    synonyms_filename = "/Users/zaki/PycharmProjects/hpo_translation/dictionaries/processed/preferred_synonyms_es.jsonl"
    preferred_synonyms = PreferredSynonyms(synonyms_filename)

    def test_synonym_dictionary_built_correctly(self):
        original = "2,6,8-trioxipurina"
        self.assertEqual(self.preferred_synonyms.synonyms_dictionary[original], ["ácido úrico"],
                         "preferred synonym dictionary should map '2,6,8-trioxipurina' to 'ácido úrico'")

    def test_synonym_dictionary_holds_all_synonyms(self):
        original = "ácido-base"
        self.assertIn("ácido-básico", self.preferred_synonyms.synonyms_dictionary[original],
                      "preferred synonym dictionary should include masculine 'ácido-básico'")
        self.assertIn("ácido-básica", self.preferred_synonyms.synonyms_dictionary[original],
                      "preferred synonym dictionary should include feminine 'ácido-básica'")

    def test_postprocess_translation(self):
        phrase = 'El paciente parece sufrir problemas con el válvula del corazón'
        self.assertEqual(self.preferred_synonyms.postprocess_translation(phrase),
                         'El paciente parece sufrir problemas con la válvula cardíaca',
                         "synonym replacement should change 'válvula del corazón' to 'válvula cardíaca'")