
def there_exists(terms, query):
    for term in terms:
        if term in query:
            return True