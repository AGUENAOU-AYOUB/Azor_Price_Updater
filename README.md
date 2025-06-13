# Azor Price Updater Webapp

This repository contains tools to update Shopify variant prices and now includes a small web application to run them more easily.

## Running the Web Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your Shopify credentials. Add login credentials:
   ```
   ADMIN_USERNAME=youruser
   ADMIN_PASSWORD=yourpass
   SECRET_KEY=random-string
   ```
3. Start the server:
   ```bash
   python run_webapp.py
   ```
4. Visit `http://localhost:5000` and log in with the credentials above.

## Using the Updaters

- **Percentage Updater** adjusts prices by a percentage and uses `project-root/scripts/update_prices_shopify.py`. Enter the desired percentage and monitor the real-time log while the script runs.
- **Variant Updater** runs `tempo solution/update_prices.py` which updates prices using predefined surcharges. Click the run button and watch the log.

The output from each script is streamed live to your browser so you can follow progress.
