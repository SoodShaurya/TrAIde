# TrAIde

TrAIde is a comprehensive tool designed to analyze market sentiment and automate trading strategies. It leverages data from various sources, processes it, and provides actionable insights.

## Features

- **Sentiment Analysis**: Analyze market sentiment on each symbol using a a sentiment analysis model for market terms.
- **Automated Symbol Caching**: Automatically cache symbols daily using AlphaVantage API.
- **Continuous Streaming**: Real time data streaming and analysis.
- **MongoDB Data Storage**: Store all collected data for easy access.
- **API Endpoints**: Connects to [`traide-web`](https://github.com/SoodShaurya/traide-web) for seamless integration.
  
## Installation

1. Clone the repository:
    ```
    git clone https://github.com/soodshaurya/traide.git
    cd traide
    ```

2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Configure the application:
    - Duplicate the configuration file `configtemplate.ini` and rename to `config.ini`.
    - Add API key, Reddit application information, and MongoDB port.

## Usage

1. Start the application:
    ```
    python main.py
    ```

2. Access the API endpoints as documented in `api.py`.

## Configuration

- **MongoDB**: Ensure MongoDB is running on a non-default port (NOT 27017). Update the configuration in `config.ini`.
- **Logging**: Logs are stored in the `logs` directory and are printed to the terminal. Check the latest logs for any issues.

## Development

### TODO

- Write an algorithm to make a decision to sell/buy and how many to sell/buy.
  - Use stock trend for day, week, and month.
  - Use average sentiment for day and week.
  - Tweak weight values.

- Implement a weightage system for more influential people and higher comment scores.
- Implement scraping from facebook groups.
- Implement scraping of stocks by name in addition to symbol.

#### Low Priority

- Write a model for sentiment analysis dedicated to market terms.

### Completed

- Everything before we had a TODO.
- Wrote a timer.
- Updated sub-list and distilbert.
- Streaming rewrite.
- Wrote a script to run continuously.
- API endpoint to connect to `traide-web`.
- Wrote an automated symbol caching system (every day right now).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.