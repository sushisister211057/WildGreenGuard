# WildGreenGuard


- [WildGreenGuard](#wildgreenguard)
  - [Object](#object)
  - [Invasive plants candidate (so far)](#invasive-plants-candidate-so-far)
  - [Flow](#flow)
  - [Members](#members)
  - [Jobs](#jobs)
  - [References](#references)


## Object

- Currently...
  - Invaded species have been problems for a long time. 
  - Though, some apps provide servers But ...
  - Gain more public attention on the invaded species.

- Our project tries to... 
  - Real-time identify invasive plants in Taiwan.
  - accuracy to ...
  - precision to ...
  
- We are going to use ...
  - Build model with Tensorflow 
  - Line with FastApi
  - Web with Javascript and Django

- Flow diagram is like ...
  - a
  - b
  - c

- Our 

## Invasive plants candidate (so far)
|入侵種|相似植物|note|
|-|-|-|
|銀合歡||資料庫|
|銀膠菊||資料庫|
|小花蔓澤蘭||拍攝|
|象草|芒草|拍攝|
|大花咸豐草||拍攝|
|孟仁草||拍攝|
|加拿大蓬|野茼蒿|拍攝|
|巴拉草|星草, 牛筋草|拍攝|
|星草|巴拉草, 牛筋草|拍攝|
|粗毛小米菊|長柄菊|拍攝|
|昭和草|
|豬草|


## Flow

1. 
    1. Webscrap images of species listed in [database](https://gisd.biodiv.tw/tw/).
    2. Take the photos Manually.
2. _(choose one)_
    1. Use [Roboflow](https://roboflow.com/) to annotate the roi, then export the yolov8.yml for training.
    2. Use [LabelImg](https://github.com/HumanSignal/labelImg) to annotate the roi, then export the .xml file for training.
3. _(choose one)_
    1. Apply the data into keras [YOLOV8Detector](https://keras.io/api/keras_cv/models/tasks/yolo_v8_detector/).
    2. Apply the data into [Ultralytics](https://docs.ultralytics.com/).
4. _(choose one or both)_
    1. Connect the model to [Line bot](https://github.com/line/line-bot-sdk-python) for using.
    2. Connect to web [Django](https://www.djangoproject.com/) for using. (
   [tensorflow.js](https://js.tensorflow.org/api/latest/#Tensors), [tensorflow.js_Basic use](https://www.tensorflow.org/js/tutorials/conversion/import_keras, ), [onnx.js](https://onnxruntime.ai/docs/api/js/index.html))
    3. Perform the model on edge device with [tensorflow lite](https://www.tensorflow.org/lite).  

## Members

Leader: 17_張家銘   
Members: 04_梁鈞翔, 12_許庭瑊, 16_呂星緯, 22_張雅婷, 31_何耿廷, 34_張大謙 

## Jobs
|Job|Subgroup Leader|Subgroup Members|
|-|-|-|
|Collect data|17_張家銘|@All|
|Build Model|04_梁鈞翔|34_張大謙|
|Build Linebot|12_許庭瑊|22_張雅婷|
|Build Web|16_呂星緯|34_張大謙, 31_何耿廷|
|Cloud deploy|22_張雅婷|12_許庭瑊, 16_呂星緯|




## References

1. [台灣物種名錄](https://taicol.tw/zh-hant/)
2. [認識植物](http://kplant.biodiv.tw/) 
3. [農業知識入口網](https://kmweb.moa.gov.tw/)
4. [Global Core Biodata Resource (GBIF)](https://www.gbif.org/zh-tw/)  
<!-- https://www.imageclef.org/PlantCLEF2020
[銀膠菊與艾草的差異(107/6/23)](https://youtu.be/-tp9ENdx8-k) -->
