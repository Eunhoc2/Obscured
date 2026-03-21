# enigma.py



import random
from datetime import datetime
from rotor import Rotor
from typing import Generator
from reflector import Reflector



_NUM_ROTORS = 5
_CODE_NUMBER = 3301



class Enigma:
    def __init__(self):
        self._keywords = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '_', '+', '[', ']', '{', '}', '|', ';', '\'', ':', '\\', '"', ',', '.', '<', '>', '/', '?', '`', ' ']
        self._keyword_indexes = list(range(len(self._keywords)))
        self._message = None
        self._set_random_seed()
        self._rotors = self._setup_rotors()
        self._reflector = self._setup_reflector()
        self._rotor_offsets = [0] * _NUM_ROTORS


    def _setup_rotors(self) -> list[Rotor]:
        '''Returns a list containing set up rotors'''
        rotors = []
        for _ in range(_NUM_ROTORS):
            primary_keyword_preset = random.sample(self._keyword_indexes, len(self._keyword_indexes))
            secondary_keyword_preset = random.sample(self._keyword_indexes, len(self._keyword_indexes))
            rotors.append(Rotor(self._keywords, primary_keyword_preset, secondary_keyword_preset))
        return rotors
    
    
    def _setup_reflector(self) -> Reflector:
        '''Returns a set up reflector'''
        return Reflector(self._keywords, random.sample(self._keyword_indexes, len(self._keywords)))


    def _set_random_seed(self) -> None:
        '''Sets up the current random seed'''
        today = datetime.today()
        # print(f'Random Seed: {_CODE_NUMBER + (today.year * today.month * today.day)}')
        random.seed(_CODE_NUMBER + (today.year * today.month * today.day))
    
    
    def set_message(self, new_message: str) -> None:
        '''Sets the Enigma message to the one given'''
        self._message = new_message


    def _click_rotor_offsets(self) -> None:
        '''Offsets the appropriate rotors based off of how each of them are currently offset'''
        self._rotor_offsets[0] += 1
        self._rotors[0].click_rotor_by_one()
        for index in range(1, len((self._rotors))):
            if self._rotor_offsets[index - 1] >= len(self._keywords):
                self._rotor_offsets[index - 1] = 0
                self._rotor_offsets[index] += 1
                self._rotors[index].click_rotor_by_one()


    def _cascade_character_forward(self, character: str) -> str:
        '''Cascades the given character forward through the rotor(s) and returns the transformed character'''
        for rotor in self._rotors:
            character = rotor.transfer_primary_to_secondary(character)
        return character


    def _process_character_through_reflector(self, character: str) -> str:
        '''Processes the given character through the Enigma\'s reflector and returns a generator with each transformed character'''
        return self._reflector.determine_reflection(character)
            
            
    def _cascade_character_backward(self, character: str) -> str:
        '''Cascades the given character backward through the rotor(s) and returns the transformed character'''
        for rotor in reversed(self._rotors):
            character = rotor.transfer_secondary_to_primary(character)
        return character


    def process_message(self) -> Generator[str, None, None]:
        '''Returns the processed version of the enigma\'s current message as Generator of characters'''
        if self._message is not None:
            for character in self._message:
                self._click_rotor_offsets()
                forwarded_character = self._cascade_character_forward(character)
                reflected_character = self._process_character_through_reflector(forwarded_character)
                yield self._cascade_character_backward(reflected_character)
        else:
            yield ''
                

    def get_message(self) -> None | str:
        '''Returns the current message stored in the Enigma'''
        return self._message
    
    
    def get_keywords(self) -> list[str]:
        '''Returns the keywords of the Enigma'''
        return self._keywords
    
    
    def get_rotor(self, index: int) -> Rotor:
        '''Returns the rotor from the specified index of the Enigma\'s rotors list'''
        return self._rotors[index]
    
    
# Random seed preset:
# 3301 + (year * month * day)
    
    
# For the future:    
# sent time and date sum + product of length of each word in notable quote + number of vowels in the notable quote

# https://www.geeksforgeeks.org/python/python-tkinter-tutorial/
# https://www.geeksforgeeks.org/python/python-ways-to-shuffle-a-list/
# https://echoes.soferity.com/
# https://www.markdownguide.org/basic-syntax/
# https://youtu.be/UKbP3Rjxhy0
# https://enigma.alextebbs.com/

# abcdefghijklmnopqrstuvwxyz
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# 0123456789
# !@#$%^&*()-=_+[]{}|;\':",.<>/?


# Next Ideas:
# Make the initial message preset the rotors for the next message?
# Randomly make some characters the same as in the original message
# Reverse the encrypted and/or decrypted message in some manner
# Modify the random seed determination
# Incorporate Vigenere Cipher + the current code for trolling purposes?