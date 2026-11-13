from langgraph.store.memory import InMemoryStore

# long term memory, across conversations.

store = InMemoryStore()

# Namespace for a particular user
namespace = ("user_123", "preferences")

# Save a preference
store.put(namespace, "language", {"preferred_language": "Python"})

# Retrieve it
memory = store.get(namespace, "language")

print(memory.value)
