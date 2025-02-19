from __future__ import annotations


def apply_personality(response: str, personality: str) -> str:
    """
    Optionally fine-tunes the already personality-specific response.
    """
    if personality == 'friendly' and '😊' not in response:
        response = response.strip() + ' 😊'
    elif personality == 'formal':
        response = response.strip()
        if response and not response[0].isupper():
            response = response[0].upper() + response[1:]
    elif personality == 'professional':
        response = ' '.join(response.split())
    elif personality == 'casual' and not response.endswith('!'):
        response = response.strip() + '!'
    elif personality == 'humorous' and 'lol' not in response.lower():
        response = response.strip() + ' lol'

    return response
