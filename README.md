# InfoFinder

The projects main file is InfoFinder.py, this is where the user inputs what they want to find out more about. This main function is mostly to just
test the basic functionality of the code as of right now. In the future this project will turn into a smart assistant where it takes speech input 
from users and decides what they want. It should also priortise the best sources for the users querys instead of relying on the same sources first.
Currently the project only checks 2 sources: Wikipedia and Dictionary.com 
Currently you can only search for a term instead asking the program what you want exactly. For example you currently have to input "Java" instead of
"What is Java?".

WikiSearch and DictionarySearch both check for multiple meanings and ask the user to clarify what context they are looking for. It also detects if
the source contains any information on the term entered or not. The different layouts for Wikipedia and Dictionary.com for different pages on the website
are considered so that the code does not break from different styling or layout.
