import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    from scipy import stats
    from scipy.interpolate import interp1d
    return interp1d, mo, pd, plt, stats


@app.cell
def _(mo):
    mo.md("""# Benzonic Acid""")
    return


@app.cell(hide_code=True)
def _(mo):
    dropdown = mo.ui.dropdown(
        options={ 
            "Benzonic": "benzonic.csv", 
            "Fumaric":"fumaric.csv", 
            "Maleic":"maleic.csv"}, 
        value="Benzonic", label="choose one"
    )
    dropdown

    return (dropdown,)


@app.cell(hide_code=True)
def _(dropdown, pd):
    df = pd.read_csv(dropdown.value)
    return (df,)


@app.cell(hide_code=True)
def _(df, interp1d, stats):
    # buckets
    t1 = df['time'].min()
    t2 = 360
    t3 = df['time'][df['temp'].idxmax()]
    t4 = df['time'].max()

    # First slope calculation
    df_ra = df[df['time'] <= t2]
    ra, intercept1, r_value1, p_value1, std_err1 = stats.linregress(df_ra['time'], df_ra['temp'])

    # Second slope calculation
    df_rb = df[(df['time'] >= t3) & (df['time'] <= t4)]
    rb, intercept2, r_value2, p_value2, std_err2 = stats.linregress(df_rb['time'], df_rb['temp'])

    # Calculate the time value when 60% of the temperature range is reached
    temp_range = df['temp'].max() - df['temp'].min()
    temp_60_percent = df['temp'].min() + 0.6 * temp_range

    interp = interp1d(df['temp'], df['time'])
    tx = interp(temp_60_percent)

    dtx = t3 - t2 - ra * (tx - t2) - rb * (t3 - tx)    # dTx = t3 - t2 - rA(tx - t2) - rB(t3 - tx)

    print(f"t1: {t1}")
    print(f"t2: {t2}")
    print(f"t3: {t3}")
    print(f"t4: {t4}")
    print("-"*80)
    print(f"dTx  ~60%: {tx}")
    print(f"dTx: {dtx}")
    return (
        df_ra,
        df_rb,
        dtx,
        intercept1,
        intercept2,
        interp,
        p_value1,
        p_value2,
        r_value1,
        r_value2,
        ra,
        rb,
        std_err1,
        std_err2,
        t1,
        t2,
        t3,
        t4,
        temp_60_percent,
        temp_range,
        tx,
    )


@app.cell(hide_code=True)
def _(
    df,
    dropdown,
    intercept1,
    intercept2,
    plt,
    ra,
    rb,
    t1,
    t2,
    t3,
    t4,
    temp_60_percent,
    tx,
):
    plt.figure(figsize=(10, 6))

    # Plot the dataframe 
    plt.plot(df['time'], df['temp'], label='Temperature Data')

    plt.axvline(x=t1, color='black', linestyle=':')
    plt.axvline(x=t2, color='black', linestyle=':')
    plt.axvline(x=t3, color='black', linestyle=':')
    plt.axvline(x=t4, color='black', linestyle=':')
    plt.text(t1 - 15, df['temp'].min() - 0.05, 't1', va='top', ha='center', color='black')
    plt.text(t2 - 15, df['temp'].min() - 0.05, 't2', va='top', ha='center', color='black')
    plt.text(t3 - 15, df['temp'].min() - 0.05, 't3', va='top', ha='center', color='black')
    plt.text(t4 - 15, df['temp'].min() - 0.05, 't4', va='top', ha='center', color='black')

    # dTx Marker
    plt.axvline(x=tx, color='green', linestyle='--', label='60% dTx')
    plt.text(tx + 10, temp_60_percent, f"dTx ~60%: {tx:.2f}", fontsize=12, color="green", ha="left", va="bottom")

    # plot line for rA
    plt.plot(df['time'], intercept1 + ra * df['time'], label='A', color='red')
    # rA text
    plt.text(1000, (intercept1 + ra * 1000) - 0.1, 'A', fontsize=12, ha='left', color='red')

    # plot line for rB
    plt.plot(df['time'], intercept2 + rb * df['time'], label='B', color='blue')
    # rB text 
    plt.text(1000, (intercept2 + rb * 1000) - 0.1, 'B', fontsize=12, ha='left', color='blue')

    # Axis lables
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [°C]')

    # Titel
    plt.title(f'{dropdown.selected_key} acid')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(False)
    plt.show()
    return


if __name__ == "__main__":
    app.run()
