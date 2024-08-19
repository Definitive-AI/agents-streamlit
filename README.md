# Definitive AI User Interface

This project is the UI for Definitive AI devin for AI Agents.

## Setup

### Environment Variables (.env file)

To run this project, you need to edit the `.env` file in the root directory with the following variables:

```
Def_API_KEY = your_api_key_here
ANTHROPIC_API_KEY = your_anthropic_key_here
Def_Server = the_server_url_here
```

Replace the placeholder values with your actual API keys and database URL.

### Streamlit Secrets (secrets.toml file)

For Streamlit-specific secrets, create a `secrets.toml` file in the `.streamlit` directory with the following content:

```toml
[api_keys]
Def_API_KEY = your_api_key_here
ANTHROPIC_API_KEY = your_anthropic_key_here
Def_Server = the_server_url_here
```

Replace the placeholder values with your actual API keys and server URL.

## Installation

1. Clone this repository:
   ```
   git clone -b local https://github.com/Definitive-AI/agents-streamlit.git
   ```
2. Navigate to the project directory:
   ```
   cd your-repo-name
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have set up the `.env` and `secrets.toml` files as described in the Setup section.
2. Run the app:
   ```
   python start.py
   ```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
