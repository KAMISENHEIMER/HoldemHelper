# HoldemHelper
**By Kaden Misenheimer and Danny Holt**  
## Installation
`npm install`

**Note:** If instead using the conda env 'cv' as listed in class, you will need these additional dependencies:  
```npm install pokerkit```  
```npm install opencv```  
```npm install numpy```  

*Extra additions for yolo version*  
```npm install ultralytics```  
```npm install omegaconf```  

## Usage  
```py src/main_yolo.py [IMAGE] [# PLAYERS]```  
*Optionally specify number of simulations*  
```py src/main_yolo.py [IMAGE] [# PLAYERS] --sims [# SIMULATIONS]```  