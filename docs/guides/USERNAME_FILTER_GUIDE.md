# Username Filter System

## Overview

The username filter system provides comprehensive protection against inappropriate usernames for the online leaderboard. It uses multiple layers of detection to catch inappropriate content, variants, leetspeak, and obfuscation attempts.

## Features

### 1. **Comprehensive Word Blocking**
- Blocks profanity, slurs, sexual content, violence, drugs, and other inappropriate terms
- Includes over 60+ blocked words with common variants
- Smart detection that considers word length to avoid false positives

### 2. **Leetspeak Detection**
Automatically detects and converts common leetspeak substitutions:
- Numbers: `0→o`, `1→i`, `3→e`, `4→a`, `5→s`, `7→t`, `8→b`
- Symbols: `@→a`, `$→s`, `!→i`, `*→a`, etc.
- Examples: "sh1t" → "shit", "d4mn" → "damn"

### 3. **Obfuscation Detection**
Catches attempts to hide inappropriate words:
- Character insertion: "f*ck", "sh-it", "b.a.d"
- Character removal: "fck", "sht", "btch"
- Repeated character reduction: "asssss" → "as"

### 4. **Pattern Detection**
Blocks suspicious patterns:
- Excessive repetition: "aaaaaaa", "lololol"
- Too many numbers: "12345678901"
- Too many special characters: "!!!!!!!", "@#$%^&*"
- URLs: ".com", "www", "http"

### 5. **Length and Character Validation**
- Minimum 2 characters
- Maximum 20 characters
- Must contain some letters (not all numbers/symbols)

## How It Works

When a user tries to submit a username, the system:

1. **Normalizes** the text (removes special chars, converts leetspeak, reduces repetition)
2. **Checks against blocked words** using multiple strategies
3. **Validates patterns** for suspicious behavior
4. **Returns** either success or a user-friendly error message

## User Experience

### Valid Username
User enters "CoolGamer123" → ✓ Accepted

### Invalid Username - Inappropriate Content
User enters "BadWord123" → ✗ Rejected
Error shown: "Username contains inappropriate content"

### Invalid Username - Pattern Issue
User enters "aaaaaaaaaa" → ✗ Rejected
Error shown: "Username contains invalid patterns"

### Error Display
- Errors appear in red text below the username input
- Error messages are generic to avoid revealing filter details
- Errors auto-dismiss after 3 seconds
- Generate Random button always creates valid usernames

## Expanding the Filter

To add more blocked words, edit `/src/utils/username_filter.py`:

```python
BLOCKED_WORDS = {
    # Add your words here
    'newbadword',
    'anotherbadword',
    # ...
}
```

**Important Notes:**
- Add common variants (e.g., "fck", "fuk" for "fuck")
- Add character-removal variants (e.g., "fack" for "f*ck")
- Test thoroughly after adding words to avoid false positives

## Testing

Run the test suite to verify the filter:

```bash
./venv/bin/python test_username_filter.py
```

The test suite includes:
- ✓ Valid usernames that should pass
- ✗ Invalid usernames that should be blocked
- Edge cases for false positives (like "Fox" with "sex" inside)
- Obfuscation attempts ("F*ck", "Sh1t", etc.)

## Files

- `/src/utils/username_filter.py` - Main filter implementation
- `/src/ui/username_input.py` - Username input screen with validation
- `/test_username_filter.py` - Comprehensive test suite
- `/USERNAME_FILTER_GUIDE.md` - This documentation

## Security Considerations

### What the Filter Catches:
✓ Direct inappropriate words
✓ Leetspeak variants (sh1t, fuk, etc.)
✓ Character substitution (f*ck, d-amn)
✓ Character removal (fck, btch)
✓ Excessive repetition/spam
✓ URL patterns

### What It Doesn't Catch:
✗ Context-dependent meanings
✗ New slang/terms not in the list
✗ Sophisticated obfuscation (requires manual review)
✗ Non-English inappropriate content (requires separate lists)

### Recommendations:
1. **Regular Updates**: Add new terms as they emerge
2. **User Reports**: Implement reporting system for manual review
3. **Moderation Queue**: Consider reviewing flagged usernames
4. **Multiple Languages**: Expand blocked word list for international users

## Privacy

- The filter runs **locally** on the game client
- No usernames are sent to external filtering services
- Generic error messages don't reveal blocked words
- Users can't probe the filter to discover all blocked words

## Performance

- Filter validation is **instant** (< 1ms per username)
- No network calls required
- Minimal memory footprint (~5KB for word list)
- No impact on game performance

## Future Enhancements

Potential improvements:
- [ ] Add more blocked words based on user reports
- [ ] Support multiple languages (Spanish, French, etc.)
- [ ] Machine learning for advanced pattern detection
- [ ] Admin dashboard to manage blocked words
- [ ] Severity levels (mild warning vs. hard block)
- [ ] Allow users to report inappropriate usernames
