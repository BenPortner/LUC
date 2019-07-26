import brightway2 as bw
import numpy as np
import pandas as pd
import itertools

import bokeh.io
import bokeh.plotting
import bokeh.models.tools
import bokeh.layouts
import bokeh.models
from bokeh.palettes import Category10_10 as palette
from bokeh.transform import dodge



# bokeh constants
width = 900
height = 300


def getILCDMethods():
    aoMethods = [m for m in bw.methods if "ILCD" in str(m) and "2018" in str(m) and "LT" not in str(m)]
    return aoMethods

def doLCA(oActivity, aoMethods, HHV=None):
    if HHV:
        functional_unit = {oActivity:1/HHV}
    else:
        functional_unit = {oActivity:1}
    oLCA = bw.LCA(functional_unit, aoMethods[0])
    oLCA.lci()
    oLCA.lcia()
    dScores = {aoMethods[0]:oLCA.score}
    for oMethod in aoMethods[1:]:
        oLCA.switch_method(oMethod)
        oLCA.lcia()
        dScores[oMethod] = oLCA.score
    return dScores, oLCA


def compareStaticLCA_interactive(dScores1, dScores2, sFileName="static_LCA_comparison.html", legend1=None, legend2=None):

    # check if same methods have been used, abort if not
    if not dScores1.keys() == dScores2.keys():
        print("Methods are different. Comparison invalid.")
        return

    # plot layout options
    bar_width = 0.5

    # extract method names, units
    ltMethods = [m for m in dScores1.keys()]
    lsUnits = [bw.Method(m).metadata["unit"] for m in dScores1.keys()]
    lsNames = [", ".join(bw.Method(m).name) for m in dScores1.keys()]
    lsMethodLabels = lsNames

    # normalized values
    normalized_v1 = np.array([np.sign(v) for v in dScores1.values()])
    normalized_v2 = np.array([np.sign(v2)*np.abs(v2/v1) for v1, v2 in zip(dScores1.values(), dScores2.values())])

    # bar labels = actual values
    lsBarLabels1 = ["%.2e " % v + unit for v, unit in zip(dScores1.values(), lsUnits)]
    lsBarLabels2 = ["%.2e " % v + unit for v, unit in zip(dScores2.values(), lsUnits)]

    # putting it all together
    source1 = bokeh.models.ColumnDataSource(
        data=dict(
            y=normalized_v1,
            method=lsMethodLabels,
            value=lsBarLabels1,
            methods = ltMethods
        )
    )
    source2 = bokeh.models.ColumnDataSource(
        data=dict(
            y=normalized_v2,
            method=lsMethodLabels,
            value=lsBarLabels2,
            methods = ltMethods
        )
    )

    TOOLTIPS = [
        ("method", "@method"),
        ("value", "@value")
    ]

    # plot
    f = bokeh.plotting.figure(x_axis_label="indicator", y_axis_label='normalized impact [-]',
                              plot_width=width, plot_height=height*3, tooltips = TOOLTIPS,
                              x_range=bokeh.models.FactorRange(*ltMethods))
    p1 = f.vbar(x="methods", top="y", width=bar_width, color=palette[0], alpha=0.6, source=source1)
    p2 = f.vbar(x=dodge('methods', bar_width/2, range=f.x_range), top="y", width=bar_width, color=palette[1], alpha=0.6, source=source2)

    # build legend
    legend = bokeh.models.Legend(items=[
        (legend1, [p1]),
        (legend2, [p2]),
    ], location="center", orientation="horizontal", label_width=75)
    f.add_layout(legend, 'above')

    # font sizes
    font_size = "15pt"
    f.xaxis.axis_label_text_font_size = \
        f.yaxis.axis_label_text_font_size = \
        f.xaxis.major_label_text_font_size = \
        f.yaxis.major_label_text_font_size = \
        f.legend.label_text_font_size = font_size

    # x label rotation
    f.xaxis.major_label_orientation = np.pi / 2

    # add tool for strict y-axis zoom
    f.add_tools(bokeh.models.WheelZoomTool(dimensions="height"))

    # show the results
    bokeh.io.output_notebook()
    bokeh.io.show(f)
    pass


