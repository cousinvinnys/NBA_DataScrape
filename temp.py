   playerBoxScore.style

# Create a matplotlib table of the teamBoxScore dataframe

#teamBoxScoreTable = ax.table(cellText=teamBoxScore.values, colLabels=teamBoxScore.columns, loc='center')

    testPlotDF = teamBoxScore

    drop_columns_2 = ['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'TEAM_ABBREVIATION','TEAM_NAME']
    testPlotDF = drop_columns(drop_columns_2, testPlotDF)

    fig, ax = plt.subplots()
    #ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=teamBoxScore.values, loc='center')

    # increase the font size to make it easier to read
    matplotlib.rc('font', size=20)

    fig.tight_layout()

    plt.show()
