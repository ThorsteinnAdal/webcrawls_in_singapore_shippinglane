from MaritimeConnectorSoup import get_IMO_numbers_from_file

nextValue = 6918560
imos = get_IMO_numbers_from_file('allIMOs.csv', start, stop)
print imos.index(nextValue)