def plotContributionAnalysis(dContributions, sFileName, lsFromActivities=None, sDatabase=None, bLegend=True, fCutOff=0.005):

    oParentActivity = list(dContributions.values())[0][0]["from"][0]

    # find contributions, save in list
    ldMethodActContrib = []
    for oMethod, ldContributions in dContributions.items():

        # break down contributions to
        # a) direct contributions to parent activity if no names supplied
        # b) contributions from activities originating in databases which are not sDatabase
        # c) contributions of activities supplied by user, if names are given
        if lsFromActivities:
            direct_contributions = [c for c in ldContributions if c["from"][-1]["name"] in lsFromActivities]
        elif sDatabase:
            direct_contributions = [
                c for c in ldContributions if (
                    c["from"][-1].get("database","") != sDatabase and
                    c["to"][-1].get("database","") == sDatabase and
                    not bool(c["to"][-1].get("aggregate",False))
                ) or (
                    bool(c["from"][-1].get("aggregate", False))
                )
            ]
        else:
            direct_contributions = [c for c in ldContributions if c["to"] == [oParentActivity]]


        # save method name, activity name, relative contribution to impact in dictionary
        fuGetName = lambda x: \
            (x["from"][-1]["database"] == "biosphere3") * x["to"][-1]["name"] +\
            (x["from"][-1]["database"] != "biosphere3") * x["from"][-1]["name"]
        ld = [{
            "method":oMethod,
            "activity":fuGetName(a).replace("{","(").replace("}",")").replace("|",", "), # replace {} from simapro activities to prevent errors
            "contribution": np.sign(a["global impact"]) * abs(a["global impact"] / ldContributions[0]["global impact"])
        } for a in direct_contributions]

        ldMethodActContrib += ld

    # make dataframe from list of dict
    dfContributions = pd.DataFrame(ldMethodActContrib)
    dfContributions = dfContributions.groupby(['method', 'activity']).sum().reset_index()

    # remove entries smaller than cutoff
    dfContributions = dfContributions[dfContributions["contribution"].abs() >= fCutOff*abs(dfContributions["contribution"].max())]

    # pivot, replace 0 with nan
    dfPivoted = dfContributions.pivot(index="method", columns="activity", values="contribution")
    dfPivoted.fillna(0, inplace=True)

    # creating necessary dicts and lists for bokeh plot
    data_pos = {c : dfPivoted[c].values * (dfPivoted[c].values > 0) for c in dfPivoted.columns}
    data_neg = {c : dfPivoted[c].values * (dfPivoted[c].values < 0) for c in dfPivoted.columns}
    methods = dfContributions["method"].unique()
    activities = dfPivoted.columns
    colors = [c for a, c in zip(activities, itertools.cycle(palette))]
    data_neg["methods"] = data_pos["methods"] = methods
    source1 = bokeh.models.ColumnDataSource(data=data_pos)
    source2 = bokeh.models.ColumnDataSource(data=data_neg)
    TOOLTIPS = [
        ("method", "@methods"),
        ("activity", "$name"),
        ("contribution", "@$name")
    ]

    # plot contributions per category
    f = bokeh.plotting.figure(x_axis_label="indicator", y_axis_label='contribution to impact [-]',
                              plot_width=width, plot_height=height*3, tooltips = TOOLTIPS,
                              x_range=bokeh.models.FactorRange(*methods))
    p1 = f.vbar_stack(activities, x="methods", width=0.5, alpha=0.6, fill_color=colors, line_color="white", source=source1)
    f.vbar_stack(activities, x="methods", width=0.5, alpha=0.6, fill_color=colors, line_color="white", source=source2)

    # x label rotation
    f.xaxis.major_label_orientation = np.pi / 2

    # build legend
    if bLegend:
        legend = bokeh.models.Legend(items=[(l,[p]) for l,p in zip(activities,p1)], location="center")
        f.add_layout(legend, 'above')

    # font sizes
    font_size = "15pt"
    f.xaxis.axis_label_text_font_size = \
        f.yaxis.axis_label_text_font_size = \
        f.xaxis.major_label_text_font_size = \
        f.yaxis.major_label_text_font_size = \
        f.legend.label_text_font_size = font_size

    # add tool for strict y-axis zoom
    f.add_tools(bokeh.models.WheelZoomTool(dimensions="height"))

    # show the results
    bokeh.io.output_notebook()
    bokeh.io.show(f)

    pass
