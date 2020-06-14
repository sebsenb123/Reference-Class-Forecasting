for c in range(len(df)):
    if Revenue_Turnover != "n.a." and df.loc[(c, 'Pre-deal target operating revenue/turnover')] != "NaN":
        Revenue_Turnover = int(Revenue_Turnover)
        df.loc[(c, 'variable difference %')] += ((df.loc[(c, 'Pre-deal target operating revenue/turnover')].astype(
            int) - Revenue_Turnover) / Revenue_Turnover).abs() * 100
        df = df.dropna(subset=['Pre-deal target operating revenue/turnover'])
    if EBITDA != "n.a." and df.loc[(c, 'Pre-deal target EBITDA')] != "NaN":
        EBITDA = int(EBITDA)
        df['variable difference %'] += ((df['Pre-deal target EBITDA'].astype(int) - EBITDA) / EBITDA).abs() * 100
        df = df.dropna(subset=['Pre-deal target EBITDA'])
    if Net_profit != "n.a." and df.loc[(c, 'Net profit')] != "NaN":
        Net_profit = int(Net_profit)
        df['variable difference %'] += ((df['Net profit'].astype(int) - Net_profit) / Net_profit).abs() * 100
        df = df.dropna(subset=['Net profit'])
    if Enterprise_value != "n.a." and df.loc[(c, 'Enterprise value')] != "NaN":
        Enterprise_value = int(Enterprise_value)
        df['variable difference %'] += ((df['Enterprise value'].astype(
            int) - Enterprise_value) / Enterprise_value).abs() * 100
        df = df.dropna(subset=['Enterprise value'])