([https://imgur.com/a/oVR0MtY.png])
# first_aid_voice 
The project aims to develop an AI-driven voice-assisted first aid and medical condition detection system to provide real-time rescue techniques to bystanders during emergencies.
This project demonstrates the implementation of speech-to-text and text-to-speech functionality using Python and Google Cloud Text-to-Speech API. It also includes integration with Intel OneAPI for optimized execution on Intel hardware.

## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Intel OneAPI Integration](#intel-oneapi-integration)
- [Code Overview](#code-overview)
- [Usage](#usage)
- [Demo](#demo)
- [Challenges and Solutions](#challenges-and-solutions)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project focuses on converting speech to text and vice versa. It uses the Google Cloud Text-to-Speech API to generate speech from text and the SpeechRecognition library for speech-to-text conversion. The implementation also integrates Intel OneAPI for enhanced performance on Intel architectures.

## Technologies Used

- Python
- Google Cloud Text-to-Speech API
- SpeechRecognition library
- JSON for intents management
- Intel OneAPI for performance optimization

## Intel OneAPI Integration

The project leverages Intel OneAPI to optimize code execution on Intel hardware. Environment variables are set using `os.environ` to configure OneAPI options, enhancing the performance of the speech-to-text and text-to-speech processes.

## Code Overview

The code is organized as follows:

- Importing necessary libraries and setting environment variables
- Loading predefined intents from a JSON file
- Implementing speech recognition and intent matching
- Utilizing Google Cloud Text-to-Speech API for generating speech

## Usage

1. Install required Python libraries:

2. Clone this repository:

3. Replace `json_key_path` with your Google Cloud service account key path in the code.

4. Run the script:

## Demo

A step-by-step demonstration of the project's functionality can be found in the [Demo](/Demo) directory. Screenshots and examples are provided.

## Challenges and Solutions

- Challenge: Matching speech input with predefined intents.
Solution: Utilizing pattern matching and keyword search for accurate intent identification.

- Challenge: Integrating with Intel OneAPI.
Solution: Setting appropriate environment variables to leverage OneAPI's performance benefits.

## Future Enhancements

- Implement more advanced intent matching techniques.
- Extend support for multiple languages and accents.
- Enhance error handling and user feedback.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
