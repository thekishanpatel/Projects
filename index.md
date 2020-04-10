# **Chennai Water Crisis**
**Skills**: Statistical Analysis, and Visualizations
(Plotly)

As climate change becomes more of a reality, we are bound to face its grave
repercussions world-wide. Climate change is most readily associated with the
melting of artic/antartic ice-caps, but it also leads to more antithetical
phenomena, such as droughts; an example of the latter can be seen in
***Chennai***, historically known as Madras--a major metropolis in southern
India. This exercise explores Chennai's 'water history' over nearly the last 20
years--including the recent shortages.

Chennai has four major reservoirs that
supply water for the populous. The combined capacity of these 4 reservoirs is
~11057 mcft. The four major reservoirs are: **Poondi**, **Cholavaram**, **Red-
Hills**, **Chembarambakkam**. Out of the four reservoirs, Cholavaram is the
smallest with a capacity of ~1000 mcft. The other reservoirs have an approximate
capacity of over 3000 mcft each. In total, the four reservoirs can hold a total
of ~11257 mcft of 1 liter. In this exercise, we evaulate the water-levels and
the rainfall-levels in these four reservoirs to evaluate the severity of the
crisis.

## **Question to Answer?**

Is this recent water shortage in Chennai a result of
cyclical changes, or is it an harbinger of a massive crisis to come?

# **Import the Libraries**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
from plotly import subplots as t
import plotly.graph_objs as go
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import (pairwise_tukeyhsd, MultiComparison);
```

# **Some Helper Functions**

```python
def trace (res, color, name):
    trace = go.Scatter(x = res.index[::-1], y = res.values[::-1], name = name, marker = dict(color = color));
    return trace
```

# **Import the Data**

```python
levels_path = '/content/chennai_reservoir_levels.csv'
rainfall_path = '/content/chennai_reservoir_rainfall.csv'

levels_data = pd.read_csv(levels_path);
levels_data.set_index("Date")
rain_data = pd.read_csv(rainfall_path)
rain_data.set_index("Date")
print("Reservoir Levels Data")
levels_data.head(10)
```

```python
print("Reservoir Rainfall Data")
rain_data.head(10)
```

```python
levels_data.info()
rain_data.info()
```

From the DataFrame summaries above, we can see that none of the cell-values are
empty or null. This assures us that we do not need to fill any gaps in data.

#
**Now Lets Take A Look at the Water Levels in the Reservoirs Over the Years**

## Convert to DateTime and then sort by Date

```python
levels_data['Date'] = pd.to_datetime(levels_data['Date'], format = '%d-%m-%Y')
rain_data['Date'] = pd.to_datetime(rain_data['Date'], format = '%d-%m-%Y')

