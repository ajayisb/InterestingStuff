# Creating forward fiscal quarter
guidance['f_fqtr'] = guidance['fqtr'] + 1

# Adjust the fiscal year if the forward quarter is 5 (Q5)
guidance['f_fyearq'] = guidance['fyearq']
guidance.loc[guidance_f['f_fqtr'] == 5, 'f_fyearq'] += 1

# Map the forward quarter from 5 (Q5) to 1 (Q1)
guidance['f_fqtr'] = (guidance['f_fqtr'] - 1) % 4 + 1




##########################################################
## creating lag fiscal year and fiscal quarter

guidance_f['l_fqtr'] = guidance_f['fqtr'] - 1
# Adjust the fiscal year if the previous quarter is 0 (Q0)
guidance_f['l_fyearq'] = guidance_f['fyearq']
guidance_f.loc[guidance_f['l_fqtr'] == 0, 'l_fyearq'] -= 1
# Map the previous quarter from 0 (Q0) to 4 (Q4)
guidance_f['l_fqtr'] = (guidance_f['l_fqtr'] - 1) % 4 + 1



########################################################
### Calculate fiscal year and fiscal quarters given date and fiscal end month

def calculate_fiscal(df, date):
    df['fyearq'] = np.where(df['eefymo'] <= 5,
                                          (date.dt.month <= df['eefymo']) * (date.dt.year - 1) + (date.dt.month > df['eefymo']) * date.dt.year,
                                          (date.dt.month <= df['eefymo']) * date.dt.year + (date.dt.month > df['eefymo']) * (date.dt.year + 1))
    df['fqtr'] = np.where(df['eefymo'] == date.dt.month, 4,
                                         np.ceil(((date.dt.month - df['eefymo']) / 3) % 4))
    return df
fpedats = pd.to_datetime(guidance_1['fpedats'])
guidance_f = calculate_fiscal(guidance_1, fpedats)


##################################################################

# Create a new column 'FPEDAT' using prd_yr and prd_mon

guidance['fpedats'] = guidance.apply(lambda row: datetime(row['prd_yr'], row['prd_mon'], 1) + pd.DateOffset(months=1) - pd.DateOffset(days=1), axis=1)


####################################################################

grouped = history_analyst.groupby(['TICKER','f_Year' ,'f_Quarter'])
n_analyst = grouped['ANALYS'].transform(lambda x: x.nunique())
history_analyst = history_analyst.assign(n_analyst=n_analyst)


#######################################################################
### Earnings_volatility variable creation: Measured as STD of last 4 quarters earnings.

comp_vol['fyearq_1'] = comp_vol['fyearq']-1
comp_vol['fqtr_1'] = comp_vol['fqtr']
comp_vol['fyearq_qtr'] = comp_vol['fyearq'].astype(int).astype(str) + 'Q' + comp_vol['fqtr'].astype(int).astype(str)
comp_vol['fyearq_qtr_1'] = comp_vol['fyearq_1'].astype(int).astype(str) + 'Q' + comp_vol['fqtr_1'].astype(int).astype(str)

comp_ibq = comp[['tic','fyearq','fqtr','ibq']].drop_duplicates()
comp_ibq['fyearq_qtr'] = comp_ibq['fyearq'].astype(int).astype(str) + 'Q' + comp_ibq['fqtr'].astype(int).astype(str)

comp_volatility = pd.merge(comp_vol.dropna(subset=['tic']), comp_ibq.dropna(subset=['tic']), on='tic', how='left')

# Apply the filter conditions using boolean indexing
comp_volatility1 = comp_volatility[
    (comp_volatility['fyearq_qtr_y'] <= comp_volatility['fyearq_qtr_x']) &
    (comp_volatility['fyearq_qtr_y'] > comp_volatility['fyearq_qtr_1']) ]











