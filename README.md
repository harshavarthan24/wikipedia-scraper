# Wikipedia Scraper

## Overview
The Wikipedia Scraper is a command-line tool that automates the extraction of structured data from Wikipedia articles based on user-specified keywords. It simplifies the process of gathering relevant information, making it an essential tool for researchers, students, and developers.

## Features
- **Automated Data Collection**: Fetches information from Wikipedia with minimal user effort.
- **Structured Data Output**: Stores extracted data in both JSON and CSV formats for easy analysis.
- **Comprehensive Extraction**: Retrieves article summaries, infobox data, main sections, and references.
- **Flexible and Scalable**: Works with any Wikipedia topic, making it a versatile research tool.
- **User-Friendly Output**: Organizes data in an `output` folder for easy access and management.

## Installation
To use the Wikipedia Scraper, install the required dependencies:
```bash
pip install requests beautifulsoup4 pandas
```

## Usage
Run the scraper from the command line, specifying keywords as arguments:
```bash
python wikipedia_scraper.py --keywords "Artificial Intelligence" "Machine Learning"
```

### Example Workflow
#### Scenario: Researching Renewable Energy Sources
A researcher wants to gather information on different renewable energy sources. They run:
```bash
python wikipedia_scraper.py --keywords "Solar Power" "Wind Energy" "Hydroelectric" "Geothermal Energy"
```
The script will:
1. Search Wikipedia for each keyword.
2. Extract relevant article content.
3. Save detailed information in individual JSON files.
4. Create a summary CSV file with key details.

The extracted data will be stored in the `output` directory.

## Output Files
- **JSON files**: Each keyword has a dedicated JSON file with comprehensive article data.
- **CSV summary**: A consolidated file containing key details from all searches.

## Why Use This Scraper?
- **Saves Time**: Automates information retrieval that would take hours manually.
- **Structured Data**: Converts unstructured Wikipedia content into structured, analyzable formats.
- **Enhances Research**: Ideal for researchers, students, and developers working with large amounts of textual data.

## Future Enhancements
- **Multi-language Support**: Extend support to Wikipedia articles in different languages.
- **Custom Output Formatting**: Enable users to specify additional output formats.
- **GUI Version**: Develop a graphical interface for easier usability.

## Contributing
Contributions are welcome! Feel free to fork this repository, submit issues, or create pull requests.

## License
This project is licensed under the MIT License.

---
Feel free to suggest improvements or request additional features!

