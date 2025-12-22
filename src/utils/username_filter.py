"""
Username Filter - Strict content filtering for usernames
Blocks inappropriate words, variants, leetspeak, and suspicious patterns
"""

import re


class UsernameFilter:
    """Strict username filter to prevent inappropriate content"""

    # EXTREMELY comprehensive list of inappropriate words and variants
    # Designed to be highly restrictive for a family-friendly game
    BLOCKED_WORDS = {
        # Profanity and variants (extensive list)
        'damn', 'damm', 'dammit', 'damnit', 'darn',
        'hell', 'heck',
        'crap', 'crapp', 'crappy',
        'piss', 'pissed', 'pissing',
        'shit', 'shite', 'sht', 'shyt', 'shitt', 'feces', 'turd',
        'fuck', 'fuk', 'fck', 'fack', 'fuq', 'fock', 'phuck', 'phuk',
        'fucking', 'fuking', 'fcking', 'fking', 'fckn', 'fkn',
        'motherfucker', 'mofo', 'mfer',
        'ass', 'arse', 'asshole', 'arsehole', 'azzhole', 'butthole',
        'bitch', 'btch', 'bish', 'biatch', 'biotch', 'bitches',
        'bastard', 'basterd', 'bstard',
        'dick', 'dck', 'dik', 'dyk', 'dickhead', 'dickwad',
        'cock', 'cck', 'cok', 'coq', 'cawk', 'kock',
        'pussy', 'pussie', 'pussi', 'pusy', 'puss',
        'cunt', 'cnt', 'kunt',
        'whore', 'whor', 'hore', 'hooker',
        'slut', 'slt', 'slutty',
        'fag', 'faggot', 'fagget', 'fagg',
        'dyke', 'dike', 'bitc', 'bick', 'head', 
        'twat', 'twt', 'lick', 'eck', 'uck', 
        'wanker', 'wank', 'cuc', 'cuck'
        'bollocks', 'bollock',

        # Slurs and hate speech (comprehensive)
        'nigger', 'nigga', 'nigg', 'nig', 'negro', 'neger',
        'nazi', 'nazy', 'nzi', 'hitler', 'heil',
        'retard', 'retarded', 'retrd', 'tard',
        'spic', 'spick', 'spik',
        'chink', 'chinky',
        'gook', 'guk',
        'kike', 'kyke',
        'wetback', 'wetbak',
        'towelhead', 'raghead',
        'beaner', 'spook', 'coon', 'jigaboo',
        'zipperhead', 'slope',
        'moron', 'moronic', 'idiot', 'idiotic', 'imbecile',

        # Sexual content (extensive)
        'sex', 'sexy', 'sexual',
        'porn', 'porno', 'pornography',
        'xxx', 'xxxx',  # Will match as substring since longer than 3 chars
        'nude', 'nudes', 'naked',
        'rape', 'raped', 'raping', 'rapist',
        'penis', 'pennis', 'penus',
        'vagina', 'vag', 'vajayjay',
        'boob', 'boobs', 'boobies', 'breast', 'tit', 'tits', 'titty', 'titties',
        'anal', 'anus',
        'oral', 'blowjob', 'handjob',
        'horny', 'hornay',
        'orgasm', 'cum', 'cumm', 'jizz',
        'masturbate', 'masturbation',
        'dildo', 'vibrator',
        'nsfw',

        # Violence and disturbing content
        'kill', 'killer', 'killing', 'killed', 'kil', 'kll',
        'murder', 'murderer', 'murdering',
        'death', 'dead', 'die', 'dying', 'died',
        'suicide', 'suicidal', 'kys', 'killurself',
        'terrorist', 'terrorism', 'terror',
        'bomb', 'bomber', 'bombing', 'explosive',
        'shoot', 'shooter', 'shooting', 'shot',
        'gun', 'rifle', 'weapon',
        'genocide', 'holocaust',
        'torture', 'torturing',
        'hang', 'hanging', 'hanged',
        'stab', 'stabbed', 'stabbing',
        'lynch', 'lynching',

        # Drugs and substances
        'weed', 'marijuana', 'cannabis', 'ganja', 'pot', 'dope',
        'cocaine', 'coke', 'crack',
        'heroin', 'smack',
        'meth', 'methamphetamine', 'crystal',
        'drug', 'drugs', 'druggie',
        'high', 'stoned', 'baked',
        'acid', 'lsd', 'trip', 'tripping',
        'ecstasy', 'molly', 'mdma',
        'xanax', 'oxy', 'oxycontin',

        # Other inappropriate content
        'pedo', 'pedophile', 'paedo',
        'molest', 'molester', 'molesting',
        'abuse', 'abuser', 'abusive',
        'hate', 'hatred', 'hater',
        'racist', 'racism',
        'sexist', 'sexism',
        'scam', 'scammer', 'scamming',
        'spam', 'spammer', 'spamming',

        # Crude/Juvenile terms
        'poop', 'poopy', 'caca',
        'butt', 'butthead',
        'fart', 'farting', 'flatulence',
        'pee', 'peeing', 'urine',
        'dumb', 'dumbass', 'dumbo',
        'stupid', 'stupidity',
        'loser', 'losers',
        'suck', 'sucks', 'sucking', 'sucker',
        'gay' # Only in negative context - but blocking entirely for safety

        # Test words
        'bad', 'badword',
    }

    # Leetspeak and character substitutions
    LEETSPEAK_MAP = {
        '0': 'o',
        '1': 'i',
        '3': 'e',
        '4': 'a',
        '5': 's',
        '7': 't',
        '8': 'b',
        '@': 'a',
        '$': 's',
        '!': 'i',
        '+': 't',
        '|': 'i',
        '(': 'c',
        ')': 'c',
        '<': 'c',
        '>': 'c',
        '[': 'c',
        ']': 'c',
        '{': 'c',
        '}': 'c',
        '*': 'a',
        '#': 'h',
        '&': 'a',
    }

    @classmethod
    def normalize_text(cls, text):
        """Normalize text to catch variants and leetspeak"""
        if not text:
            return ""

        # Convert to lowercase
        normalized = text.lower()

        # Remove special characters but keep track for leetspeak
        # First, substitute leetspeak characters
        for leet_char, normal_char in cls.LEETSPEAK_MAP.items():
            normalized = normalized.replace(leet_char, normal_char)

        # Remove all remaining special characters and spaces
        normalized = re.sub(r'[^a-z0-9]', '', normalized)

        # ONLY remove excessive repeated characters (3+ in a row, reduce to 2)
        # This prevents "hell" from becoming "hel", but catches "helllll" → "hell"
        normalized = re.sub(r'(.)\1{2,}', r'\1\1', normalized)

        return normalized

    @classmethod
    def contains_blocked_word(cls, text):
        """Check if text contains any blocked words or variants"""
        normalized = cls.normalize_text(text)

        # Also check with wildcards replaced (for "f*ck" style obfuscation)
        wildcard_normalized = re.sub(r'[^a-z0-9]', '', text.lower())

        # Special case: Check for "xxx" pattern before normalization reduces it
        # Matches xxx, XXX, xXx, etc. anywhere in the text
        if re.search(r'x{3,}', text, re.IGNORECASE):
            return True

        # Check for exact matches and substrings
        for blocked_word in cls.BLOCKED_WORDS:
            blocked_normalized = cls.normalize_text(blocked_word)

            # Skip very short words (3 chars or less) unless they are the entire username
            # This prevents false positives like "sex" in "Essex" or "Fox"
            if len(blocked_normalized) <= 3:
                # Only block if it's a complete word match or at word boundaries
                # Check if it's the entire normalized username
                if normalized == blocked_normalized:
                    return True
                # Check for word boundaries (start/end or surrounded by non-letters)
                pattern = f'(^|[^a-z]){re.escape(blocked_normalized)}($|[^a-z])'
                if re.search(pattern, normalized):
                    return True
            else:
                # For longer words (4+ chars), check as substring
                if blocked_normalized in normalized:
                    return True
                # Also check against wildcard-removed version
                if blocked_normalized in wildcard_normalized:
                    return True

            # Check for character-separated variants (e.g., "f*u*c*k" or "f-u-c-k")
            # Create a regex pattern that allows any character between letters
            if len(blocked_normalized) >= 4:
                # Create pattern like "f.?u.?c.?k" to match "f*uck", "f-uck", etc.
                pattern_chars = '.?'.join(re.escape(c) for c in blocked_normalized)
                pattern = f'{pattern_chars}'
                if re.search(pattern, normalized, re.IGNORECASE):
                    return True

        return False

    @classmethod
    def contains_repeated_pattern(cls, text):
        """Check for suspicious repeated patterns"""
        # Check for excessive character repetition (e.g., "aaaaaaa")
        if re.search(r'(.)\1{4,}', text):
            return True

        # Check for pattern repetition (e.g., "lollollol")
        for length in range(2, 5):
            pattern = f'(.{{{length}}})\\1{{2,}}'
            if re.search(pattern, text.lower()):
                return True

        return False

    @classmethod
    def is_valid_username(cls, username):
        """
        Validate username with EXTREMELY strict filtering

        Returns: (is_valid, error_message)
        """
        # Check if username is empty or only whitespace
        if not username or not username.strip():
            return False, "Username cannot be empty"

        username = username.strip()

        # Check length
        if len(username) < 2:
            return False, "Username must be at least 2 characters"

        if len(username) > 20:
            return False, "Username must be 20 characters or less"

        # Must contain at least one letter
        if not any(c.isalpha() for c in username):
            return False, "Username must contain at least one letter"

        # Check for blocked words
        if cls.contains_blocked_word(username):
            return False, "Username contains inappropriate content"

        # Check for suspicious patterns
        if cls.contains_repeated_pattern(username):
            return False, "Username contains invalid patterns"

        # STRICTER: Check for excessive numbers (likely spam/bot)
        num_digits = sum(c.isdigit() for c in username)
        if num_digits > len(username) * 0.5:  # More than 50% numbers (reduced from 70%)
            return False, "Username contains too many numbers"

        # STRICTER: Check for excessive special characters
        special_chars = sum(not c.isalnum() and c not in ' -_' for c in username)
        if special_chars > 0:  # No special chars allowed except space, dash, underscore
            return False, "Username contains invalid characters"

        # STRICTER: Limit allowed special characters to specific ones
        allowed_special = {' ', '-', '_'}
        for char in username:
            if not char.isalnum() and char not in allowed_special:
                return False, "Username contains invalid characters"

        # Check for URL patterns
        if any(pattern in username.lower() for pattern in ['.com', '.net', '.org', '.io', '.co', 'http', 'www', '://', 'bit.ly']):
            return False, "Username cannot contain URLs"

        # Check for common spam patterns
        spam_patterns = [
            r'\d{7,}',  # 7+ consecutive digits (reduced from 10)
            r'[a-z]{18,}',  # 18+ consecutive letters (reduced from 20)
            r'^[^a-zA-Z]*$',  # No letters at all
            r'\d+\s*\d+\s*\d+\s*\d+\s*\d+',  # Many numbers even with spaces
        ]

        for pattern in spam_patterns:
            if re.search(pattern, username):
                return False, "Username contains invalid patterns"

        # Check for multiple consecutive spaces
        if '  ' in username:
            return False, "Username contains invalid spacing"

        # Check for leading/trailing special characters
        if username[0] in '-_ ' or username[-1] in '-_ ':
            return False, "Username cannot start or end with special characters"

        # Check for too many consecutive special characters
        if re.search(r'[-_]{3,}', username):
            return False, "Username contains invalid patterns"

        # All checks passed
        return True, ""

    @classmethod
    def sanitize_username(cls, username):
        """
        Sanitize username by removing invalid characters
        This is a helper function for the input field
        """
        if not username:
            return ""

        # Remove leading/trailing whitespace
        sanitized = username.strip()

        # Limit length
        sanitized = sanitized[:20]

        return sanitized


def validate_username(username):
    """
    Convenience function for validating usernames

    Args:
        username: The username to validate

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    return UsernameFilter.is_valid_username(username)


def sanitize_username(username):
    """
    Convenience function for sanitizing usernames

    Args:
        username: The username to sanitize

    Returns:
        str: Sanitized username
    """
    return UsernameFilter.sanitize_username(username)
