#!/usr/bin/env python
# coding: utf-8

# <h3>Preface</h3>
# In this notebook I will be reviewing the daily ETF price data quality of the <a href="https://pypi.org/project/yfinance/">yfinance module</a> which scrapes equity prices and info from <a href="https://uk.finance.yahoo.com/">Yahoo Finance</a>.<br>
# I am trying to find out if the data quality is of a sufficient standard so as to track live my daily ETF Portfolio performance to date on my personal blog.<br>
# Currently my investments since the 1st October 2019 are in the following Vanguard ETFs, <a href="https://www.vanguardinvestor.co.uk/investments/vanguard-ftse-emerging-markets-ucits-etf-usd-distributing">VFEM.L</a>, <a href="https://www.vanguardinvestor.co.uk/investments/vanguard-ftse-250-ucits-etf-gbp-distributing">VMID.L</a> and <a href="https://www.vanguardinvestor.co.uk/investments/vanguard-ftse-all-world-ucits-etf-usd-distributing">VWRL.L.</a><br> 
# These ETFs will be the focus of my investigation however if the pricing data proves reliable I may expand the scope later on to include other equities.

# In[1]:


import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# In[2]:


#Create Ticker objects for each ETF
VFEM = yf.Ticker('VFEM.L')
VWRL = yf.Ticker('VWRL.L')
VMID = yf.Ticker('VMID.L')


# In[3]:


#VFEM Initial Analysis
VFEM_hist = VFEM.history(period="max")
VFEM_hist.reset_index(inplace=True) #reset Date index to a column

print(VFEM_hist.columns)
print(VFEM_hist[['Date', 'Open', 'High', 'Low', 'Close']].head(5))
print("Min close price Value VFEM: ",VFEM_hist['Close'].min())
print("Max close price value VFEM:",VFEM_hist['Close'].max())
print("Mean close price value VFEM:",VFEM_hist['Close'].mean())
print("Median of close price value VFEM:",VFEM_hist['Close'].median())
print("Std dev. of close price value VFEM:",VFEM_hist['Close'].std())


# 
# It appears that there is a large std deviation in close prices for VFEM.L with prices ranging from 34.31 to 4657.0<br>
# Let's check to see if the same applies to VWRL.L and VMID.L
# 

# In[4]:


VWRL_hist = VWRL.history(period="max")
VWRL_hist.reset_index(inplace=True) #reset Date index to a column

print("Min close price Value VWRL: ",VWRL_hist['Close'].min())
print("Max close price value VWRL:",VWRL_hist['Close'].max())
print("Median of close price value VWRL:",VWRL_hist['Close'].median())
print("Std dev. of close price value VWRL:",VWRL_hist['Close'].std())


# In[5]:


VMID_hist = VMID.history(period="max")
VMID_hist.reset_index(inplace=True) #reset Date index to a column

print("Min close price Value VMID: ",VMID_hist['Close'].min())
print("Max close price value VMID:",VMID_hist['Close'].max())
print("Median of close price value VMID:",VMID_hist['Close'].median())
print("Std dev. of close price value VMID:",VMID_hist['Close'].std())


# <h3>Initial analysis and thoughts</h3>
# The same large std deviation also seems to apply to VMID.L and VWRL.L.<br> It appears the yahoo pricing data for these Vanguard ETFs may be flipping between Major and Minor Currency (GBP and GBX), so the close prices are flipping by a factor of 100.<br>
# The Median Prices for VFEM and VWRL suggests that these ETFs are primarily priced in GBP, where as the Median of VWRL suggests that it is primarily priced in the Minor Currency GBX.<br>
# The KDE plot for each ETF should help confirm this.

# In[6]:


get_ipython().run_line_magic('matplotlib', 'inline')

price_history=[[VFEM_hist,'VFEM'],[VWRL_hist,'VWRL'],[VMID_hist,'VMID']]

fig, axes = plt.subplots(nrows=3, ncols=2)

