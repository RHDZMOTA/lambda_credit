# -*- coding: utf-8 -*-

# future_value
futureValue = lambda capital, interest, periods: capital * (1 + interest) ** periods

# present_value 
presetValue = lambda capital, interest, periods: capital * (1 + interest) ** (-periods)

# annual interest rate
annualInterest = lambda initial_capital, end_capital, years: (end_capital / initial_capital) ** (1 / years) - 1

# equivalent annual interest rate

equivalentAnnualInterest = lambda rate, cap: (1 + rate / cap) ** cap - 1 

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
