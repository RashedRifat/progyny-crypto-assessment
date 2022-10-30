# Overview

* **Author:** Rashed Rifat

This document details some important design choices and instructions by the author. Please refer to the appropriate section for the relevant discussion.

## Running The Application

* Executing The Application
  * Copy the `.env.example` file to `.env`
    * Note that, by default, the application uses an SQLite DB called `crypto.db`. You may modify this behavior by changing the `DB_HOST` variable within your `.env` file.
  * Start the docker container (`make init`)
  * Run the program with `python app.py`
* Executing The Tests
  * Copy the `.env.example` file to `.env`
  * Start the docker container (`make init`)
  * Navigate to the testing directory (`cd testing`)
  * Run the tests with `python test_logic.py`
* Scheduling the Application via Cronjobs
  * Please add the content from `scheduling\scheduler.bash` to a cronjob file.
  * For instructions to do so, please refer to [this tutorial](https://phoenixnap.com/kb/set-up-cron-job-linux), section "Setting Up a Cron Job."

## Library Choices

This section will beefily discuss some of the libraries chosen for this project and will include a brief primer as to why.

* Database: SQLite
  * SQLite was chosen as the DB API due to its ease of use and flexibility for a relatively simple application.
* ORM: SQLAlchemy
  * SQLAlchemy was chosen as the ORM due to its extensive support and ease of use with the SQLite library.

## Architectural Choices  

This section brefily discusses the different modules of the project. This project was constructed to be scaled up if possible and thus has multiple modules, each with thier own function.

* core
  * This module features some helper functions that transform data, format objects into strings and calculate various values. This is where some of the logic of the application has been abstracted to.
* custom_logging
  * This module sets up the logger for the project. A custom logger was required to output information to both the file as well as the console.
* docs
  * This module contains the documentation for this project. A meta module discussing the overall assessment and improvements.
* models
  * This module contains the models for the database as well as the logic to setup the database.
* scheduling
  * This module contains the information to schedule this application to run once every hour. More information as to scheduling can be found below.
* storage/logs
  * Output directory for the logs for this project.
  * Note that logs are ignored by default for the GitHub repository.
* testing
  * This module contains the tests for this project.

## Design Choices

This section will briefly discuss some design choices. This is **not** an exhaustive list and only features some important notes for the reader to consider.

* Scheduling
  * Scheduling this application to run every hour is done through a cronjob - this is a relatively simple script that stores some data (and submits an order to purchase several assets) into a database. This application does not need to run within the background as a daemon and thus can be executed once every hour through a cronjob.
* Database Design
  * The database architecture is composed of two tables, a transactions table and a portfolio table.
    * The transactions table stores records of the top three cryptocurrencies by market cap per hour and if they were chosen to be purchased.
    * The portfolio table contains records of the current distribution of a hypothetical cryptocurrency wallet.
  * The transactions table was designed to store both records of the top three cryptocurrencies by market cap **and** whether or not they were purchased as it would be redundant to store the information about a cryptocurrency and its trading history into two separate tables.
    * Reduce complexity in storing information when not necessary. Within this design, information regarding the trade and its information are available at a glance.
  * The portfolio table was designed to store the positions so as to keep a constantly updated record of current balances.
    * Avoid performance overhead incurred if we were to calculate the overall portfolio from the transaction history.
    * Does not store the current price of any asset/coin as prices vary widely day to day and thus would render the table outdated.
* Additional Endpoints
  * Note that the author added an extra endpoint that retrieves the current price of a coin in USD.
  * This endpoint was added so as to provide updated information for the portfolio, specifically as to the percent gain or loss of the underlying coin.
  * An additional endpoint was required as relying on the provided endpoint to get the top 3 cryptocurrencies by market cap does not guarantee that there will be an updated price for all coins within the portfolio.
    * What if the market cap of these coins change? Then, our portfolio would hold a coin that is no longer within the top 3 coins by market cap and we would not be able to calculate the percent gain or loss just by depending on the provided endpoint.
    * What if the portfolio contains more than 3 coins? Then the provided endpoint is not sufficient as we need data for those cryptocurrencies themselves.
* Storing prices as decimal 
  * When researching the best way to store prices within a SQL database, due to the rounding errors associated with floats, prices are currently stored as a decimal with a precision of 7 digits (due to the precision offered by the API results, in reference to Tether).
    * This design was chosen to keep things simple and easy. There are better designs, as discussed below.
    * Additionally, since we are only storing coins held (which are integers due to the design of the problem), this schema is suffcient. 
  * This was a design noted by the author - there are possibly better designs such as storing the cents as an integer. Deciding how to store prices within the database is a discussion that depends on the use case of the application and the overall fault tolerance of the application. A further discussion would be required to determine the best possible way forward. 

## Improvements

This section describes some of the improvements to the logic and functionality of this application

### Business Logic Improvements 

* Using additional metrics to generate a buy signal 
  * Currently, this application relies on a rolling 10-day average to generate buy signals for this application. This is a relatively simplistic algorithm and has much room for improvement. Considering other factors such as the moving average of volume, current trend, the relative strength of the coin, etc.
    * One simple improvement would be consider a moving 30- or 60-day average instead of just 10 days. Considering price improvement with more than one simply moving average would also add more complexity to the overall design. 
* Generating sell signals 
  * Currently the project does not generate any sell signals - it passively purchases coins once below a certain threshold. While strategy may be profitable for a long-term investor but in terms of trading, is insufficient as it does not generate any profit or protect aganist any sudden drops in price.
  * Consider adding a criteria to sell a coin to generate profit. One such strategy would be to consider adding a minimum or rolling profit margin for each coin. that a coin has suddenly risen 10-50% in value. If this profit margin is acceptable, sell all or a portion of the current portfolio to lock in profits. 
    * A rolling profit margin criteria could be to sell 50% of the position at a 10% profit, 25% at a 25% profit margin, etc...
  * Consider adding a sell signal to avoid any massive losses (in effect, a price floor). This would require selling (or closing) a position once a certain amount of losses have been incurred, to protect against any rapidly falling price action. 
* Monitoring the markets more frequently 
  * The cryptocurrency markets are prone to moving quickly. Simply monitoring the price once every hour is slow compared to the pace of the market. Consider monitoring your portfolio once every minute or an even shorter interval, if possible or necessary. 

### Code Improvements  

* Running the application as long-running process/daemon 
  * Currently, the application is set to run once every hour, as per the requirements. Due to this requirement, a cron job is sufficient to run this application as the increased overhead of running a long-standing instance is not justified. 
  * However, it would be better if this project was instead developed into a long running process/service (such as a Flask API that runs in the background), which also queries the API at a shorter interval.
    * One great resource/way to do this would be via the `APScheduler` library. The documentation is [linked here](https://pypi.org/project/APScheduler/3.3.1/). 
* Including custom logging levels
  * Currently the application will log everything to the console and to a singular log file, including actions such as inserting transactions into the table, displaying the portfolio, etc. This can get quite messy and it might be better to filter out some of these messages to different log files. 
  * That is to say, a root logger would log everything within the application while also logging some specific actions (displaying trades, portfolio, etc) into separate directories.
* Database redesign 
  * The current database design is quite simple and simply features two tables to comply with the system requirements. If some of the improvements within the business logic section were to be implements, the database would have to wholly redesigned.
  * One simple example of this might be include a compound primary key for the transactions tables, composed of both an auto-incrementing sequence and a coin_id, where the coin_id is also a foreign key to the portfolio table. This design would allow you to create a relationship between a position within the portfolio and the trades that led to the position. 
    * This could allow you to, for example, display all of the trades for a certain position. 
    * This is also easily done within the current schema but this re-design makes it more explicit 