# PowerFlowCalculation
电力系统潮流计算 using Python through Newton-Raphson method

参考 《电力系统分析（第二版）》（夏道止 主编，中国电力出版社）附录

* 输入输出： 
输入输出均采用文件方式，
输入数据格式与要求均与上述附录相同，注意数据块之间的空行严格为一行。

* 画收敛图 DrawConvergenceGraph.py： 
程序在计算之后画出了迭代收敛图，
横坐标为 迭代次数，纵坐标为 最大功率误差。
同时与PQ分解法的收敛图对比，硬编码在程序中的数据来自于与 input.txt 默认数据相同的测例，可参考上述书籍 Page 115。
一般可作为该项目的入口文件。

* makeInput.py：
基于原始的输入数据input.txt，通过改变输入倍数(times)等其他因素生成新的输入数据存入input1.txt。
在设置好times等参数后可直接运行DrawConvergenceGraph.py（作为入口文件运行），全自动化得出基于input1.txt输入数据的输出。

* drawTimesComparisonGraph.py:
timesResultComparison.txt来自于几次对makeInput.py中输入线路(gv.line)times的更改而生成的输入数据对应的数据结果的整理。
基于此txt用该py画出了其对比图分析线路参数与其收敛的情况。
