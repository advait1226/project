from django.test import TestCase
import numpy as np
# Create your tests here.
def nstep_option_price_volatility(request):

    s = 45
    k = 40
    r= 0.08
    v=0.25
    t=2
    n= 2

    delta_t = t/n
    u = np.exp(v* np.sqrt(delta_t))
    d = 1/u
    p = (np.exp(r*delta_t) - d) / (u - d)
    
    stock_prices = np.zeros(n+1)
    option_values = np.zeros(n+1)
    
    for i in range(n+1):
        stock_prices[i] = s * np.power(u, n-i) * np.power(d, i)
        option_values[i] = max(stock_prices[i] - k, 0)
    
    
    for j in range(n-1, -1, -1):
        for i in range(j+1): 
            option_values[i] = (p * option_values[i] + (1-p) * option_values[i+1]) * np.exp(-1*r*delta_t)
        
    
    
    option_price = option_values[0]

    print(option_price)

nstep_option_price_volatility(1)