for i in range(0,len(price_history)):
    prices = price_history[i][0]
    label = price_history[i][1]

    prices['Close'].plot.kde(ax=axes[i,0],figsize=(10,10))
    axes[i,0].set_title(label+" Close Prices KDE")
    axes[i,0].set_xlabel("Close Price")

    try:
        prices[prices['Close'] < prices['Close'].std()]['Close'].plot.kde(ax=axes[i, 1])
        axes[i, 1].set_title(label + " Filtered Major Close Prices KDE")
        axes[i, 1].set_xlabel("Close Price")
    except:
        print('None or less than 2 prices available for Close < std-dev graph in '+label)

plt.subplots_adjust(hspace=1)
plt.show()


# <h3>KDE Plot Analysis</h3>
# The KDE plots confirm that VFEM and VWRL have the bulk of their prices listed in the major currency GBP
# and VMID.L has the bulk of its prices listed in the minor currency GBX.<br>
# 
# Next job is to normalise the prices for each ETF to the Major Currency GBP; this means dividing almost all of VMIDs prices by a factor of 100 and just the largest values in VFEM and VWRL.

# In[7]:


#Normalise the prices using the STD DEV as a filter
VFEM_hist['Close'] = VFEM_hist['Close'].apply(lambda x: x/100 if x>VFEM_hist['Close'].std() else x)
VWRL_hist['Close'] = VWRL_hist['Close'].apply(lambda x: x/100 if x>VWRL_hist['Close'].std() else x)
VMID_hist['Close'] = VMID_hist['Close'].apply(lambda x: x/100 if x>VMID_hist['Close'].std() else x)

fig, axes = plt.subplots(nrows=3, ncols=1)
price_history=[[VFEM_hist,'VFEM'],[VWRL_hist,'VWRL'],[VMID_hist,'VMID']]

for i in range(0,len(price_history)):
    price_history[i][0]['Close'].plot.kde(ax=axes[i],figsize=(10,10))
    axes[i].set_title(price_history[i][1]+" Close Prices KDE")
    axes[i].set_xlabel("Close Price")

plt.subplots_adjust(hspace=1)
plt.show()


# Now the prices have been normalised to GBP we can compare the daily return and cumluative return of each ETF.

# In[8]:


VFEM_hist['DailyReturn'] = VFEM_hist['Close'].pct_change() * 100
VWRL_hist['DailyReturn'] = VWRL_hist['Close'].pct_change() * 100
VMID_hist['DailyReturn'] = VMID_hist['Close'].pct_change() * 100


# In[9]:


fig, axes = plt.subplots(nrows=3, ncols=1)

price_history=[[VFEM_hist,'VFEM'],[VWRL_hist,'VWRL'],[VMID_hist,'VMID']]

for i in range(0,len(price_history)):
    price_history[i][0].set_index('Date')['DailyReturn'].plot(ax=axes[i],figsize=(10,10))
    axes[i].set_title(price_history[i][1]+" Daily Return")
    axes[i].set_xlabel("Date")
    axes[i].set_ylabel("% Return")

plt.subplots_adjust(hspace=1)
plt.show()


# There is some suspiciously large daily changes in VWRL and VFEM which suggests there may be some poor close price records, but the data for the VMID looks ok with no large spikes in the daily change.

# In[10]:


VFEM_hist['CumulativeReturn'] = VFEM_hist['DailyReturn'].cumsum()
VWRL_hist['CumulativeReturn'] = VWRL_hist['DailyReturn'].cumsum()
VMID_hist['CumulativeReturn'] = VMID_hist['DailyReturn'].cumsum()


# In[11]:


fig, axes = plt.subplots(nrows=3, ncols=1)

price_history=[[VFEM_hist,'VFEM'],[VWRL_hist,'VWRL'],[VMID_hist,'VMID']]

for i in range(0,len(price_history)):
    price_history[i][0].set_index('Date')['CumulativeReturn'].plot(ax=axes[i],figsize=(10,10))
    axes[i].set_title(price_history[i][1]+" Cumulative Return")
    axes[i].set_xlabel("Date")
    axes[i].set_ylabel("% Return")

