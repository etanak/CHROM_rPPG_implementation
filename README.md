<div align="center">

# CHROM rPPG Implementation

This is part of my undergrad graduation project for the Electrical Engineering Project 2102499 course. This is a CHROM rPPG implementation to estimate heart rate with finite state machine to validate.

❗️<b style="color:red">DISCLAIMER:</b>❗️ I didn't develop the entire code myself. I have given credit to other Githubs in the last part of this README (BIG THANKS!!)

</div>

## Running the Code
1. Clone/download SkinDetector at: https://github.com/pavisj/rppg-pos/tree/master/SkinDetector and place the SkinDetector folder in a place where it's compatible with your path.
2. Install all the required libraries.
3. The main code to execute is `FSM_x_CHROM.py`.
4. To validate the estimated HR, you can take a look at the `.csv` files and run `bland_altman.py` to plot all the graphs.

## Results 📊
<div align="center">
  
  The study collected data from two groups of subjects, one with normal skin color and one with darker skin color. The normal skin group had 484 samples and the darker skin group had 207 samples. The mean absolute difference (MAD) and standard deviation (SD) were calculated for both groups. The results showed that the MAD and SD were slightly higher for the darker skin group.
  
  |             | MAD (mean absolute difference) | SD (standard deviation) |
|-------------|--------------------------------|-------------------------|
| Normal Skin | 2.20                           | 2.98                    |
| Tanned Skin   | 2.71                           | 3.60                    |


To visualize the data, scatter plots, Bland-Altman plots, and density histograms were used. These graphs showed the distribution of the data and how close the estimated heart rate was to the actual heart rate.

You can find these graphs in Figures 1-3.

![Figure_1](https://user-images.githubusercontent.com/108513333/237021689-8b19b57d-9e29-42e5-a5d7-51d68463d091.png)
<br>Figure 1 - Scatter plot 

![Figure_2](https://user-images.githubusercontent.com/108513333/237021781-2010ba2e-95d9-4de2-8a3d-c6ba96d2d5e5.png)
<br>Figure 2 - Bland-Altman plot

![Figure_3](https://user-images.githubusercontent.com/108513333/237021816-72b471dc-6128-4b77-b65c-ec5437d705b0.png)
<br>Figure 3 - Density histogram

</div>

## Test Videos 🎥
- [CHROM test](https://youtu.be/e884ERxox64)
- [CHROM x FSM test](https://youtu.be/qiBjtAyDVHA)


<div align="center">

## Acknowledgments

BIG THANKS TO THESE GITHUBS!!: 💖💖
- https://github.com/dnwjddl/remotePPG
- https://github.com/pavisj/rppg-pos
- https://github.com/habom2310/Heart-rate-measurement-using-camera

</div>

--- 
