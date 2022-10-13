

get_test_report = '''
## All test cases were successful, and production is now ready. 
[/report](/report)
'''

get_countries = '''
## This endpoint returns a listing with all the available countries from where stocks can be retrieved
use *&sortby=asce* (default) to ascend in order and use *&sortby=desc* to descend in order.

[/countries](/countries)
'''

get_stock = '''
## This endpoint retrieves all the stock data by country.

The country name should be supplied as a query parameter.

Example:-

[/stock?country=india](/stock?country=india)
'''
get_active_countries = '''
## This endpoint retrieves countries where a particular stock asset is active.

The stock asset symbol name should be supplied as a path variable.

Example:-

[/activecountries/ba](/activecountries/ba)

_Note: **ba** is the symbol name of Boeing._
'''

get_profile = '''
## This endpoint retrieves the company profile of a stock company

Some stock assets are active in many countries.As a result,must provide both the stock asset name(symbol) and the country name as path variables.

Example :-

[/profile/ba/united states](/profile/ba/united%20states)

_Note:Sometimes (rarely) , if stock and country are available but details are not found, The API will then respond with a **500** status code._
'''

get_summary = '''
## This endpoint retrieves the financial summary of the introduced stock (by symbol) from the introduced country.

Some stock assets are active in many countries.As a result,must provide both the stock asset name(symbol) and the country name as path variables.

[/summary/ba/united states](/summary/ba/united%20states)

_Note:Sometimes (rarely) , if stock and country are available but details are not found, The API will then respond with a **500** status code._
'''

get_info = '''
## This endpoint retrieves fundamental financial information from the specified stock.

Some stock assets are active in many countries.As a result,must provide both the stock asset name(symbol) and the country name as path variables.

[/info/ba/united states](/info/ba/united%20states)

_Note:Sometimes (rarely) , if stock and country are available but details are not found, The API will then respond with a **500** status code._
'''

get_ohlcv = '''
## This endpoint retrieves recent historical data from the introduced stock.

Some stock assets are active in many countries.As a result,must provide both the stock asset name(symbol) and the country name as path variables.

[/ohlcv/ba/united states](/ohlcv/ba/united%20states)

_Note:Sometimes, if stock and country are available but details are not found, The API will then respond with a **500** status code._

'''

get_overview = '''
## This endpoint retrieves an overview containing all the real time data available for the main stocks from a country, such as the names, symbols, current value, etc. 

The country name should be supplied as a path variable.

[/overview/united states](/overview/united%20states)

_Note:Sometimes (rarely) , if stock and country are available but details are not found, The API will then respond with a **500** status code._

'''