plt.subplots_adjust(hspace=1)
plt.show()


# <h4>Daily and Cumulative Return Analysis</h4>
# There is some suspiciously large changes in the dalily return for VWRL and VFEM which suggests there may be some poor close price records, but the data for the VMID looks ok with no large spikes in the daily change.<br>
# Again the VMID Cumulative Return looks as expected, however the VWRL and VFEM cumulative return has some suspicously large jumps in returns for ETFs that track the All-World and Emerging Markets.<br>
# Most of the suspicous returns occur pre-2019 and as I only need the pricing data from Close 30th September 2019 onwards lets check its reliability starting from there.

# In[15]:


#Filter price records to just 30/09/2019 onwards.
VWRL_hist = VWRL_hist.loc[VWRL_hist['Date']>='2019-09-30']
VFEM_hist = VFEM_hist.loc[VFEM_hist['Date']>='2019-09-30']
VMID_hist = VMID_hist.loc[VMID_hist['Date']>='2019-09-30']

#Recalculate the daily returns
VWRL_hist['DailyReturn'] = VWRL_hist['Close'].pct_change() * 100
VFEM_hist['DailyReturn'] = VFEM_hist['Close'].pct_change() * 100
VMID_hist['DailyReturn'] = VMID_hist['Close'].pct_change() * 100

#Recalculate the cumulative returns
VWRL_hist['CumulativeReturn'] = VWRL_hist['DailyReturn'].cumsum()
VFEM_hist['CumulativeReturn'] = VFEM_hist['DailyReturn'].cumsum()
VMID_hist['CumulativeReturn'] = VMID_hist['DailyReturn'].cumsum()

#Replot daily returns
fig, axes = plt.subplots(nrows=3, ncols=1)

price_history=[[VFEM_hist,'VFEM'],[VWRL_hist,'VWRL'],[VMID_hist,'VMID']]

for i in range(0,len(price_history)):
    price_history[i][0].set_index('Date')['DailyReturn'].plot(ax=axes[i],figsize=(10,10))
    axes[i].set_title(price_history[i][1]+" Daily Return")
    axes[i].set_xlabel("Date")
    axes[i].set_ylabel("% Return")

plt.subplots_adjust(hspace=1)
plt.show()


# In[13]:


fig, axes = plt.subplots(nrows=3, ncols=1)

price_history=[[VFEM_hist,'VFEM'],[VWRL_hist,'VWRL'],[VMID_hist,'VMID']]

for i in range(0,len(price_history)):
    price_history[i][0].set_index('Date')['CumulativeReturn'].plot(ax=axes[i],figsize=(10,10))
    axes[i].set_title(price_history[i][1]+" Cumulative Return")
    axes[i].set_xlabel("Date")
    axes[i].set_ylabel("% Return")

plt.subplots_adjust(hspace=1)
plt.show()


# VFEM and VWRL look fine for this time period, however VMID appears to have periods of low or almost no change.<br>
# Best to check to see if there are changes in price occurring albeit very small or if the Yahoo Finance data has stagnant prices between the 1st of November and the 15th December.

# In[14]:


date_filter = (VMID_hist['Date']>='2019-10-15') & (VMID_hist['Date']<='2020-01-04')
print(VMID_hist[date_filter][['Date','Close','DailyReturn','CumulativeReturn']])


# Unfortunately it appears that Yahoo Finance is missing prices for VMID.L from the 1st November til the 2nd of January which explains the flat spot during this period.<br>

# <h3>Conclusion</h3>
# The yfinance python module running off of Yahoo Finance does not prove to be a promising data source for live and historical pricing of ETFs.<br>
# The switiching between major and minor currencies and periods of none or stagnant price data means it will not be a reliable enough source to track my ETF portfolio daily; however it may still prove useful as a secondary dataset for price comparison and/or validation.<br>
# My next step will be to investigate some of the other free and paid API equity pricing services such as <a href="https://www.quandl.com/">quandl</a> or the python library <a href="https://pandas-datareader.readthedocs.io/en/latest/">pandas-datareader</a>.
