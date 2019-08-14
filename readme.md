<span style="line-height:1.5"> Environmental impact of open ground PV displacing corn production in the USA </span>
Author: Benjamin W. Portner, Bauhaus Luftfahrt e.V., Willy-Messerschmitt-Straße 1, 82024 Taufkirchen

<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Research-question" data-toc-modified-id="Research-question-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Research question</a></span></li><li><span><a href="#Introduction" data-toc-modified-id="Introduction-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Methodology" data-toc-modified-id="Methodology-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Methodology</a></span></li><li><span><a href="#Inventory" data-toc-modified-id="Inventory-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Inventory</a></span></li><li><span><a href="#Impact-assessment" data-toc-modified-id="Impact-assessment-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Impact assessment</a></span></li><li><span><a href="#Conclusion" data-toc-modified-id="Conclusion-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Conclusion</a></span></li></ul></div>

## Research question
Should photovoltaic panels be installed on ground-area currently used for agriculture? More specifically: Is it environmentally harmful if open ground PV is installed in US areas currently used for corn production?

## Introduction
Photovoltaic (PV) panels are a promising technology for sustainable energy production. In order to produce significant amounts of electricity, it is not enough to install panels on roofs exclusively. Today and most-likely also in the future, significant amounts of PV electricity will come from ground installations. This electricity will displace electricity from fossil sources such as coal and natural gas, thus reducing the environmental impact of the grid mix. However, installation on open ground also means that the area under the panels cannot be used for agricultural activities. In case of the USA, one common agricultural activity is the production of corn. Main supplier is the so-called "corn belt" which comprises Iowa, Indiana, Illinois, Ohio and parts of their neighboring states. PV installation in the corn belt would reduce the amount of farmable land. Assuming that the market demand for corn remains constant, reduced production will induce a rise in market price. This in turn will draw new producers in other locations to the market. This displacement of production is called indirect land use change. For this study, I assume rigid market prices, i.e. the displacement of 1 kg of corn production from the US will induce the production of 1 kg of corn in Argentina. This is a rather pessimistic scenario in terms of land use change. Because productivity per area (kg corn produced per m2) is on average lower in Argentina than in the USA, indirect land use change will negatively affect the installed PV plant's environmental impact. At the same time, PV electricity will displace fossil grid electricity in the USA, which will improve its impact. In this document I will quantify both effects in order to decide which one is stronger and thus, whether PV installation in the corn belt makes sense from an ecological perspective. 


## Methodology
Two scenarios are analyzed:
1. business-as-usual: corn is produced in the corn belt, electricity grid mix in the USA is unchanged
2. PV: corn is produced in Argentina, PV electricity is fed into the grid in the USA

The scenarios' impacts are compared in order to decide which one is more beneficial for the environment. For modeling, ecoinvent 3.5 is used as background database. Allocation at the point of substitution is used as the system model. ILCD 2018 midpoint methods are used for impact assessment. Brightway is used for database manipulation and impact calculations.


## Inventory
The plant occupies an area of 4400 m2 and produces electricity using polycrystalline Silicon panels. The plant's nominal capacity is 570 kWp, it's life time is 30 years ("photovoltaic plant construction, 570kWp, multi-Si, on open ground", location "GLO"). Assuming an effective electricity production of 1099.4 kWh produced per year and per kWp capacity, total electricity output of the plant over its life time is 1.88E7 kWh (ecoinvent activity "electricity production, photovoltaic, 570kWp open ground installation, multi-Si", location "RFC").

The average occupation of 1 kg of corn in the US is 0.62623 m2 yr. Thus, 1.60 kg of corn are produced per m2 and year ("maize grain production", location "US"). The total corn production on 4400 m2 of land over 30 yrs amounts to 2.11E5 kg. If the area is used for PV electricity production instead, 1.88E7 kWh are produced and fed into the grid. In this case, 2.11E5 kg of corn need to be produced in Argentina. The average occupation of 1 kg of corn in Argentina is 1.355 m2 yr (0.74 kg corn per m2 and year, ecoinvent activity "maize grain production", location "AR"). Hence, 9524 m2 are needed to produce the displaced amount of corn over 30 years. This is 2.2 times the area that is needed in the USA. Since the production is outsourced from the US, additional agricultural land needs to be created in Argentina. It is converted from a mix of existing lands such as agricultural area, grass land, forest, etc. The environmental impact of this land conversion is modeled using the ecoinvent activity "land use change, annual crop", location "AR".

