from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
app = Flask(__name__)  # Instantiate a new web application called `app`, with `__name__` representing the current file

data=pd.read_csv(r'/Users/kazba1/Downloads/Master-list-numeric.csv')
df=pd.DataFrame(data)
df=df.drop("Unnamed: 0", axis=1)
df=df.replace(" ",np.nan)
df=df[df['Target business description'].notnull()]
df=df.reset_index(drop=True)

@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        keyword = request.form.get("keyword")
        Revenue_Turnover = request.form.get("Revenue_Turnover")
        EBITDA = request.form.get("EBITDA")
        Net_profit = request.form.get("Net_profit")
        Enterprise_value = request.form.get("Enterprise_value")
        keyword = keyword.split()
        global df
        df['Keyword count'] = 0
        for j in range(len(keyword)):
            df.loc[(df['Target business description'].str.contains(keyword[j])), 'Keyword count'] += 1
        df['variable difference %'] = 0
        if Revenue_Turnover != "n.a.":
            df = df.dropna(subset=['Pre-deal target operating revenue/turnover'])
            Revenue_Turnover = int(Revenue_Turnover)
            df['variable difference %'] += ((df['Pre-deal target operating revenue/turnover'].astype(int) - Revenue_Turnover) / Revenue_Turnover).abs() * 100
        if EBITDA != "n.a.":
            df = df.dropna(subset=['Pre-deal target EBITDA'])
            EBITDA = int(EBITDA)
            df['variable difference %'] += ((df['Pre-deal target EBITDA'].astype(int) - EBITDA) / EBITDA).abs() * 100
        if Net_profit != "n.a.":
            df = df.dropna(subset=['Net profit'])
            Net_profit = int(Net_profit)
            df['variable difference %'] += ((df['Net profit'].astype(int) - Net_profit) / Net_profit).abs() * 100
        if Enterprise_value != "n.a.":
            df = df.dropna(subset=['Enterprise value'])
            Enterprise_value = int(Enterprise_value)
            df['variable difference %'] += ((df['Enterprise value'].astype(int) - Enterprise_value) / Enterprise_value).abs() * 100
        df = df.sort_values(by=['Keyword count', 'variable difference %'], ascending=[False, True])
        df['variable difference %']=df['variable difference %'].round(2)
        df = df.reset_index(drop=True)
        df = df[:30]
        df = df.astype(str).apply(lambda x: x.str[:70])
        for i in range(0, 30):
            if len(df.loc[(i, 'Target business description')]) == 70:
                df.loc[(i, 'Target business description')] = df.loc[(i, 'Target business description')] + "..."
        return render_template('simple.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


#Creating boxplot:
@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')
## Store data in each collection
Revenue_T = Revenue_Turnover
EBITDA_ = EBITDA
Net_P = Net_profit
Enter_V = Enterprise_value
Deal_V =

## combine these different collections into a list
data_to_plot = [Revenue_T, EBITDA_, Net_P, Enter_V, Deal_V]

# Create a figure instance (Size is optional)
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)

#Create boxplot
bp = ax.boxplot(data_to_plot, patch_artist=True)

## change outline color, fill color and linewidth of the boxes
for box in bp['boxes']:
    # change outline color
    box.set( color='#7091b3', linewidth=2)
    # change fill color
    box.set( facecolor = '#1b9e77' )

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='#7091b3', linewidth=2)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='#7091b3', linewidth=2)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='#b2df8a', linewidth=2)

## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', color='#e7298a', alpha=0.5)

# Save the figure
fig.savefig('fig1.png', bbox_inches='tight')

#Done with boxplot


#Create summary statistics Tabel

#Easyway
print df.describe(include='average')

#Hard way
import plotly.graph_objects as go

headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'


fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Values</b>','<b>Revenue_Turnover</b>','<b>EBITDA</b>','<b>Net_profit</b>','<b>Enterprise_value</b>','<b>Deal Value</b>'],
    line_color='darkslategray',
    fill_color=headerColor,
    align=['left','center'],
    font=dict(color='white', size=12)
  ),
  cells=dict(
    values=df.describe(include='average'),
    line_color='darkslategray',
    # 2-D list of colors for alternating rows
    fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
    align = ['left', 'center'],
    font = dict(color = 'darkslategray', size = 11)
    ))
])

fig.show()




