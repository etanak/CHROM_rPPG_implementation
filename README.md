<div align="center">

# CHROM rPPG Implementation

This is part of my undergrad graduation project for the Electrical Engineering Project 2102499 course.

❗️<b style="color:red">DISCLAIMER:</b>❗️ I didn't develop the entire code myself. I just modified and assembled others' codes together. I have given credit to other Githubs in the last part of this README (BIG THANKS!!)!!

</div>

## Running the Code
1. Clone/download SkinDetector at: https://github.com/pavisj/rppg-pos/tree/master/SkinDetector and place the SkinDetector folder in a place where it's compatible with your path.
2. Install all the required libraries.
3. The main code to execute is `FSM_x_CHROM.py`.
4. To validate the estimated HR, you can take a look at the `.csv` files and run `bland_altman.py` to plot all the graphs.

## Results 📊
<div align="center">

![Figure_1](https://user-images.githubusercontent.com/108513333/237021689-8b19b57d-9e29-42e5-a5d7-51d68463d091.png)
<br>Figure 1 - Example result for estimating heart rate using the proposed CHROM algorithm

![Figure_2](https://user-images.githubusercontent.com/108513333/237021781-2010ba2e-95d9-4de2-8a3d-c6ba96d2d5e5.png)
<br>Figure 2 - Example result for estimating heart rate using the FSM method

![Figure_3](https://user-images.githubusercontent.com/108513333/237021816-72b471dc-6128-4b77-b65c-ec5437d705b0.png)
<br>Figure 3 - Bland-Altman plot for comparing the HR estimation results between CHROM and FSM methods

</div>

## Test Videos 🎥
- [CHROM test](https://youtu.be/qiBjtAyDVHA)
- [CHROM x FSM test](https://youtu.be/e884ERxox64)

<div align="center">

## Acknowledgments

BIG THANKS TO THESE GITHUBS!!: 💖💖
- https://github.com/dnwjddl/remotePPG
- https://github.com/pavisj/rppg-pos
- https://github.com/habom2310/Heart-rate-measurement-using-camera

</div>

--- 
