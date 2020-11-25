# TRT_Ultra_Fast_Lane_Detect

TRT_Ultra_Fast_Lane_Detect is an implementation of converting Ultra fast lane detection into tensorRT model by Python API.  There are some other works in our project are listed below:

- The detection procedure is encapsulated.
- The pytorch model is transformed into onnx model and trt model.
- The trt models have different versions: FP32, FP16, INT8.
- The Tusimple data set can be compressed by /calibration_data/make_mini_tusimple.py. There are redundancies in the Tusimple data set, for only the 20-th images are used. The compressed tusimple data set takes about 1GB.

The original project, model, and paper is available from https://github.com/cfzd/Ultra-Fast-Lane-Detection



### Ultra-Fast-Lane-Detection

PyTorch implementation of the paper "[Ultra Fast Structure-aware Deep Lane Detection](https://arxiv.org/abs/2004.11757)".

Updates: Our paper has been accepted by ECCV2020.

[![alt text](https://github.com/cfzd/Ultra-Fast-Lane-Detection/raw/master/vis.jpg)](https://github.com/cfzd/Ultra-Fast-Lane-Detection/blob/master/vis.jpg)

The evaluation code is modified from [SCNN](https://github.com/XingangPan/SCNN) and [Tusimple Benchmark](https://github.com/TuSimple/tusimple-benchmark).

Caffe model and prototxt can be found [here](https://github.com/Jade999/caffe_lane_detection).



### Trained models

The trained models can be obtained by the following table:

| Dataset  | Metric paper | Metric This repo | Avg FPS on GTX 1080Ti | Model                                                        |
| -------- | ------------ | ---------------- | --------------------- | ------------------------------------------------------------ |
| Tusimple | 95.87        | 95.82            | 306                   | [GoogleDrive](https://drive.google.com/file/d/1WCYyur5ZaWczH15ecmeDowrW30xcLrCn/view?usp=sharing)/[BaiduDrive(code:bghd)](https://pan.baidu.com/s/1Fjm5yVq1JDpGjh4bdgdDLA) |
| CULane   | 68.4         | 69.7             | 324                   | [GoogleDrive](https://drive.google.com/file/d/1zXBRTw50WOzvUp6XKsi8Zrk3MUC3uFuq/view?usp=sharing)/[BaiduDrive(code:w9tw)](https://pan.baidu.com/s/19Ig0TrV8MfmFTyCvbSa4ag) |



### Installation

`pip3 install -r requirement.txt`



### Convert

Above all, you have to train or download a 4 lane model trained by the Ultra Fast Lane Detection pytorch version. You have to change some codes, if you want to use different lane number. 



Now, we have a trained pytorch model "model.pth". 

 1.  Use torch2onnx.py to convert the the model into  onnx model.  You should rename your model as "model.pth". The original configuration file is configs/tusimple_4.py.

    `python3 configs/${config_file}.py `

 2.  Use onnx_to_tensorrt.py to convert the onnx model in to tensorRT model (FP16, FP32).

    `python3 onnx_to_tensorrt.py -p ${mode_in_fp16_or_fp32} --model ${model_name}` 

 3.  Use onnx_to_tensorrt.py to convert the onnx model in to tensorRT model (INT8).

    `python3 onnx_to_tensorrt.py  --model ${model_name}`

 4.  Run tensorrt_run.py to activate detection 

    `python tensorrt_run.py --model ${model_name}` 

    

### Evalutaion

|            | Pytorch | libtorch | tensorRT(FP32) | tensorRT(FP16) | tensorRT(int8) |
| :--------: | :-----: | :------: | :------------: | :------------: | :------------: |
|  GTX1060   |  55fps  |  55fps   |     55fps      |  Unsupported   |     99fps      |
| Xavier AGX |  27fps  |  27fps   |       --       |       --       |       --       |
| Jetson T1  |  8fps   |   8fps   |      8fps      |     16fps      |  Unsupported   |

Where "--" denotes the experiment  haven't been completed yet.