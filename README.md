# json2csv

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/json2csv/pulls)

A tiny, practical command-line tool to convert JSON into CSV.

- ✅ Supports JSON array, single object, or NDJSON
- ✅ Flattens nested objects (e.g. `profile.email`)
- ✅ Flexible list handling (`join` or `index`)
- ✅ Works with stdin/stdout and multiple files
- ✅ Custom delimiters, field selection, and no-header option

## 🚀 Installation

### Direct Download
```bash
git clone https://github.com/yourusername/json2csv.git
cd json2csv
chmod +x json2csv.py
```

## 📖 Usage

### Basic Usage

Convert a JSON file to CSV:
```bash
python json2csv.py data.json
```

Convert from stdin:
```bash
cat data.json | python json2csv.py
```

### Command Line Options

```
Usage: python json2csv.py [OPTIONS] [FILE]

Options:
  -d, --delimiter TEXT       CSV delimiter (default: ,)
  -f, --fields TEXT          Comma-separated list of fields to include
  -n, --no-header            Don't output CSV header
  -l, --list-handling TEXT   How to handle lists: 'join' or 'index' (default: join)
  -j, --join-string TEXT     String to join list items with (default: |)
  -h, --help                 Show this help message
  -v, --version              Show version

Arguments:
  FILE                       JSON file to convert (reads from stdin if not provided)
```

### Examples

#### 1. Basic JSON Array
**Input (data.json):**
```json
[
  {"name": "Alice", "age": 30, "city": "New York"},
  {"name": "Bob", "age": 25, "city": "San Francisco"}
]
```

**Command:**
```bash
python json2csv.py data.json
```

**Output:**
```csv
name,age,city
Alice,30,New York
Bob,25,San Francisco
```

#### 2. Nested Objects (Flattened)
**Input (nested.json):**
```json
[
  {
    "name": "Alice",
    "profile": {
      "email": "alice@example.com",
      "social": {
        "twitter": "@alice",
        "github": "alice-dev"
      }
    }
  }
]
```

**Command:**
```bash
python json2csv.py nested.json
```

**Output:**
```csv
name,profile.email,profile.social.twitter,profile.social.github
Alice,alice@example.com,@alice,alice-dev
```

#### 3. Lists with Join Handling
**Input (lists.json):**
```json
[
  {
    "name": "Alice",
    "hobbies": ["reading", "coding", "gaming"],
    "tags": ["developer", "python"]
  }
]
```

**Command:**
```bash
python json2csv.py lists.json
```

**Output:**
```csv
name,hobbies,tags
Alice,reading|coding|gaming,developer|python
```

#### 4. Lists with Index Handling
**Command:**
```bash
python json2csv.py --list-handling index lists.json
```

**Output:**
```csv
name,hobbies.0,hobbies.1,hobbies.2,tags.0,tags.1
Alice,reading,coding,gaming,developer,python
```

#### 5. Custom Delimiter and Field Selection
**Command:**
```bash
python json2csv.py --delimiter ";" --fields "name,profile.email" nested.json
```

**Output:**
```csv
name;profile.email
Alice;alice@example.com
```

#### 6. No Header
**Command:**
```bash
python json2csv.py --no-header data.json
```

**Output:**
```csv
Alice,30,New York
Bob,25,San Francisco
```

#### 7. NDJSON (Newline Delimited JSON)
**Input (data.ndjson):**
```ndjson
{"name": "Alice", "age": 30}
{"name": "Bob", "age": 25}
```

**Command:**
```bash
python json2csv.py data.ndjson
```

**Output:**
```csv
name,age
Alice,30
Bob,25
```

#### 8. Multiple Files
**Command:**
```bash
python json2csv.py file1.json file2.json > combined.csv
```

#### 9. Pipe from Other Commands
**Command:**
```bash
curl -s https://api.example.com/data | python json2csv.py > output.csv
```

## 🔧 Advanced Features

### Field Selection
Use the `--fields` option to select specific fields:
```bash
python json2csv.py --fields "name,age,city" data.json
```

### Custom List Joining
Change how list items are joined:
```bash
python json2csv.py --join-string ";" lists.json
```

### Nested Field Access
Access deeply nested fields using dot notation:
```bash
python json2csv.py --fields "user.profile.settings.theme" data.json
```

## 📋 Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## 🧪 Testing

Run the included tests:
```bash
python -m pytest tests/
```

Or run a quick test:
```bash
python json2csv.py examples/sample.json
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/yourusername/json2csv.git
cd json2csv
python json2csv.py --help
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by various JSON to CSV conversion tools
- Built with Python's standard library for maximum portability

## 🐛 Troubleshooting

### Common Issues

1. **"Permission denied" error on Linux/Mac**
   ```bash
   chmod +x json2csv.py
   ```

2. **"Module not found" error**
   - Ensure you're using Python 3.7+
   - Check that the file path is correct

3. **Empty output**
   - Verify your JSON is valid
   - Check if the JSON contains the expected structure

### Getting Help

- Open an issue on GitHub
- Check the examples in the `examples/` directory
- Run `python json2csv.py --help` for usage information
