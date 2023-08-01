from astropy.io import fits
from mar.config import MarManager

def remove_keywords_with_patterns(header, patterns):
    keywords_to_remove = []

    for keyword in header:
        keyword_stripped = keyword.strip()  # Remove leading/trailing whitespaces
        for pattern in patterns:
            pattern_stripped = pattern.strip()  # Remove leading/trailing whitespaces
            if pattern_stripped.lower() in keyword_stripped.lower():
                keywords_to_remove.append(keyword)
                break

    for keyword in keywords_to_remove:
        try:
            del header[keyword]
        except:
            MarManager.WARN("Could not remove keyword: " + keyword)

    return header