levels_data.sort_values(by = 'Date', inplace = True)
rain_data.sort_values(by = 'Date', inplace = True)
```

## Extract Water Level Data for each Reservoir

```python
poondi = levels_data['POONDI']; poondi.index = levels_data['Date']
chola = levels_data['CHOLAVARAM']; chola.index = levels_data['Date']
red = levels_data['REDHILLS']; red.index = levels_data['Date']
chem = levels_data['CHEMBARAMBAKKAM']; chem.index = levels_data['Date']
```

## Make a Trace for each Reservoir (Water-Levels)

```python
poondit = trace(poondi, 'blue', 'Poondi');
cholat = trace(chola, 'orange', 'Cholavaram');
redt = trace(red, 'red', 'Redhills');
chemt = trace(chem, 'purple', ' Chembarambakkam');
```

## Plot The Water Levels

```python
levels = t.make_subplots(rows=1, cols=1);
# Reservoir Levels
levels.append_trace(poondit, 1, 1);
levels.append_trace(cholat, 1, 1);
levels.append_trace(redt, 1, 1);
levels.append_trace(chemt, 1, 1);
levels['layout'].update(title = "Water Levels (mcft) in Chennai's Four Main Reservoirs", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Water Level (mcft)'))
levels.show();
```

As is evident in the plot above, the water levels in the four reservoirs vary
annualy in a cyclic manner. This is  a seasonal phenomena, due to annual
patterns in the weather--i.e. The Monsoon. We can also see that the Cholavaram
reservoir historically has lower water levels than the other three; as
highlighted earlier, Cholavaram has approximately a third of the capacity as the
other reservoirs. The other three reservoirs follow similar patterns to one
another, but from the plot it seems as if the Redhills Reservoir isn't as
susceptible extremities like Poondi and Chembarambakkam. This can be seen in the
timespan from 2013 to 2016, where the water levels in all reservoirs varied
vastly, but the Redhill Reservoir didn't see as drastic of variations as the
others. The water-levels at Red-Hills stayed noticeably higher than the other
reservoirs. This could possibly be that the Red-Hills Reservoir might not be
used as readily as the others. 

We also see two periods where the water levels
in all reservoirs dropped significantly--between 2012 and 2016, and more
recently in 2017. South India had severe floods at the end of 2015, and this is
likely why the reservoirs reached their max-capacity in 2016. But these max
levels didn't hold for long and dropped drastically between 2016 and 2017. The
reservoirs have yet to go back to max-capacity following the drop. Decreased
water levels for a persistent amount of time can be alaraming, and may
foreshadow a looming water-crisis.

## Lets Look at the ***total*** reservoir water levels in Chennai

```python
'''Calculate the Total Water Level (sum of levels from each reservoir) on a Given Day'''
levels_data['Total'] = levels_data.apply(lambda row: row['POONDI'] + row['CHOLAVARAM'] + row['REDHILLS'] + row['CHEMBARAMBAKKAM'], axis = 1)
total = levels_data['Total']
total.index = levels_data["Date"];
totalt = trace(total, 'royalblue', 'Total');
tl ={'Date': total.index, 'total': total.values}
totall2 = pd.DataFrame(data = tl);
totall2['year'] = totall2['Date'].map(lambda x: x.strftime('%Y'));
totall2['modate'] = totall2['Date'].map(lambda x: x.strftime('%m-%d'));
yearwltot = totall2[totall2['modate']=='12-31']; # Will Use Later for calulation of Consumption/Water Loss

# Total Water Level Only
totfig = go.Figure();
totfig.add_trace(totalt);
totfig['layout'].update(title = "Total Water Level (mcft) in Chennai", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Water Level (mcft)'));
totfig.show();
```

Chennai is supplied water from all four reservoirs, and to see how dire the
situation is for the metropolis, it might be helpful to see the total water
levels in Chennai. The plot above shows the total water level (sum of the water
levels in the four reservoirs) on a given day. The trends seen in the earlier
graph are mimicked in this one. The water levels vary annually. We also see the
same two periods where the water level has decreased.

In June 2019, the water
level was nearly 0 mcft. Prior to that, it was 0 mcft in July 2017, and prior to
that it was 0 mcft back in October 2004. Other than the two peaks in early 2015
and 2016--the latter being a result of massive flooding--the total water level
since 2012 has been consistently lower than in the previous years; the water
shortage crisis in Chennai might have started earlier than 2017. 

Now lets
determine if these changes are due to a decrease in rainfall, or some other
factor. 

# **Now Lets Take a Look at the Rainfall levels in Chennai**

## Extract Rainfall Level Data for each Reservoir

```python
poondirf = rain_data['POONDI']; poondirf.index = rain_data['Date']
cholarf = rain_data['CHOLAVARAM']; cholarf.index = rain_data['Date']
redrf = rain_data['REDHILLS']; redrf.index = rain_data['Date']
chemrf = rain_data['CHEMBARAMBAKKAM']; chemrf.index = rain_data['Date']
```

## Make a Trace for each Reservoir (Rainfall)

```python
poondit = trace(poondirf, 'blue', 'Poondi');
cholat = trace(cholarf, 'orange', 'Cholavaram');
redt = trace(redrf, 'red', 'Redhills');
chemt = trace(chemrf, 'purple', ' Chembarambakkam');
```

## Plot the Rainfall Levels

```python
rf = t.make_subplots(rows=1, cols=1);
# Rainfall Levels
rf.append_trace(poondit, 1, 1);
rf.append_trace(cholat, 1, 1);
rf.append_trace(redt, 1, 1);
rf.append_trace(chemt, 1, 1);
rf['layout'].update(title = "Rainfall Levels (mm) in Chennai's Four Main Reservoirs", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Rainfall (mm)'))
rf.show();
```

The plot above shows the daily-rainfall in the four reservoirs from 2004 to
2019. Like the water-levels plot, the rainfall plot also has a cyclic pattern
that likely aligns with the monsoon season. From this plot it does not seem as
if rainfall in recent years is much lower than in previous years.

## Lets Look
at the ***total annual*** rainfall in Chennai, for a better understanding

```python
'''Calculate the Total Water Level (sum of levels from each reservoir) on a Given Day'''
rain_data['Total'] = rain_data.apply(lambda row: row['POONDI'] + row['CHOLAVARAM'] + row['REDHILLS'] + row['CHEMBARAMBAKKAM'], axis = 1)
rftotal = rain_data['Total']
rftotal.index = rain_data["Date"];
rftotal_annual = rftotal.resample('Y').sum()
rftl ={'Date': rftotal.index, 'total': rftotal.values}
totalrf2 = pd.DataFrame(data = rftl);
totalrf2['year'] = totalrf2['Date'].map(lambda x: x.strftime('%Y'));
totalrf2['modate'] = totalrf2['Date'].map(lambda x: x.strftime('%m-%d'));

yrt = {'Date':rftotal_annual.index, 'total': rftotal_annual.values};
yearraintot = pd.DataFrame(data = yrt);
yearraintot['year'] = yearraintot['Date'].map(lambda x: x.strftime('%Y'));
yearraintot['modate'] = yearraintot['Date'].map(lambda x: x.strftime('%m-%d'));
labels = []
for i in range(2004, 2020, 1): labels.append(i)
# Total Water Level Only
totrffig = go.Figure([go.Bar(x = rftotal_annual.index[::-1], y = rftotal_annual.values[::-1], text = labels[::-1], textposition = 'auto', marker_color = 'red', name = 'Total Annual Rain Fall')]);
totrffig['layout'].update(title = "Total Rainfall (mm) in Chennai", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Rainfall (mm)'));
totrffig.show();
```

### Lets rank years by annual rainfall amount

```python
yearraintot.sort_values(by = 'total', ascending = False, inplace = True)
yearraintot
```

From the total annual rainfall graph, we can see that rainfall amount from 2012
to 2014 was lower than in previous years. This could possibly explain why the
reservoir water levels between 2012-2016 were lower. 

You can see the drastic
surge in rainfall in 2015, which led to max capacity in reservoir water levels
in 2016. Subsequently, 2016 had a dismal year in terms of rainfall, which
explains the resulting drop in the reservoir water levels. 

This brings us to
2017. Rainfall in 2017 was normal; in fact, in the data-frame above where the
years are ranked according to annual rainfall amount, 2017 comes in at 7th
place. Despite this, the reservoir water levels failed to bounce back. This
indicates that there is another factor at play--possibly increased consumption.
Following 2017, rainfall in 2018 dropped to its lowest in the window of years we
are examining. This explains why the reservoir water levels continued to drop
and approach 0.

# **Lets Look At Water Usage or Consumption**

## Visualizing the Consumption

```python
consumption = levels_data
consumption.set_index('Date', inplace = True)
consumption = levels_data.diff(periods = -1) # Difference between Daily Water Levels
# Draw Traces
poondic = trace(consumption['POONDI'], 'blue', 'Poondi');
cholac = trace(consumption['CHOLAVARAM'], 'orange', 'Cholavaram');
redc = trace(consumption['REDHILLS'], 'red', 'Redhills');
chemc = trace(consumption['CHEMBARAMBAKKAM'], 'purple', ' Chembarambakkam');
# Plotting
con = t.make_subplots(rows=2, cols=2);
# Rainfall Levels
con.append_trace(poondic, 1, 1);
con.append_trace(cholac, 1, 2);
con.append_trace(redc, 2, 1);
con.append_trace(chemc, 2, 2);
con['layout'].update(title = "Daily Change in Water Usage Levels", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Water Level (mcft)'))
con.show();
```

(*A negative water level means water was added*) 

The daily changes in water
levels are normally 0 for all levels. This is probably because consumption from
the reservoir is dependent on the availability of ground water; if the latter is
limited or unavailable, only then the Chennai populous resorts to the
reservoirs. Looking at daily changes doesn't help us understand if consumption
has increased or decreased. Lets try to see change on an annual scale.

```python
consumption['Year'] = consumption.index
consumption['Year'] = consumption['Year'].dt.year
yearly_consumption = pd.DataFrame(consumption.groupby('Year')[['POONDI', 'CHOLAVARAM', 'REDHILLS', 'CHEMBARAMBAKKAM', 'Total']].sum())
```

## Let's look at annual water consumption

```python
# Draw Traces
poondicy = trace(yearly_consumption['POONDI'], 'blue', 'Poondi');
cholacy = trace(yearly_consumption['CHOLAVARAM'], 'orange', 'Cholavaram');
redcy = trace(yearly_consumption['REDHILLS'], 'red', 'Redhills');
chemcy = trace(yearly_consumption['CHEMBARAMBAKKAM'], 'purple', ' Chembarambakkam');
# Plotting
conyear = t.make_subplots(rows=2, cols=2);
# Rainfall Levels
conyear.append_trace(poondicy, 1, 1);
conyear.append_trace(cholacy, 1, 2);
conyear.append_trace(redcy, 2, 1);
conyear.append_trace(chemcy, 2, 2);
conyear['layout'].update(title = "Annual Change in Water Usage Levels", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Water Level (mcft)'))
conyear.show();
```

```python
totalcy = trace(yearly_consumption['Total'], 'royalblue', 'Total Water Usage')
totconfig = go.Figure();
totconfig.add_trace(totalcy);
totconfig['layout'].update(title = "Annual Total Water Usage", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Water Level (mcft)'));
totconfig.show();
```

# **Conclusion**
From the annual water usage levels above, we see that sharpest
increase in water usage was in 2016--which was a direct contributor to the
sharpest decrease in water levels between 2016 and 2017 we noticed earlier.
Despite this, we cannot claim that consumption has increased or decreased in
recent years when compared to previous years--that trend isn't evident.
However, from the rainfall plots we do know that rainfall in recent years--
really since 2012, apart from 2015--has been lower than in the previous
years(2004 - 2012). With rainfall being lower and consumption being consistent,
a decrease in water levels is a logical outcome. Exhausting the water supply
without proper replenishment in form of rainfall has most likely led to the
recent water shortages.

It's important to note Chennai's main rainfall happens
during its monsoon season, which falls in the last few months and January. If
water usage continues as is throughout the year, the resevoirs are left nearly
empty by the time the monsoon arrives. Subsequently, if the monsoon doesn't
deliver an above normal rainfall, the water levels won't reach max capacity; the
water shortage cycle will continue, leading to lower reservoir water levels
annually. 

The analysis shows that the recent shortages are more than simply
doings of a cyclical change. Looking at the rainfall history, its a likely
conclusion that changes in the climate have had an impact on rainfall in
Chennai. Being a metropolis its expected that the population in Chennai will
continue to rise, which may lead to increased consumption that can excarbate the
water shortage crisis. Chennai cannot control the amount of rain it gets, but it
can control the usage--which is paramount if a water shortage crisis is to be
avoided.

# ***Thank You***

```python
## Test
```
