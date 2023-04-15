from django.shortcuts import render

# Create your views here.
# import necessary modules

from django.http import HttpResponse
import numpy as np
from scipy.stats import norm

# define the function to calculate option pricing using a two-step binomial tree
q=0
y=3
def home_view(request):
    return render(request, 'home.html')

def result_view(request):
    if q==1 :
        option_value= two_step_option_price(request)
        if(y==0):
            return render(request, 'option_price1.html', {'call_option_value' : option_value})
        if(y==1):
            return render(request, 'option_price1.html', {'put_option_value' : option_value})
    if q==2 :
        option_value= nstep_option_price(request)
        if(y==0):
            return render(request, 'option_price2.html', {'call_option_value' : option_value})
        if(y==1):
            return render(request, 'option_price2.html', {'put_option_value' : option_value})
    if q==3 :
        option_value= nstep_option_price_volatility(request)
        if(y==0):
            return render(request, 'option_price3.html', {'call_option_value' : option_value})
        if(y==1):
            return render(request, 'option_price3.html', {'put_option_value' : option_value})
    if q==4 :
        option_value= black(request)
        
        if(y==0):
            return render(request, 'option_price4.html', {'call_option_value' : option_value})
        if(y==1):
            return render(request, 'option_price4.html', {'put_option_value' : option_value})
    

# --------------------------------------------------------------------------------------------------------------------------------------------------
def two_step_option_price(request):
    # , spot_price, strike_price, up_factor, down_factor, risk_free_rate, time_to_maturity):
    global y
    # convert inputs to floats
    spot_price = float((request.GET)['spot_price'])
    strike_price = float((request.GET)['strike_price'])
    up_factor = float((request.GET)['up_factor'])
    down_factor = float((request.GET)['down_factor'])
    risk_free_rate = float((request.GET)['risk_free_rate'])
    time_to_maturity = float((request.GET)['time_to_maturity'])
    option= (request.GET)['option']
    risk_free_rate/=100
    # calculate the time step
    time_step = time_to_maturity / 2
    
    # calculate the up and down probabilities
    # up_prob = (1 + risk_free_rate * time_step - down_factor) / (up_factor - down_factor)
    # down_prob = 1 - up_prob
    up_prob= (np.exp(risk_free_rate*time_step) - down_factor) / (up_factor - down_factor)
    down_prob = 1- up_prob
    # calculate the stock prices at each node
    stock_price_0 = spot_price
    stock_price_1_up = spot_price * up_factor
    stock_price_1_down = spot_price * down_factor
    stock_price_2_up_up = spot_price * up_factor * up_factor
    stock_price_2_up_down = spot_price * up_factor * down_factor
    stock_price_2_down_down = spot_price * down_factor * down_factor
    
    # calculate the option payoffs at each leaf node
    option_payoff_2_up_up = max(stock_price_2_up_up - strike_price, 0)
    option_payoff_2_up_down = max(stock_price_2_up_down - strike_price, 0)
    option_payoff_2_down_down = max(stock_price_2_down_down - strike_price, 0)
    
    # calculate the option values at each node
    option_value_1_up = (up_prob * option_payoff_2_up_up + down_prob * option_payoff_2_up_down) *np.exp(-1*risk_free_rate*time_step)
    option_value_1_down = (up_prob * option_payoff_2_up_down + down_prob * option_payoff_2_down_down) *np.exp(-1*risk_free_rate*time_step)
    option_value_0 = (up_prob * option_value_1_up + down_prob * option_value_1_down) *np.exp(-1*risk_free_rate*time_step)
    
    if(option=='call'):
        y=0
        return option_value_0 
    if(option=='put'):
         y=1
         put= option_value_0 + strike_price*(np.exp)(-risk_free_rate*time_to_maturity)-spot_price
         return put

# -----------------------------------------------------------------------------------------------------------------------------------------
# define the Django view function
def two_step_option_price_view(request):
    global q
    q=1
    return render(request, 'option_price1.html')

def n_step_option_price_view(request):
     global q
     q=2
     return render(request, 'option_price2.html')

def n_step_option_price_volatility_view(request):
    global q
    q=3
    return render(request, 'option_price3.html')
# ------------------------------------------------------------------------------------------------------------------------------------------

def nstep_option_price_volatility(request):
    global y
    s = float((request.GET)['spot_price'])
    k = float((request.GET)['strike_price'])
    r= float((request.GET)['risk_free_rate'])
    v=float((request.GET)['volatility'])
    t=float((request.GET)['time_to_maturity'])
    n= int((request.GET)['n'])
    option= (request.GET)['option']
    r/=100
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
    if(option=='call'):
        y=0
        return  option_price 
    if(option=='put'):
         y=1
         put= option_price + k*(np.exp)(-r*t)-s
         return put

# -----------------------------------------------------------------------------------------------------------------------------------------------

def nstep_option_price(request):
    global y
    s = float((request.GET)['spot_price'])
    k = float((request.GET)['strike_price'])
    r= float((request.GET)['risk_free_rate'])
    u= float((request.GET)['up_factor'])
    d= float((request.GET)['down_factor'])
    t=float((request.GET)['time_to_maturity'])
    n= int((request.GET)['n'])
    option= (request.GET)['option']
    r/=100
    delta_t = t/n
    
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
    if(option=='call'):
         y=0
         return option_price 
    if(option=='put'):
         y=1
         put= option_price + k*(np.exp)(-r*t)-s
         return put
# ------------------------------------------------------------------------------------------------------------------------------------------
def black(request):
    global y
    s = float((request.GET)['spot_price'])
    k = float((request.GET)['strike_price'])
    v = float((request.GET)['volatility'])
    r = float((request.GET)['risk_free_rate'])
    t = float((request.GET)['time_to_maturity'])
    option= (request.GET)['option']
    r/=100
    d1 = [(np.log)(s/k) + (r + v*v/2)*t]/(v*(np.sqrt)(t))
    d2= d1- v* (np.sqrt)(t)
    if(option=='call'):
        y=0
        call= (norm.cdf)(d1)*s - (norm.cdf)(d2)*k*(np.exp)(-1*r*t)
        return call
    if(option=='put'):
         y=1
         put= (norm.cdf)(-d2)*k*(np.exp)(-1*r*t) - (norm.cdf)(-d1)*s
         return put

def black_view(request):
    global q
    q=4
    return render(request, 'option_price4.html')