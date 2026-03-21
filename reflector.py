# reflector.py



class Reflector:
    def __init__(self, keywords: list[str], primary_preset: list[int]):
        self._keywords = keywords
        first_half = primary_preset[:(len(primary_preset) // 2)]
        second_half = primary_preset[(len(primary_preset) // 2):]
        self._primary_reflector_num_alterations = dict(zip(first_half, second_half))
        self._secondary_reflector_num_alterations = dict(zip(second_half, first_half))
        
    
    def determine_reflection(self, keyword: str) -> str:
        '''Takes in a keyword and returns the new keyword reflected by the reflector'''
        input_index = self._keywords.index(keyword)
        if input_index in self._primary_reflector_num_alterations.keys():
            output_index = self._primary_reflector_num_alterations[input_index]
        else:
            output_index = self._secondary_reflector_num_alterations[input_index]
            
        return self._keywords[output_index]