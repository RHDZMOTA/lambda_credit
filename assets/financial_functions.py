# -*- coding: utf-8 -*-

# %% 
import numpy as np
from datetime import datetime, date

# %% 
def toDate(datetime_obj):
    '''toDate function
    Transforms a datetime object to date. 
    '''
    return date(datetime_obj.year, datetime_obj.month, datetime_obj.day)

# %% Basic financial functions

# future_value
futureValue = lambda capital, interest, periods: capital * (1 + interest) ** periods

# present_value 
presetValue = lambda capital, interest, periods: capital * (1 + interest) ** (-periods)

# annual interest rate
annualInterest = lambda initial_capital, end_capital, years: (end_capital / initial_capital) ** (1 / years) - 1

# %% Other financial functions 

# equivalent annual interest rate
'''equivalentAnnualInterest function
This function returns the equivalent annual interest rate with 1y capitalization
for a given interest rate (rate) with cap-capitalizations per year. 

---- inputs
rate: previous annual interest rate
cap: number of time the prev. rete capitalizes per year

--- outputs 
An equivalent annual rate that capitalizes 1 time per year.
'''
equivalentAnnualInterest = lambda rate, cap: (1 + rate / cap) ** cap - 1 

# equivalent rate 
'''equivalentRate function
This function returns an annual interest rate with new_cap-capitalizations per year given
a previous annual rate (rate) with cap-capitalizations per year

---- inputs 
rate:
cap:
new_cap:

---- outputs
...
'''
equivalentRate = lambda rate, cap, new_cap: new_cap * ((1 + rate / cap) ** (cap / new_cap) - 1)

# %% Risk Free Interest Rate (CETES)

def getRiskFreeRate():
    '''getRiskFreeRate function.
    description: This fuction returns the risk-free interest rate (cetes) for 28,91,182 days.
    
    ---- inputs
     
    
    ---- outputs
    
    
    '''
    
    # import libraries
    import urllib.request
    
    # open url to get source
    with urllib.request.urlopen('http://www.banxico.org.mx/SieInternet/'+
                                'consultarDirectorioInternetAction.do?a'+
                                'ccion=consultarCuadro&idCuadro=CF107&s'+
                                'ector=22&locale=es') as response:
        
        # read source and save as string 
        html_source = response.read().decode('latin-1')
    
    
    # identify target
    def getTarget(source):
        '''getTarget function
        description: function adapted to retrieve the value of cetes interest rate. 
        
        ---- inputs
        source: 
        
        ---- outputs
        position_index: 
        value: 
        
        '''
        
        tasa_de_rendimiento = source.find('Tasa de rendimiento')
        visibility_hidden   = 0
        
        for i in range(3):
            visibility_hidden += source[tasa_de_rendimiento:][visibility_hidden:].find('<span style="visibility:hidden">')+34
            
        position_index = tasa_de_rendimiento + visibility_hidden - 10 - 34
        value          = float(source[position_index:position_index+10].strip(' '))
        return position_index, value

    
    # get key,values and save in dictionary 
    cetes_dictionary = {}
    reference_index  = 0
    
    for i in [28, 91, 182]:
        html_source            = html_source[reference_index:]
        reference_index, value = getTarget(html_source)
        cetes_dictionary[i]    = value
    
    
    return cetes_dictionary

# %% Debt object

class debt:

    desc = 'Interest Rate Object'
    rate_options  = {360:'daily', 12:'1m', 6:'2m', 4:'3m', 3:'4m', 2:'6m', 1:'1y'}
    cap_options   = {'daily':360, '1m':12, '2m':6, '3m':4, '4m':3, '6m':2, '1y':1}
    cetes         = getRiskFreeRate()

    def __init__(self, initial_date, final_date,capital = 10000, rate = {'rate':0.01, 'cap':12}):
        
        self.initial_date   = toDate(datetime.strptime(initial_date, '%b %d %Y'))
        self.final_date     = toDate(datetime.strptime(final_date, '%b %d %Y'))
        self.actual_date    = toDate(datetime.now())
        self.capital = capital
        self.reference_rate = rate
        daily_rate = equivalentRate(rate['rate'], rate['cap'], 360)
        self.final_capital  = round(futureValue(capital, daily_rate / 360, (self.final_date - self.initial_date).days), 2)  
    
    def daysToGo(self, ref_date = None):
        '''
        '''
        if type(ref_date) == type(None):
            ref_date = self.actual_date
            
        return (self.final_date - ref_date).days

    def diffDates(self, date0, date1):
        date0 = toDate(datetime.strptime(date0, '%b %d %Y'))
        date1 = toDate(datetime.strptime(date1, '%b %d %Y'))
        return (date1-date0).days

    def discountRate(self, cap_desc):
        '''discountRate function
        Use discountRate function to get the discount interest rate for...
        '''
        
        # get capitalization frequency
        if type(cap_desc) == type(' '):
            aux = self.cap_options[cap_desc]
        elif type(cap_desc) == type(1):
            aux = cap_desc
        
        return equivalentRate(self.cetes[28]/100, 360 / 28, aux)
    
    def payDebt(self, pay_date = None):
        '''
        '''
        
        if type(pay_date) == type(None):
            pay_date = toDate(datetime.now())
        else:
            pay_date = toDate(datetime.strptime(pay_date, '%b %d %Y'))
            
        days = self.daysToGo(ref_date = pay_date)
        dr = self.discountRate('daily')
        return presetValue(self.final_capital,dr/360, days)
        
    def annualRate(self, cap_desc):
        '''calulate_equivalent method
        Use the reference_rate to calculate different equivalent rates. 
        Specif: daily, monthly, 2-months, 3-months, 4-months, 6-months, 1y, continuously
        '''
        
        # get capitalization frequency
        if type(cap_desc) == type(' '):
            aux = self.cap_options[cap_desc]
        elif type(cap_desc) == type(1):
            aux = cap_desc
            
        return equivalentRate(self.reference_rate['rate'], self.reference_rate['cap'], aux)
    
    def rate(self, cap_desc):
        '''rate method
        Use equivalentRate to generate a ready-to-use rate.
        '''
        
        # get capitalization frequency
        if type(cap_desc) == type(' '):
            aux = self.cap_options[cap_desc]
        elif type(cap_desc) == type(1):
            aux = cap_desc
        
        return self.annualRate(cap_desc) / aux
    
    
    def simulate(self, periods = 1, cap_desc = '1y'):
        '''simulate method
        add desc
        '''
        initial_capital = self.capital
        
        return futureValue(initial_capital, self.rate(cap_desc), periods)
    
    def simulateYears(self, years = 1, cap_desc = '1y'):
        '''simulate_years
        add desc
        '''
        initial_capital = self.capital
        return futureValue(initial_capital, self.rate(cap_desc), years * self.cap_options[cap_desc])

    def simulateMonths(self, months = 1, cap_desc = '1y'):
        '''simulate_months 
        add desc
        '''
        initial_capital = self.capital
        return self.simulateYears(initial_capital, months / 12, cap_desc)
    
    def riskFreeSpread(self, risk_free = 28):
        '''riskFreeSpread function
        '''
        
        # catch error 
        # TODO: check if risk_free is on cetes.keys()
        r  = equivalentAnnualInterest(self.reference_rate['rate'], self.reference_rate['cap'])
        rf = equivalentAnnualInterest(self.cetes[risk_free] / 100, risk_free / 360)
        return r - rf 
        
        
    
    
        

# %% 

# %% 

# %% 

# %% 