*Scenario business-as-usual*
- 2.11E5 kg corn produced in US
- 1.88E7 kWh grid electricity produced in RFC


*Scenario PV*
- 2.11E5 kg corn produced in AR 
- 1.88E7 kWh PV electricity produced in RFC
- 9.524E-1 ha converted to crop land in AR


For the impact assessment, all values are normalized by the amount of electricity produced (1.88E7 kWh). The functional unit is then 1 kWh of electricity and 11 g of corn.


## Impact assessment




```python
from helper_functions import *
import pickle

bw.projects.set_current("ecoinvent-import")

# helper variables
o = bw.Database("LUC PV").search("electricity production")[0]
oRef = bw.Database("LUC PV").search("reference")[0]
aoILCD = getILCDMethods()

# do static LCA
dScores, oLCA = doLCA(o, aoILCD)
dScores_ref, oLCA_ref = doLCA(oRef, aoILCD)
compareStaticLCA_interactive(dScores, dScores_ref, None, "PV", "business-as-usual")
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="1054">Loading BokehJS ...</span>
    </div>











  <div class="bk-root" id="b3d10316-cdc6-43c3-9787-d830962cdbbf" data-root-id="1004"></div>





Figure 1 compares the environmental impact of both scenarios (business-as-usual: orange, PV: blue). The two scenarios are scored according to the 19 ILCD midpoint impact categories. The results are normalized with respect to the PV scenario. 

The PV scenario shows a lower impact than the business-as-usual scenario in most categories. As expected, it compares worse in the land use change category. However, the main contribution is not the land converted in Argentina but the PV plant itself. The electricity grid mix in the business-as-usual scenario contains large amounts of coal and natural gas power. These sources need a negligible amount of land when compared to a PV plant. Hence, the PV scenario has a higher land use impact. Still, the GHG emissions from land use change caused by PV are small compared to those from the grid mix. Thus, the PV scenario has lower total GHG emissions (climate change total). It also has a larger impact on minerals- and metal resources. Again, contributions are mainly from the PV system itself, due to the amount of aluminium needed to produce mounting systems and panel cases, as well as silver, gold and copper needed for contacts and wiring.


```python
f = open("res/contribution_analysis_results.pkl","rb")
dContributions_net = pickle.load(f)
f.close()
plotContributionAnalysis(dContributions_net, None, fCutOff=0.01)
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="1202">Loading BokehJS ...</span>
    </div>











  <div class="bk-root" id="3c4e1391-2650-4e64-afac-7d3f71643a54" data-root-id="1135"></div>





Figure 2 compares the impacts of corn production displacement (impacts of AR corn production plus impacts of AR land use change minus impacts of US corn production) to those of PV electricity substituting grid electricity (impacts of PV electricity production in the US minus impacts of average grid electricity production in the US).

For almost all of the categories, displacement of grid electricity by PV electricity has a negative score, i.e. contributes positively to the impact of PV installation. The only exceptions are "land use" and "minerals and metals" for the reasons stated above. As expected, displacement of corn production to Argentina contributes negatively (positive score) to the ecological impact in almost all categories. The only positive impacts of corn production in Argentina vs. USA are seen in the categories "freshwater ecotoxicity" and "dissipated water". The former impact is caused by significant emissions of zinc and chromium to freshwater in case of corn production in the USA. The later impact is caused by larger amounts of water evaporating in case of US corn production.

## Conclusion
The construction of PV systems in the corn belt in the US will cause corn production to shift to other regions. The drawbacks of this shift are smaller than the benefits of displacing fossil-based grid electricity. Generally, the impacts of corn production are small when compared to the impact of PV plant construction and -operation. Whether PV installation on land currently used for corn production in the US makes sense from an ecological stand-point depends on the weight applied to each impact category. If land use or metal resource depletion are given high priority, PV installation should be avoided. In all other cases, PV installation has a beneficial influence on the environment, compared to the status quo.
