# DepenFusion: A Powerful Pentesting Tool for Detecting Dependency Confusion Vulnerabilities in Node.js

![DepenFusion Logo](https://user-images.githubusercontent.com/86640585/135770826-57d80968-675a-40fd-a156-b0b7fa08e972.png)

## What is DepenFusion?

DepenFusion is an advanced, multithreaded penetration testing (pentest) tool designed specifically to identify and analyze dependency confusion vulnerabilities in Node.js (npm) projects.

## Key Features:

- **Automated Vulnerability Detection:** DepenFusion is designed to automatically scan and identify dependency confusion vulnerabilities in Node.js projects.
- **User-Friendly Interface:** With an easy-to-use command-line interface, the tool simplifies the process of scanning subdomains/domains for potential vulnerabilities.
- **Smart URL Handling:** DepenFusion intelligently handles variations in URLs, ensuring smooth processing even with different formats.
- **Support for Multithreading:** The tool's multithreading capability allows for faster and more efficient scanning of multiple targets simultaneously.
- **Silent Mode and Verbose Options:** DepenFusion provides the flexibility of silent mode, which displays only useful results, or verbose mode for more detailed output.
- **Integration Possibilities:** DepenFusion can be easily integrated with other security tools to enhance vulnerability assessment capabilities.

## How to Use DepenFusion?

1. **Installation:**

   - Ensure you have both Git and Python 3 installed on your system.
   - Download the DepenFusion tool using the command:

     ```bash
     git clone github.com/benjamin-mauss/depenfusion
     ```

   - Change to the DepenFusion directory:

     ```bash
     cd depenfusion
     ```

   - Install the necessary dependencies:

     ```bash
     pip3 install -r requirements.txt
     ```
2. **Scanning Subdomains/Domains:**
  
    Use the following command to analyze subdomains/domains by providing them in the standard input (stdin):
    
    ```bash
    cat subdomains.txt | python3 ./main.py
    ```


3. **Advanced Usage:**

    DepenFusion offers several optional command-line arguments for advanced users. To view these options, run:
    
    ```bash
    python3 ./main.py --help
    ```
  
  
    These options include adjusting the number of concurrent threads, setting a timeout period, appending a custom string to URLs, enabling verbose mode, and more.

## How DepenFusion Works:

DepenFusion employs a systematic approach to identify dependency confusion vulnerabilities:

1. **Async Request and File Analysis:** The tool sends asynchronous requests to the target URLs, appending `package.json` and `package-lock.json` to each URL. It then checks if these files exist and are valid.
2. **Dependency Extraction:** If valid package files are found, DepenFusion extracts the dependencies listed within them.
3. **Validation through NPM API:** DepenFusion proceeds to verify the existence of the extracted dependencies by querying the npm API.

## Future Enhancements:

In the future, DepenFusion is expected to expand its capabilities by incorporating the following improvements:

- **Support for Additional Package Managers:** DepenFusion aims to include support for other popular package managers such as pip for Python and gem for Ruby.
- **GoLang Implementation:** Development is underway to create a GoLang version of DepenFusion, enabling even faster and more efficient scanning.

DepenFusion is a valuable tool for identifying and mitigating dependency confusion vulnerabilities in Node.js projects, enhancing the security posture of developers and organizations worldwide.
