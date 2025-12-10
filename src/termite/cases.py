import re
import random
from typing import TypedDict, Callable, Any


class LetterInfo(TypedDict, total=False):
    s: str | list[str]
    letter: str
    wordIndex: int
    word: str
    prevWord: str
    nextWord: str
    letterInWordIndex: int
    letterIndex: int  # Added for alternatingcase and inversecase


class CaseConfig(TypedDict, total=False):
    name: str
    separator: str | Callable[[LetterInfo], str]
    capitalizeFirstLetterOfString: bool | None | Callable[[LetterInfo], bool | None]
    capitalizeFirstLetterOfWord: bool | None | Callable[[LetterInfo], bool | None]
    capitalizeLetter: bool | None | Callable[[LetterInfo], bool | None]


def split_into_words(s: str) -> list[str]:
    """Split on multiple criteria to handle all case types"""
    result: list[str] = []
    current_word = ''

    for i in range(len(s)):
        char = s[i]
        prev_char = s[i - 1] if i > 0 else ''
        next_char = s[i + 1] if i < len(s) - 1 else ''

        # Check if this character should start a new word
        is_separator = bool(re.search(r'[\s\-_.\/\\|:;,!@#$%^&*()+=\[\]{}~`"\'\<\>?]', char))
        is_upper = bool(re.search(r'[A-Z]', char))
        is_lower = bool(re.search(r'[a-z]', char))
        is_digit = bool(re.search(r'[0-9]', char))
        is_letter = bool(re.search(r'[a-zA-Z]', char))
        
        prev_is_upper = bool(re.search(r'[A-Z]', prev_char)) if prev_char else False
        prev_is_lower = bool(re.search(r'[a-z]', prev_char)) if prev_char else False
        prev_is_letter = bool(re.search(r'[a-zA-Z]', prev_char)) if prev_char else False
        prev_is_digit = bool(re.search(r'[0-9]', prev_char)) if prev_char else False
        
        next_is_upper = bool(re.search(r'[A-Z]', next_char)) if next_char else False
        next_is_lower = bool(re.search(r'[a-z]', next_char)) if next_char else False
        
        should_split = (
            # Traditional separators (space, dash, underscore, dot, slash, etc.)
            is_separator or

            # camelCase/PascalCase: lowercase to uppercase (but not acronyms)
            (prev_char and
             is_upper and
             prev_is_lower and
             not next_is_upper) or

            # Handle acronyms followed by regular words: XMLParser -> XML, Parser
            (prev_char and
             is_upper and
             prev_is_upper and
             next_char and
             next_is_lower) or

            # Numbers to letters or letters to numbers
            (prev_char and
             ((is_digit and prev_is_letter) or
              (is_letter and prev_is_digit)))
        )

        if should_split:
            # If it's a separator character, save current word and skip the separator
            if is_separator:
                if current_word:
                    result.append(current_word)
                    current_word = ''
                # Skip the separator character
            else:
                # If it's a case change, save current word and start new word with this character
                if current_word:
                    result.append(current_word)
                current_word = char
        else:
            current_word += char

    # Add the last word if there is one
    if current_word:
        result.append(current_word)

    return [word for word in result if len(word) > 0]


def to_custom_case(s: str | list[str], case_config: CaseConfig) -> str:
    """Use advanced word splitting to handle all case types"""
    words = s if isinstance(s, list) else split_into_words(s)
    result = ''
    letter_index = 0  # Track global letter index for alternatingcase/inversecase

    for word_index in range(len(words)):
        word = words[word_index]

        # Add separator before word (except for first word)
        if word_index > 0:
            if isinstance(case_config['separator'], str):
                result += case_config['separator']
            else:
                # For function separators, we check if we should add a separator before this word
                letter_info: LetterInfo = {
                    's': s,
                    'letter': word[0] if word else '',
                    'wordIndex': word_index,
                    'word': word,
                    'prevWord': words[word_index - 1] if word_index > 0 else '',
                    'nextWord': words[word_index + 1] if word_index < len(words) - 1 else '',
                    'letterInWordIndex': 0,
                }
                sep = case_config['separator'](letter_info)
                if sep:
                    result += sep  # Default separator when function returns true

        # Process each letter in the word
        for letter_in_word_index in range(len(word)):
            letter = word[letter_in_word_index]
            letter_info: LetterInfo = {
                's': s,
                'letter': letter,
                'wordIndex': word_index,
                'word': word,
                'prevWord': words[word_index - 1] if word_index > 0 else '',
                'nextWord': words[word_index + 1] if word_index < len(words) - 1 else '',
                'letterInWordIndex': letter_in_word_index,
                'letterIndex': letter_index,
            }

            should_capitalize: bool | None = None

            if letter_in_word_index == 0:
                # Override for first letter of entire string
                if word_index == 0:
                    if callable(case_config.get('capitalizeFirstLetterOfString')):
                        should_capitalize = case_config['capitalizeFirstLetterOfString'](letter_info)
                    elif case_config.get('capitalizeFirstLetterOfString') is not None:
                        should_capitalize = case_config['capitalizeFirstLetterOfString']
                else:
                    # First letter of word
                    if callable(case_config.get('capitalizeFirstLetterOfWord')):
                        should_capitalize = case_config['capitalizeFirstLetterOfWord'](letter_info)
                    elif case_config.get('capitalizeFirstLetterOfWord') is not None:
                        should_capitalize = case_config['capitalizeFirstLetterOfWord']
            elif callable(case_config.get('capitalizeLetter')):
                should_capitalize = case_config['capitalizeLetter'](letter_info)
            elif case_config.get('capitalizeLetter') is not None:
                should_capitalize = case_config['capitalizeLetter']

            if should_capitalize is None:
                result += letter
            else:
                result += letter.upper() if should_capitalize else letter.lower()
            
            letter_index += 1

    return result


