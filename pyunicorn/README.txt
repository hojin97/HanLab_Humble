
Anaconda 가상환경으로 Python 3.7 version에서 실행

Requirements :
	Numpy 1.14+
	Scipy 1.0+
	Matplotlib 2.0+
	Pandas

1. pyunicorn - 파일에 있는 whl 파일 pip 설치

	python -m pip install python_igraph-0.8.3-cp37-cp37m-win_amd64.whl
	python -m pip install pyunicorn-0.6.1-cp37-cp37m-win_amd64.whl

2. netcdf4-python (for classes Data and NetCDFDictionary) 설치

	pip install netCDF4
	

3. Anaconda 가상환경을 만들어서 설치했을 경우 "C:\Anaconda3\envs\가상환경이름\Lib\site-packages\pyunicorn" 로 이동하여 

__init__.py 의 43번줄 from setup import __version__ 을 주석처리

가상환경을 만들지 않고 구성할 경우, 라이브러리가 설치된 위치로 가서 똑같이 __init__.py .의 43번줄을 주석처리


4. AI_LineGraph.py 실행 (Line Graph : Red - Angle, Blue - RMS)

	AAFT
	32 line : d = Surrogates(original_data=td, silence_level=2).AAFT_surrogates(td) 

	IAAFT (반복횟수 10000번)
	35 line : d = Surrogates(original_data=td, silence_level=2).refined_AAFT_surrogates(td,10000)