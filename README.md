# WeEagles
Team WeEagles Astro Pi Competition 2021/2022
Team members: 
 Wiktoria Dusza
 Antoni Moskal
 Kinga Moskal
 Julia Zegarowska
  
Mentor: Jadwiga Moskal

Our goal is to check the condition of forest areas, water bodies (oceans, seas and lakes) and the degree of cloudiness on the Earth with NDVI. The areas covered by vegetation are marked by higher NDVI values because they reflect much infrared radiation but relatively little visible light, compared to areas with no vegetation. Spectral reflectance for water is characterized by high absorption in the near, medium and far infrared - light reflection decreases from ultraviolet to infrared. As a result, water reservoirs can be easily detected and their boundaries carefully examined. Contaminated water has a higher reflectivity in the visible range than pure water. This dependence is also true for water with high chlorophyll content. That's why our measurements can be used to detect algae colonies as well as water pollution caused by for example, oil spills. 

In the experiment we will use the NoIR camera. We are planning to take images recorded on the SD card for further analysis.  The file name will contain timestamps. The program will count their number and assume their volume, if it will be close to limit it  will stop the recording on SD card. The names and total brightness in the Blue and IR channels will be recorded in the csv file together with the NDI (NDVI) calculated for the centre of image. After submitting photos to the Earth we will carry out further analysis.
