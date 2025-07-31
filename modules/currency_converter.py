import requests
import json

class CurrencyConverter:
    def __init__(self):
        # Country to currency mapping
        self.country_currency_map = {
            'US': 'USD', 'United States': 'USD', 'USA': 'USD',
            'GB': 'GBP', 'United Kingdom': 'GBP', 'UK': 'GBP',
            'DE': 'EUR', 'Germany': 'EUR',
            'FR': 'EUR', 'France': 'EUR',
            'IT': 'EUR', 'Italy': 'EUR',
            'ES': 'EUR', 'Spain': 'EUR',
            'JP': 'JPY', 'Japan': 'JPY',
            'CN': 'CNY', 'China': 'CNY',
            'IN': 'INR', 'India': 'INR',
            'CA': 'CAD', 'Canada': 'CAD',
            'AU': 'AUD', 'Australia': 'AUD',
            'BR': 'BRL', 'Brazil': 'BRL',
            'MX': 'MXN', 'Mexico': 'MXN',
            'RU': 'RUB', 'Russia': 'RUB',
            'KR': 'KRW', 'South Korea': 'KRW',
            'SG': 'SGD', 'Singapore': 'SGD',
            'CH': 'CHF', 'Switzerland': 'CHF',
            'SE': 'SEK', 'Sweden': 'SEK',
            'NO': 'NOK', 'Norway': 'NOK',
            'DK': 'DKK', 'Denmark': 'DKK',
            'PL': 'PLN', 'Poland': 'PLN',
            'TR': 'TRY', 'Turkey': 'TRY',
            'ZA': 'ZAR', 'South Africa': 'ZAR',
            'NZ': 'NZD', 'New Zealand': 'NZD'
        }
        
        # Fallback exchange rates (static rates for demo purposes)
        # In production, you'd use a real-time API like exchangerate-api.com
        self.fallback_rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.0,
            'CNY': 6.45,
            'INR': 74.5,
            'CAD': 1.25,
            'AUD': 1.35,
            'BRL': 5.2,
            'MXN': 20.0,
            'RUB': 75.0,
            'KRW': 1180.0,
            'SGD': 1.35,
            'CHF': 0.92,
            'SEK': 8.5,
            'NOK': 8.8,
            'DKK': 6.3,
            'PLN': 3.9,
            'TRY': 8.5,
            'ZAR': 14.5,
            'NZD': 1.42
        }
    
    def get_currency_for_country(self, country):
        """Get currency code for a given country"""
        return self.country_currency_map.get(country.upper(), 'USD')
    
    def get_exchange_rate(self, from_currency, to_currency):
        """Get exchange rate between two currencies"""
        try:
            # Try to get real-time rates from a free API
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data['rates'].get(to_currency, 1.0)
            else:
                # Fallback to static rates
                return self._get_fallback_rate(from_currency, to_currency)
                
        except Exception:
            # Fallback to static rates
            return self._get_fallback_rate(from_currency, to_currency)
    
    def _get_fallback_rate(self, from_currency, to_currency):
        """Get exchange rate using fallback static rates"""
        if from_currency == to_currency:
            return 1.0
        
        from_rate = self.fallback_rates.get(from_currency, 1.0)
        to_rate = self.fallback_rates.get(to_currency, 1.0)
        
        # Convert to USD first, then to target currency
        usd_amount = 1.0 / from_rate
        return usd_amount * to_rate
    
    def convert_price(self, price, country, base_currency='USD'):
        """Convert price to local currency based on country"""
        target_currency = self.get_currency_for_country(country)
        
        if base_currency == target_currency:
            return {
                'amount': price,
                'currency': target_currency,
                'rate': 1.0
            }
        
        exchange_rate = self.get_exchange_rate(base_currency, target_currency)
        converted_amount = round(price * exchange_rate, 2)
        
        return {
            'amount': converted_amount,
            'currency': target_currency,
            'rate': exchange_rate
        }
    
    def get_supported_countries(self):
        """Get list of supported countries"""
        return list(self.country_currency_map.keys())
    
    def get_currency_symbol(self, currency_code):
        """Get currency symbol for display"""
        symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥',
            'CNY': '¥', 'INR': '₹', 'CAD': 'C$', 'AUD': 'A$',
            'BRL': 'R$', 'MXN': '$', 'RUB': '₽', 'KRW': '₩',
            'SGD': 'S$', 'CHF': 'CHF', 'SEK': 'kr', 'NOK': 'kr',
            'DKK': 'kr', 'PLN': 'zł', 'TRY': '₺', 'ZAR': 'R',
            'NZD': 'NZ$'
        }
        return symbols.get(currency_code, currency_code)
