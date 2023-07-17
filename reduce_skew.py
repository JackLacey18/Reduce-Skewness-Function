def reduce_skew(df):
    upper_skew = 0.5
    lower_skew = -0.5
    
    # Only select columns of type float or int.
    floats = [i for i in df.columns if df[i].dtype =='float' or df[i].dtype == 'int']
    
    # For each column where the column is of type float or int.
    for col in floats:
        
        # Initialise high and low quantile for positive and negative skew respectively.
        pos_quantile = 1.0
        neg_quantile = 0.0
        
        # Initialise while loop to keep changing the quantile until the skew is acceptable.
        while df[col].skew(axis=0) > upper_skew or df[col].skew(axis=0) < lower_skew:

            # If there is positive or right skew.
            if df[col].skew(axis=0) > upper_skew:
                # Find the quantile of the column at the current pos_quantile. 
                quant = df[col].quantile(pos_quantile)
                # Initialise a secondary dataframe where values in that column are 
                # below the current pos_quantile.
                df_1 = df[df[col] < quant]
                # If the skew of secondary dataframe is acceptable, the primary dataframe
                # is set to a new dataframe where all values in the current column are below
                # that quantile value otherwise reduce the pos_quantile.
                if df_1[col].skew(axis=0) <= upper_skew:
                    df = df[df[col] < df[col].quantile(pos_quantile)]
                else:
                    pos_quantile -= 0.001

            # If there is negative or left skew repeat a similar method to positive skew
            # but increase neg_quantile until skewness is acceptable.
            if df[col].skew(axis=0) < lower_skew:
                quant = df[col].quantile(neg_quantile)
                df_1 = df[df[col] > quant]
                df_1[col].skew(axis=0)
                if df_1[col].skew(axis=0) >= lower_skew:
                    df = df[df[col] > df[col].quantile(pos_quantile)]
                else:
                    neg_quantile += 0.001
                    
    return df