# enigma_shell.py



from enigma import Enigma



class EnigmaShell:
    def __init__(self):
        self._enigma = Enigma()


    def run(self):
        '''Runs the Enigma Shell Program'''
        while True:
            message = self._input_message()
            if message is None:
                break
            else:
                self._enigma.set_message(message)
                message = ''.join(self._enigma.process_message())
                print(f'| Output: {message}')
                

    def _input_message(self) -> None | str:
        '''Asks the user for the message to either encrypt or decrypt and returns it; returns None if the user inputted nothing'''
        message = input('| Message: ')
        if message:
            return message
        else:
            return None
        
        
    def get_message(self) -> None | str:
        '''Returns the current message of the Enigma'''
        return self._enigma.get_message()
    


def main():
    enigma_shell = EnigmaShell()
    enigma_shell.run()
    
    

if __name__ == '__main__':
    main()