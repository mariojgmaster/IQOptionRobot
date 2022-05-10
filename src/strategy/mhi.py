def mhi(opened, closed):
    """Valida se tem uma entrada MHI

        Args:
            opened (pd.series): pandas series de open
            closed (pd.series): pandas series de close
        
        Returns:
            [String|None]: put or call
    """

    # calcula mhi
    last_3_open = opened.tail(3)
    last_3_close = closed.tail(3)

    r = 0
    g = 0
    doji = 0

    for idx, val in enumerate(last_3_open):
        if last_3_open.iloc[idx] > last_3_close.iloc[idx]:
            r += 1
        elif last_3_open.iloc[idx] < last_3_close.iloc[idx]:
            g += 1
        else:
            doji += 1
    
    signal = None
    if doji == 0:
        if g >= 2:
            signal = 'put'
        if r >= 2:
            signal = 'call'
    
    print(f'R: {r} - G: {g} - D: {doji}')
    return signal