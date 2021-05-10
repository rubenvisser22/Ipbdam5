from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
import csv
def getData():
    # Test de connectie
    Cryptocurrencies().find_crypto_pairs()

    # Vind litecoin
    data = Cryptocurrencies(coin_search='LTC-EUR', extended_output=False).find_crypto_pairs()

    # Haal historische data op
    historicalData = HistoricalData('LTC-EUR', 3600, '2021-05-01-00-00', '2021-05-02-00-00').retrieve_data()
    historicalData.to_csv(
        r'C:\Users\ruben\OneDrive\Bureaublad\School huiswerk\Jaar 2\IPBDAM2\prijs2.csv')
    return historicalData

def main():
    getData()

if __name__ == "__main__":
    main()
