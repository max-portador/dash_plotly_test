def apply_filter(df, option_slctd, column):
    if isinstance(option_slctd, list):
        if len(option_slctd):
            return df[df[column].isin(option_slctd)]
    else:
        return df[df[column] == option_slctd]
    return df