_case_configs: dict[str, CaseConfig] = {
    # Standard text cases
    'titlecase': {
        'name': "Title Case",
        'separator': " ",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': lambda w: w['wordIndex'] == 0 or w['word'].lower() not in ['of', 'in', 'at', 'by'],
        'capitalizeLetter': lambda w: w['word'].lower() in ['ai'],
    },
    'sentencecase': {
        'name': "Sentence case",
        'separator': " ",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'lowercase': {
        'name': "lowercase",
        'separator': " ",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'uppercase': {
        'name': "UPPERCASE",
        'separator': " ",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': True,
        'capitalizeLetter': True
    },

    # Programming cases
    'camelcase': {
        'name': "camelCase",
        'separator': "",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': True,
        'capitalizeLetter': False
    },
    'pascalcase': {
        'name': "PascalCase",
        'separator': "",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': True,
        'capitalizeLetter': False
    },
    'snakecase': {
        'name': "snake_case",
        'separator': "_",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'titlesnakecase': {
        'name': "Tile_Snake_Case",
        'separator': "_",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': True,
        'capitalizeLetter': False
    },
    'constcase': {
        'name': "CONST_CASE",
        'separator': "_",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': True,
        'capitalizeLetter': True
    },
    'kebabcase': {
        'name': "kebab-case",
        'separator': "-",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'traincase': {
        'name': "Train-Case",
        'separator': "-",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': True,
        'capitalizeLetter': False
    },
    'screamingkebabcase': {
        'name': "SCREAMING-KEBAB-CASE",
        'separator': "-",
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': True,
        'capitalizeLetter': True
    },

    # Dot and path cases
    'dotcase': {
        'name': "dot.case",
        'separator': ".",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'pathcase': {
        'name': "path/case",
        'separator': "/",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'windowspathcase': {
        'name': "Windows\\Path\\Case",
        'separator': "\\",
        'capitalizeFirstLetterOfString': None,
        'capitalizeFirstLetterOfWord': None,
        'capitalizeLetter': None
    },

    # Special separators
    'pipecase': {
        'name': "pipe|case",
        'separator': "|",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'coloncase': {
        'name': "colon:case",
        'separator': ":",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },
    'hashcase': {
        'name': "hash#case",
        'separator': "#",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },

    # No separator cases
    'flatcase': {
        'name': "flatcase",
        'separator': "",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    },

    # Fun/meme cases
    'spongebobcase': {
        'name': "sPOnGeBoBcAsE",
        'separator': " ",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': lambda info: random.random() > 0.5
    },
    'alternatingcase': {
        'name': "aLtErNaTiNgCaSe",
        'separator': "",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': lambda info: info.get('letterIndex', 0) % 2 == 1
    },
    'inversecase': {
        'name': "iNVERSE cASE",
        'separator': " ",
        'capitalizeFirstLetterOfString': False,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': lambda info: info.get('letterIndex', 0) % 2 == 0
    },
    'togglecase': {
        'name': "tOGGLE cASE",
        'separator': " ",
        'capitalizeFirstLetterOfString': lambda info: info['letter'].lower() == info['letter'],
        'capitalizeFirstLetterOfWord': lambda info: info['letter'].lower() == info['letter'],
        'capitalizeLetter': lambda info: info['letter'].lower() == info['letter']
    },
    'readmecase': {
        'name': "programmer🔥case🚀",
        'separator': lambda info: (
            " " if (r := random.random()) < 0.25
            else "🚀 " if r < 0.6
            else "🔥 " if r < 0.85
            else "🙌 "
        ),
        'capitalizeFirstLetterOfString': True,
        'capitalizeFirstLetterOfWord': False,
        'capitalizeLetter': False
    }
}


def tocasekey(s: str) -> str:
    k = to_custom_case(s, _case_configs['flatcase'])
    return k if k.endswith('case') else f"{k}case"


class CaseConfigs:
    """Proxy-like class for case configs with dynamic key lookup"""
    def __init__(self):
        for k in _case_configs:
            setattr(self, k, self[k])

    def __getitem__(self, key: str) -> CaseConfig:
        return _case_configs[tocasekey(key)]

    def __getattr__(self, item):
        return self[item]
    
    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self):
        for k in _case_configs:
            yield k, self[k]



case_configs = CaseConfigs()
registry = {}
class Case:
    registry = registry

    def __new__(cls, name):
        key = tocasekey(name)
        if key in cls.registry:
            return cls.registry[key]
        inst = super().__new__(cls)
        cls.registry[key] = inst
        return inst

    def __init__(self, name):
        self.key = tocasekey(name)
        self.config = _case_configs[self.key]
        self.name = self.config["name"]

    def __call__(self, *t):
        t = "".join(t)
        return to_custom_case(t, self.config)

    def __repr__(self):
        return f"Case<{self.name}>"


class Cases:
    registry = registry

    def __init__(self):
        for k in _case_configs:
            setattr(self, k, self._get(k))

    """Proxy-like class for case conversion functions with dynamic key lookup"""
    def __getitem__(self, key: str) -> Callable[[str | list[str]], str]:
        if not isinstance(key, str):
            return
        return self._get(key)

    def _get(self, key: str):
        return Case(key)
    
    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __getattr__(self, item):
        return self[item]

    def __contains__(self, item):
        return tocasekey(item) in _case_configs

    def __iter__(self):
        for k in _case_configs:
            yield k, self[k]


cases = Cases()

case_names = [k.upper() for k in _case_configs]


def run_tests():
    """Test the advanced word splitting"""
    print("=== Testing Advanced Word Splitting ===")
    test_cases = [
        "hello world",
        "hello-world",
        "hello_world",
        "helloWorld",
        "HelloWorld",
        "XMLHttpRequest",
        "iPhone13Pro",
        "user.name.value",
        "file/path/name",
        "some:colon:case",
        "mixed_case-and.formats",
        "camelCaseWith_underscores-and.dots",
        "HTML5Parser",
        "getHTMLElementById",
        "iOS15",
        "version2.0.1"
    ]

    for test in test_cases:
        words = split_into_words(test)
        word_str = ", ".join(f'"{w}"' for w in words)
        print(f'"{test}" → [{word_str}]')
    print()

    # Usage examples
    test_string = "Hello World Example"
    print("=== Case Conversion Examples ===")
    print("Original:", test_string)
    print()

    # Standard cases
    print("Standard Cases:")
    print("Title Case:", cases['titlecase'](test_string))
    print("Sentence case:", cases['sentencecase'](test_string))
    print("lowercase:", cases['lowercase'](test_string))
    print("UPPERCASE:", cases['uppercase'](test_string))
    print()

    # Programming cases
    print("Programming Cases:")
    print("camelCase:", cases['camelcase'](test_string))
    print("PascalCase:", cases['pascalcase'](test_string))
    print("snake_case:", cases['snakecase'](test_string))
    print("CONST_CASE:", cases['constcase'](test_string))
    print("kebab-case:", cases['kebabcase'](test_string))
    print("Train-Case:", cases['traincase'](test_string))
    print("SCREAMING-KEBAB-CASE:", cases['screamingkebabcase'](test_string))
    print()

    # Path and separator cases
    print("Path & Separator Cases:")
    print("dot.case:", cases['dotcase'](test_string))
    print("path/case:", cases['pathcase'](test_string))
    print("Windows\\Path\\Case:", cases['windowspathcase'](test_string))
    print("pipe|case:", cases['pipecase'](test_string))
    print("colon:case:", cases['coloncase'](test_string))
    print("hash#case:", cases['hashcase'](test_string))
    print("flatcase:", cases['flatcase'](test_string))
    print()

    # Fun cases
    print("Fun Cases:")
    print("sPOnGeBoBcAsE:", cases['spongebobcase'](test_string))
    print("aLtErNaTiNgCaSe:", cases['alternatingcase'](test_string))
    print("iNVERSE cASE:", cases['inversecase'](test_string))
    print("tOGGLE cASE:", cases['togglecase'](test_string))
    print("readme case:", cases['readmecase'](test_string))

    # Test conversions between different case types
    print()
    print("=== Cross-Case Conversion Tests ===")
    complex_test_cases = [
        "XMLHttpRequest",
        "getUserById",
        "user_profile_data",
        "my-component-name",
        "file.path.name",
        "iOS15Update",
        "HTML5Parser",
        "version2.0.1"
    ]

    for test in complex_test_cases:
        print(f'\nOriginal: "{test}"')
        print(f'  → camelCase: "{cases["camelcase"](test)}"')
        print(f'  → snake_case: "{cases["snakecase"](test)}"')
        print(f'  → kebab-case: "{cases["kebabcase"](test)}"')
        print(f'  → Title Case: "{cases["titlecase"](test)}"')


if __name__ == "__main__":
    run_tests()

