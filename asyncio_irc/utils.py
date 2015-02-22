import cchardet


def to_unicode(bytestring):
    """Try to decode as UTF8, then fall back to cchatdet."""
    try:
        return bytestring.decode()
    except AttributeError:
        if not isinstance(bytestring, str):
            raise
        return bytestring
    except UnicodeDecodeError:
        charset = cchardet.detect(bytestring)['encoding']
        return bytestring.decode(charset)


def to_bytes(string):
    try:
        return string.encode()
    except AttributeError:
        if not isinstance(string, bytes):
            raise
        return string


def chunk_message(message, max_length):
    """
    Chunk a unicode message into lines with a max_length in bytes.

    Splits the message by linebreak chars, then words, and finally letters to
    keep the string chunks short enough.
    """
    lines = []
    # Split the message on linebreaks, and loop over lines.
    for line in message.splitlines():
        # If the line fits, add it the the lines.
        line_bytes = line.encode()
        if len(line_bytes) < max_length:
            lines.append(line_bytes)
            continue

        # As the line doesn't fit: split into words & join into smaller lines.
        line_length = 0
        words = []
        for word in line.split():
            # If word fits on end of current line, add it to the lines.
            word_bytes = word.encode()
            word_length = len(word_bytes)
            if (word_length + line_length + 1) <= max_length:
                words.append(word_bytes)
                line_length += 1 if line_length else 0
                line_length += word_length
                continue

            # Word doesn't fit at the end so finish the line.
            if line_length:
                lines.append(b' '.join(words))
                words = []
                line_length = 0

            # If the new word fits, start a new line.
            if word_length <= max_length:
                words = [word_bytes]
                line_length = word_length
                continue

            # As the word doesn't fit: split into letters & join into subwords.
            letters = []
            num_bytes = 0
            for letter in word:
                letter_bytes = letter.encode()
                letter_length = len(letter_bytes)
                if (letter_length + num_bytes) <= max_length:
                    letters.append(letter_bytes)
                    num_bytes += letter_length
                    continue

                # Letter does not fit, so finish subword, and start new one.
                lines.append(b''.join(letters))
                letters = [letter_bytes]
                num_bytes = letter_length

            if num_bytes:
                words.append(b''.join(letters))
                line_length += 1 if line_length else 0
                line_length += num_bytes

        # Join any remaining words into the list of lines.
        if line_length:
            lines.append(b' '.join(words))

    return lines
