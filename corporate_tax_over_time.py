# corporate tax changes over time

# (c) Dan Neidle of Tax Policy Associates Ltd
# licensed under the GNU General Public License, version 2

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from PIL import Image
import math
# also requires kaleido package

gdp_data_starting_year = 1965
gdp_data_end_year = 2018
rate_data_starting_year = 1965
rate_data_end_year = 2021

# visible_countries = "United Kingdom United States France Germany Denmark Spain Sweden Ireland New Zealand Australia Italy Japan Luxembourg Norway Switzerland Belgium"
visible_countries = "United Kingdom"

colours = ["aqua", "aquamarine", "azure", "bisque", "black", "blanchedalmond", "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgrey", "darkgreen", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey", "dodgerblue", "firebrick", "forestgreen", "fuchsia", "gainsboro", "ghostwhite", "gold", "goldenrod", "green", "greenyellow", "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray",  "lightgreen", "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray",  "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue", "purple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray", "springgreen", "steelblue", "tan", "teal", "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen"]

excel_file = "corporate_tax_over_time.xlsx"

logo_jpg = Image.open("logo_full_white_on_blue.jpg")

# create plotly graph object
# layout settings

logo_layout = [dict(
        source=logo_jpg,
        xref="paper", yref="paper",
        x=1, y=1.03,
        sizex=0.1, sizey=0.1,
        xanchor="right", yanchor="bottom"
    )]

end_year = min (gdp_data_end_year, rate_data_end_year)


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(
    images=logo_layout,
    title="Corporate tax revenues as a % of GDP (solid line) and tax rate (dashed line)",
    yaxis=dict(
        title="Corporate as as % of GDP",
        tickformat='.1%',  # so we get nice percentages
    ),
    xaxis=dict(
           dtick = 5, range = [gdp_data_starting_year, end_year]
       )
    )

fig.update_yaxes(title="Corporate tax rate (combined central and local), %", range = [0, 0.60], showgrid=False, tickformat='.0%', secondary_y=True)

print(f"Opening {excel_file}")
xl = pd.ExcelFile(excel_file)
print("")
print(f"Opened spreadsheet. Sheets: {xl.sheet_names}")

print("")

revenue_data = xl.parse("corp-tax-gdp")
rate_data = xl.parse("rates")

total_revenues = {}
total_rates = {}

line_colour = 0
for country_row in range (0,len(revenue_data)):
    country_name = revenue_data.iat[country_row, 0]
    print (country_name)

    # plot revenue data
    x_data = []  # year
    y_data = []  # CT revenues
    for i in range (0, end_year - gdp_data_starting_year):
        revenues = revenue_data.iat[country_row, i + 1] / 100
        year = gdp_data_starting_year + i
        x_data.append(year)
        y_data.append(revenues)

        if math.isnan(revenues) or revenues ==0:
            pass   #  no entry for this year, so keep out of averages
        else:
            if year in total_revenues:
                total_revenues[year].append(revenues)
            else:
                total_revenues[year] = [revenues]

    # add label to last data item showing country (bit hacky; must be better way)
    labels = [""] * (end_year - gdp_data_starting_year - 2)
    labels.append(country_name)

    if country_name in visible_countries:
        visibility = True
    else:
        visibility = 'legendonly'

    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode="lines+text",    # no markers
        name=country_name,
        legendgroup=country_name,
        text=labels,
        textposition="top center",
        showlegend=True,
        visible=visibility,
        line=dict(color=colours[line_colour])
    ),
    secondary_y=False)

    # plot rate data
    x_data = []  # year
    y_data = []  # CT rate
    for i in range(0, end_year - rate_data_starting_year):
        rate = rate_data.iat[country_row, i+1] / 100
        year = rate_data_starting_year + i
        x_data.append(year)
        y_data.append(rate)

        if math.isnan(rate) or rate == 0:
            pass  # no entry for this year, so keep out of averages
        else:
            if year in total_rates:
                total_rates[year].append(rate)
            else:
                total_rates[year] = [rate]

    # add label to last data item showing country (bit hacky; must be better way)
    labels = [""] * (end_year - rate_data_starting_year - 2)
    labels.append(country_name + "<br>(rate)")

    if country_name in visible_countries:
        visibility = True
    else:
        visibility = 'legendonly'

    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode="lines+text",  # no markers
        name=country_name,
        legendgroup=country_name,
        text=labels,
        textposition="top center",
        showlegend=False,
        visible=visibility,
        line=dict(color=colours[line_colour],dash='dash')
    ),
        secondary_y=True)

    line_colour += 1

# now compute OECD revenue average
x_data = []
y_data = []

for year in total_revenues:
    x_data.append(year)
    y_data.append(sum(total_revenues[year]) / len(total_revenues[year]))  # average revenue
    print(f"{year}: total {sum(total_revenues[year])}, and {len(total_revenues[year])} entries, so average {(sum(total_revenues[year]) / len(total_revenues[year]))}")

print("OECD averages:")
print(total_revenues[2000])

labels = [""] * (end_year - rate_data_starting_year - 2)
labels.append("OECD average")

fig.add_trace(go.Scatter(
    x=x_data,
    y=y_data,
    mode="lines+text",  # no markers
    name='OECD average',
    legendgroup='OECD average',
    text=labels,
    textposition="top center",
    showlegend=True,
    visible='legendonly',
    line=dict(color=colours[line_colour])
),
    secondary_y=False)


# now compute OECD revenue average
x_data = []
y_data = []

for year in total_rates:
    x_data.append(year)
    y_data.append(sum(total_rates[year]) / len(total_rates[year]))  # average revenue
    print(f"{year}: total {sum(total_rates[year])}, and {len(total_rates[year])} entries, so average {(sum(total_rates[year]) / len(total_rates[year]))}")

print("OECD averages:")
print(total_rates[2000])

labels = [""] * (end_year - rate_data_starting_year - 2)
labels.append("OECD average" + "<br>(rate)")

fig.add_trace(go.Scatter(
    x=x_data,
    y=y_data,
    mode="lines+text",  # no markers
    name='OECD average',
    legendgroup='OECD average',
    text=labels,
    textposition="top center",
    showlegend=True,
    visible='legendonly',
    line=dict(color=colours[line_colour],dash='dash')
),
    secondary_y=True)


# make legend more cramped, so all countries fit
fig.update_layout(legend_tracegroupgap=2)
fig.show()
# fig.write_image(f"Corporate tax.svg")