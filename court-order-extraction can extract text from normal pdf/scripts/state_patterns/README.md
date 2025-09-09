# State Patterns Module Organization

This directory contains the reorganized state-specific pattern files for legal document extraction. 

## Structure

```
utils/state_patterns/
├── __init__.py           # Main module entry point with STATE_PATTERNS dictionary
├── kerala.py             # Kerala High Court patterns (88.7% success rate)
├── delhi.py              # Delhi High Court patterns (60.7% success rate)
├── gujarat.py            # Gujarat High Court patterns (baseline)
├── maharashtra.py        # Maharashtra High Court patterns
├── tamil_nadu.py         # Tamil Nadu High Court patterns
├── karnataka.py          # Karnataka High Court patterns
└── general.py            # General fallback patterns and utility functions
```

## Benefits

1. **Maintainability**: Each state's patterns are in separate files, making them easier to modify and maintain
2. **Scalability**: New states can be easily added by creating a new pattern file
3. **Organization**: Clear separation of concerns - each file handles one state's specific patterns
4. **Modularity**: Individual pattern files can be imported independently if needed
5. **Performance**: Proven high-performance patterns (Kerala: 88.7%, Delhi: 60.7%) are preserved

## Usage

The main `STATE_PATTERNS` dictionary is automatically assembled from all state pattern files:

```python
from utils.state_patterns import STATE_PATTERNS, GENERAL_PATTERNS

# Access Kerala patterns
kerala_patterns = STATE_PATTERNS["Kerala"]

# Access Delhi patterns  
delhi_patterns = STATE_PATTERNS["Delhi"]

# Use general fallback patterns
general_patterns = GENERAL_PATTERNS
```

## Adding New States

To add a new state:

1. Create a new file: `new_state.py`
2. Define patterns: `NEW_STATE_PATTERNS = { ... }`
3. Import in `__init__.py`: `from .new_state import NEW_STATE_PATTERNS`
4. Add to STATE_PATTERNS dictionary: `"New State": NEW_STATE_PATTERNS`

## Pattern Performance

- **Kerala**: 88.7% success rate (9 fields achieving 90%+)
- **Delhi**: 60.7% success rate (advocates: 100%, case_number: 96.4%)
- **Gujarat**: 40.7% baseline (opportunity for enhancement)
- **Other States**: Baseline patterns ready for optimization

## File Dependencies

- All pattern files are imported by `__init__.py`
- `metadata_extractor.py` imports `STATE_PATTERNS` and `GENERAL_PATTERNS`
- No circular dependencies - clean import structure

## Validation

The reorganized structure has been tested and confirmed to work correctly with the main extraction system. All existing functionality is preserved while improving code maintainability and organization.
