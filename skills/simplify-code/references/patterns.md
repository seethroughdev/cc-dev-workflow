# Simplification Patterns

Specific patterns to identify and fix, organized by category.

## Dead Code

### Unused Imports
```python
# REMOVE
import os  # never used
from typing import Optional, List, Dict  # only Optional used

# KEEP only what's used
from typing import Optional
```

### Unreachable Code
```python
# BAD
def process(data):
    if not data:
        return None
    result = transform(data)
    return result
    logging.info("Done")  # unreachable

# GOOD
def process(data):
    if not data:
        return None
    return transform(data)
```

### Unused Variables
```python
# BAD
def calculate(x):
    temp = x * 2  # never read
    result = x + 1
    return result

# GOOD
def calculate(x):
    return x + 1
```

### Commented-Out Code
```python
# REMOVE entirely - git has history
# def old_implementation():
#     ...

# KEEP only if explaining why NOT to do something
# Don't use recursion here - stack overflow on deep trees
```

## Duplication

### Repeated Logic (Extract)
```python
# BAD
def create_user(data):
    if not data.get('email'):
        raise ValueError("Email required")
    if not data.get('name'):
        raise ValueError("Name required")
    ...

def update_user(data):
    if not data.get('email'):
        raise ValueError("Email required")
    if not data.get('name'):
        raise ValueError("Name required")
    ...

# GOOD
def validate_user_data(data):
    if not data.get('email'):
        raise ValueError("Email required")
    if not data.get('name'):
        raise ValueError("Name required")

def create_user(data):
    validate_user_data(data)
    ...
```

### Near-Duplicate Functions (Parameterize)
```python
# BAD
def get_active_users():
    return db.query("SELECT * FROM users WHERE status = 'active'")

def get_inactive_users():
    return db.query("SELECT * FROM users WHERE status = 'inactive'")

# GOOD
def get_users_by_status(status: str):
    return db.query(f"SELECT * FROM users WHERE status = '{status}'")
```

## Over-Engineering

### Unnecessary Abstraction Layers
```python
# BAD - abstraction adds no value
class UserRepositoryInterface(ABC):
    @abstractmethod
    def get(self, id): pass

class UserRepository(UserRepositoryInterface):
    def get(self, id):
        return db.users.find(id)

# GOOD - just use the implementation
class UserRepository:
    def get(self, id):
        return db.users.find(id)
```

### Premature Generalization
```python
# BAD - only ever called with one value
def process_data(data, *, format="json", version=1, strict=True):
    ...
process_data(data)  # always default args

# GOOD
def process_data(data):
    ...  # inline the json/v1/strict logic
```

### Factory for Single Type
```python
# BAD
class ConnectionFactory:
    @staticmethod
    def create(type="postgres"):
        if type == "postgres":
            return PostgresConnection()
        raise ValueError(f"Unknown type: {type}")

conn = ConnectionFactory.create()

# GOOD
conn = PostgresConnection()
```

## Verbose Patterns

### Boolean Comparisons
```python
# BAD
if is_valid == True:
if is_valid == False:
if len(items) > 0:
if len(items) == 0:

# GOOD
if is_valid:
if not is_valid:
if items:
if not items:
```

### Redundant Conditionals
```python
# BAD
if condition:
    return True
else:
    return False

# GOOD
return condition

# BAD
if condition:
    x = a
else:
    x = b

# GOOD
x = a if condition else b
```

### Unnecessary Else After Return
```python
# BAD
def check(x):
    if x > 0:
        return "positive"
    else:
        return "non-positive"

# GOOD
def check(x):
    if x > 0:
        return "positive"
    return "non-positive"
```

### Verbose String Building
```python
# BAD
message = "User " + user.name + " (" + str(user.id) + ")"

# GOOD
message = f"User {user.name} ({user.id})"
```

### Unnecessary List Comprehension
```python
# BAD
list(x for x in items)
[x for x in items]  # when items is already a list

# GOOD
list(items)
items  # if already a list
```

## Redundant Comments

### Stating the Obvious
```python
# BAD
i = 0  # initialize counter
users = []  # empty list for users
return result  # return the result

# GOOD - no comment needed, code is clear
i = 0
users = []
return result
```

### Repeating the Code
```python
# BAD
# Loop through users and print names
for user in users:
    print(user.name)

# GOOD - only comment if non-obvious
# Admin users need special formatting
for user in users:
    print(format_admin(user.name) if user.is_admin else user.name)
```

### Outdated Comments
Look for comments that don't match the code. Either update or remove.

## AI Slop Specific

### Excessive Try/Except
```python
# BAD - catching impossible errors
try:
    x = 1 + 1
except Exception as e:
    logger.error(f"Failed to add: {e}")
    raise

# GOOD - only catch what can fail
x = 1 + 1
```

### Unnecessary Validation
```python
# BAD - internal function, callers are trusted
def _internal_helper(items: list[str]) -> str:
    if items is None:
        raise ValueError("items cannot be None")
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    ...

# GOOD - trust internal callers, type hints document contract
def _internal_helper(items: list[str]) -> str:
    ...
```

### Over-Logging
```python
# BAD
def process(x):
    logger.debug(f"Entering process with x={x}")
    result = x + 1
    logger.debug(f"Computed result={result}")
    logger.debug("Exiting process")
    return result

# GOOD - log meaningful events only
def process(x):
    return x + 1
```

### Defensive Copies
```python
# BAD - unnecessary in most cases
def process(items):
    items = list(items)  # defensive copy "just in case"
    ...

# GOOD - only copy if mutation is a real concern
def process(items):
    ...
```
