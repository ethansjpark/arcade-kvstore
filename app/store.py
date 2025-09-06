_TOMBSTONE = object()

class Store:
    """A simple in-memory key-value store with transaction support."""

    def __init__(self):
        self.data = {}
        self.transactions = []

    def set(self, key, value):
        """Set key -> value in the current transaction or base store."""
        if self.transactions:
            self.transactions[-1][key] = value
        else:
            self.data[key] = value

    def get(self, key):
        """Return value for key, or None if not found."""
        for layer in reversed(self.transactions):
            if key in layer:
                return None if layer[key] is _TOMBSTONE else layer[key]
        return self.data.get(key)

    def delete(self, key):
        """Delete key if it exists."""
        if self.transactions:
            self.transactions[-1][key] = _TOMBSTONE
        else:
            self.data.pop(key, None)

    def begin(self):
        """Start a new transaction."""
        self.transactions.append({})

    def commit(self):
        """Commit the most recent transaction."""
        if not self.transactions:
            return False
        changes = self.transactions.pop()
        target = self.transactions[-1] if self.transactions else self.data
        for k, v in changes.items():
            if v is _TOMBSTONE:
                target.pop(k, None)
            else:
                target[k] = v
        return True

    def rollback(self):
        """Roll back the most recent transaction."""
        if not self.transactions:
            return False
        self.transactions.pop()
        return True
