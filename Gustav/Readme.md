# Hurricane Gustav (aal072008)

### Instructions to Run


## Storm Info
Hurricane Gustav was a category 4 hurricane that officially became so at UTC 18:00 on August 30th, 2008. Gustav made several landfalls along its path, including on Haiti, Cuba, and Louisiana. Prior to then, Gustav had originated as a tropical wave off the coast of Africa on August 13th, moving westward until it became classified as a tropical depression on August 25th about 350 miles south of Puerto Rico. It quickly developed into a tropical storm at UTC 12:00 on August 25th and a hurricane shortly thereafter. Gustav then weakened into a tropical storm on August 27th and remained so as it passed through Jamaica. The storm intensified on August 29th, and regained hurricane status as a category 2 hurricane as it traveled over Cayman Islands on August 30th. It grew into a category 4 hurricane just before making landfall in Cuba, thus officially acquiring the title of a major hurricane. Although Gustav weakened over the Gulf of Mexico, Gustav made landfall on Louisiana at UTC 15:00 on September 1st as a category 2 hurricane. The hurricane then further weakened into a tropical storm midway through Louisiana, and became a tropical depression as it passed into Arkansas. Gustav reduced to being extratropical as it moved north into Missouri. 

For topological purposes, we focus on the latter half of hurricane Gustav as it passes through Louisiana. 

*Source:* https://www.nhc.noaa.gov/data/tcr/AL072008_Gustav.pdf

**Topography Info:** Topography data was fetched from the following:

http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

---
## Geoclaw Parameters 
**Storm Data:** http://ftp.nhc.noaa.gov/atcf/archive/2008/aal072008.dat.gz

**Landfall Time:** UTC 15:00 on 09/01/2008

**Begin Time:** UTC 15:00 on 08/30/2008

**End Time:** UTC 15:00 on 09/03/2008

**Gauge Data:** https://tidesandcurrents.noaa.gov/inundationdb/

**Gauges:** 
1. Grand Isle, LA (8761724)
2. Pilots Station East, SW Pass, LA (8760922)
3. Dauphin Island, AL (8735180)
4. Freshwater Canal Locks, LA (8766072)
5. Pascagoula NOAA Lab, MS (8741533)
6. Shell Beach, LA (8761305)

**AMRClaw Parameters:**
Here we set `amr_levels_max` to 7 with `refinement_ratios` as `[2,2,2,3,4,4,4,]`.

---
## Results

Note: some gauge coordinates were shifted slightly to allow for better modelling of surge, the ones noted below are for simulation purposes

---
**Gauge 1:** `Grand Isle, LA`

**Coordinates:** 89.7567 W, 29.2733 N

<img width="322" alt="Screen Shot 2022-08-27 at 11 10 53 PM" src="https://user-images.githubusercontent.com/98766868/187055798-aa1b4af3-ad8d-4bda-8676-7096c20c96b9.png">

**Actual Surge:** 1.22 meters

**Predicted Surge:** 2.38 meters

---
**Gauge 2:** `Pilots Station East, SW Pass, LA`

**Coordinates:** 89.4067 W, 28.9317 N

<img width="321" alt="Screen Shot 2022-08-27 at 11 11 06 PM" src="https://user-images.githubusercontent.com/98766868/187055800-150117bb-f6f3-44fd-9c26-a0d306944c47.png">

**Actual Surge:** 0.82 meters

**Predicted Surge:** 1.01 meters

---
**Gauge 3:** `Dauphin Island, AL`

**Coordinates:** 88.0750 W, 30.2500 N

<img width="322" alt="Screen Shot 2022-08-27 at 11 11 24 PM" src="https://user-images.githubusercontent.com/98766868/187055801-4c0b5fcc-988f-4d9f-865a-969493e05f24.png">

**Actual Surge:** 1.00 meters

**Predicted Surge:** 0.55 meters

---
**Gauge 4:** `Freshwater Canal Locks, LA`

note: left of landfall — clockwise spin and thus negative surge

**Coordinates:** 92.3050 W, 29.4717 N

<img width="321" alt="Screen Shot 2022-08-27 at 11 11 35 PM" src="https://user-images.githubusercontent.com/98766868/187055813-65aa222a-bb6f-4d72-acaf-4ad81f3587fb.png">

**Actual Surge:** -1.23 meters

**Predicted Surge:** -0.49 meters

---
**Gauge 5:** `Pascagoula NOAA Lab, MS`

**Coordinates:** 88.9633 W, 30.3683 N

<img width="323" alt="Screen Shot 2022-08-27 at 11 11 58 PM" src="https://user-images.githubusercontent.com/98766868/187055820-9ec65af0-a796-434b-b28a-7f52fc293cfd.png">

**Actual Surge:** 1.55 meters

**Predicted Surge:** 1.41 meters

---
**Gauge 6:** `Shell Beach, LA`

**Coordinates:** 89.6733 W, 29.9683 N

<img width="321" alt="Screen Shot 2022-08-27 at 11 12 13 PM" src="https://user-images.githubusercontent.com/98766868/187055821-a4494d06-4877-47d0-a5b8-e41417fa71ee.png">

**Actual Surge:** 2.86 meters

**Predicted Surge:** 1.35 meters

---
## Conclusion
Overall, the predicted surge mostly matched the actual data. The most notable discrepancies were Grand Isle and Shell Beach, both of which were over a meter off in prediction. These are likely by cause of flooding/rainfall; complex topography also plays a role due to our limited ability to refine. Timing of surges generally agreed between data and prediction. All of the simulations underestimated the size of the surges to some degree, and this may be due to flooding/rainfall unaccounted for in the simulations.

Author: Peter Jin
