// Myo
using MyoSharp.Communication;
using MyoSharp.Device;
//using MyoSharp.ConsoleSample.Internal;
using MyoSharp.Exceptions;
using MyoSharp.Poses;
// OpenJigWare
using OpenJigWare;
using System;
using System.Drawing;
using System.Windows.Forms;
using System.Collections.Generic;
//Math.net >> Generate Sine Waveforms & using fft
using MathNet.Numerics;
using MathNet.Numerics.IntegralTransforms;
//using Complex Number & Charts
using System.Numerics;
using System.Windows.Forms.DataVisualization.Charting;

using System.Threading;
using System.Diagnostics;
using System.IO;

namespace TestEmg
{
    public partial class frmMain : Form
    {

        private Thread cpuThread;
        private double[] cpuArray = new double[30];
        bool CollectionFlag = false;

        public frmMain()
        {
            InitializeComponent();

        }


        #region Variable
        #region For OpenJigWare
        // Graphic
        private Ojw.CGraph m_CGrap = null;
        private Ojw.CGraph m_CGrap2 = null;
        private Ojw.CGraph m_CGrap3 = null;

        // Timer
        private Ojw.CTimer m_CTId = new Ojw.CTimer();
        private Ojw.CTimer m_CTId_Graph = new Ojw.CTimer();


        #endregion For OpenJigWare

        #region For Myo
        IChannel m_myoChannel;
        IHub m_myoHub;
        IHeldPose m_myoPos;

        #endregion For Myo
        #endregion Variable


        #region forFFT
        List<Complex> cplx = new List<Complex>();

        #endregion forFFT
        double Intrms = 0;


        private void frmMain_Load(object sender, EventArgs e)
        {
            Ojw.CMessage.Init(txtMessage);
            //Ojw.CMessage.Init(txtSensor);

            // Graph Init
            m_CGrap = new Ojw.CGraph(lbGraph, lbGraph.Width, Color.White, null,
                //for 8 channel
                //Color.Red,
                //Color.Blue,
                //Color.Green,
                //Color.Cyan,
                //Color.Violet,
                //Color.Purple,
                //Color.Magenta,
                //Color.Orange

               Color.Black
               // Color.ForestGreen
                );
            m_CGrap2 = new Ojw.CGraph(lbDisp, lbDisp.Width, Color.White, null,
                                    Color.Red, Color.Blue, Color.Black, //angle
                                    Color.Red, Color.Blue, Color.Black  //gyro  -
                                    );
            m_CGrap3 = new Ojw.CGraph(lbINTG, lbINTG.Width, Color.White, null,
                                    Color.ForestGreen);

            tmrDraw.Enabled = true;

            #region Myo
            m_myoChannel = Channel.Create(ChannelDriver.Create(ChannelBridge.Create(), MyoErrorHandlerDriver.Create(MyoErrorHandlerBridge.Create())));
            m_myoHub = Hub.Create(m_myoChannel);

            // 이벤트 등록            
            m_myoHub.MyoConnected += new EventHandler<MyoEventArgs>(myoHub_MyoConnected);
            m_myoHub.MyoDisconnected += new EventHandler<MyoEventArgs>(myoHub_MyoDisconnected);

            // start listening for Myo data
            m_myoChannel.StartListening();
            #endregion Myo



        }

        #region Myo
        private void myoHub_MyoConnected(object sender, MyoEventArgs e)
        {
            Ojw.CMessage.Write(String.Format("Myo {0} has connected!", e.Myo.Handle));
            e.Myo.Vibrate(VibrationType.Short);
            //e.Myo.Unlock(UnlockType.Hold);
            Ojw.CMessage.Write("Connected(Myo)");

            m_anHandle[m_nCnt_Handle] = e.Myo.Handle.ToInt32();

            #region Sensor
            e.Myo.AccelerometerDataAcquired += new EventHandler<AccelerometerDataEventArgs>(Myo_AccelerometerDataAcquired);
            e.Myo.GyroscopeDataAcquired += new EventHandler<GyroscopeDataEventArgs>(Myo_GyroscopeDataAcquired);
            #endregion Sensor

            m_nCnt_Handle++;

            m_CTId.Set();
            e.Myo.EmgDataAcquired += Myo_EmgDataAcquired;



            e.Myo.SetEmgStreaming(true);
        }
        private void myoHub_MyoDisconnected(object sender, MyoEventArgs e)
        {
            e.Myo.SetEmgStreaming(false);
            e.Myo.EmgDataAcquired -= Myo_EmgDataAcquired;


            Ojw.CMessage.Write("Disconnected(Myo)");
        }
        private void Myo_EmgDataAcquired(object sender, EmgDataEventArgs e)
        {

            //float amp = 0.7f; OJW 수정 불가 int only graph 
            double rms = 
                Math.Sqrt((Math.Pow(e.EmgData.GetDataForSensor(0), 2) + 
                Math.Pow(e.EmgData.GetDataForSensor(1), 2) + 
                Math.Pow(e.EmgData.GetDataForSensor(2), 2) + 
                Math.Pow(e.EmgData.GetDataForSensor(3), 2) +
                Math.Pow(e.EmgData.GetDataForSensor(4), 2) + 
                Math.Pow(e.EmgData.GetDataForSensor(5), 2) + 
                Math.Pow(e.EmgData.GetDataForSensor(6), 2) + 
                Math.Pow(e.EmgData.GetDataForSensor(7), 2)) / 8);

            int mav = (Math.Abs(e.EmgData.GetDataForSensor(0)) + Math.Abs(e.EmgData.GetDataForSensor(1)) + Math.Abs(e.EmgData.GetDataForSensor(2)) + Math.Abs(e.EmgData.GetDataForSensor(3)) +
                      Math.Abs(e.EmgData.GetDataForSensor(4)) + Math.Abs(e.EmgData.GetDataForSensor(5)) + Math.Abs(e.EmgData.GetDataForSensor(6)) + Math.Abs(e.EmgData.GetDataForSensor(7))) / 8;
   

            //rms값을 complex로 변환 , theta == 0; cplx 리스트에 저장                  //RMS가 과연 적합??
            cplx.Add(from_Polar(rms, 0));


            // Display Emg Text Data (1000 ms interval = 1 second)
            if (m_CTId.Get() >= 1000)
            {
                m_CTId.Set();
                Ojw.CMessage.Write(String.Format("Emg = {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}",

                    e.EmgData.GetDataForSensor(0),
                    e.EmgData.GetDataForSensor(1),
                    e.EmgData.GetDataForSensor(2),
                    e.EmgData.GetDataForSensor(3),
                    e.EmgData.GetDataForSensor(4),
                    e.EmgData.GetDataForSensor(5),
                    e.EmgData.GetDataForSensor(6),
                    e.EmgData.GetDataForSensor(7),
                    rms
                    //Intrms
                    )) ;
            }

            // Display Emg Graphic Data (100 ms interval)
            if (m_CTId_Graph.Get() >= 100)
            {
                Intrms += rms;
                //int len = cplx.ToArray().Length;
                //double HZ;

                //Complex tmp = 0;
                //Complex[] temp = FFT(cplx.ToArray());

                //for (int i = 0; i < len; i++)                //과연 dft에서 얻어진 spectrum data의 summation이 frequency 그래프 변환에 유효한가?
                //{
                //    tmp += temp[i];
                //}
                //Complex follow = tmp / 2;
                //int follow_idx = 0;

                //for(int i = 0; i < temp.Length; i++)
                //{
                //    if ((Math.Truncate(temp[i].Real * 100) / 100) == (Math.Truncate(follow.Real * 100 / 100))){
                //        follow_idx = i;
                //    }
                //}

                //HZ = follow_idx / 2;

                m_CTId_Graph.Set();

                int data_rms = (int)(Math.Round(rms));
                int data_int = (int)Math.Round(Intrms);

                if (CollectionFlag)
                {
                    dm.getRMS().AddRMS(data_rms);
                    dm.getINT().AddINT(data_int);
                }
                else
                {
                    Intrms = 0;
                }

                m_CGrap.Push(
                        //e.EmgData.GetDataForSensor(0),
                        //e.EmgData.GetDataForSensor(1),
                        //e.EmgData.GetDataForSensor(2),
                        //e.EmgData.GetDataForSensor(3),
                        //e.EmgData.GetDataForSensor(4),
                        //e.EmgData.GetDataForSensor(5),
                        //e.EmgData.GetDataForSensor(6),
                        //e.EmgData.GetDataForSensor(7)

                        data_rms
                        //(int)(Math.Round(HZ))
                        //(int)tmp.Real       //theta=0 , 어차피 허수부 존재 X
                        );

                m_CGrap.OjwDraw();

                m_CGrap3.Push(data_int/40);
                m_CGrap3.OjwDraw();
            }
        }
        #endregion Myo

        static int deviceCnt = 1;

        private int[] m_anHandle = new int[deviceCnt];
        private int m_nCnt_Handle = 0;

        #region Acc
        private float[] m_afAcc = new float[3];
        private void Myo_AccelerometerDataAcquired(object sender, AccelerometerDataEventArgs e)
        {

            if (m_anHandle[0] == e.Myo.Handle.ToInt32())
            {
                m_afAcc[0] = e.Accelerometer.X; // / 57.1f*90.0f;
                m_afAcc[1] = e.Accelerometer.Y;// / 57.7f*90.0f;
                m_afAcc[2] = e.Accelerometer.Z;// / 57.1f*90.0f;}

            }
        }
        #endregion Acc

        #region Gyro
        private float[] m_afGyro = new float[3];
        private void Myo_GyroscopeDataAcquired(object sender, GyroscopeDataEventArgs e)
        {
            if (m_anHandle[0] == e.Myo.Handle.ToInt32())
            {

                m_afGyro[0] = e.Gyroscope.X;
                m_afGyro[1] = e.Gyroscope.Y;
                m_afGyro[2] = e.Gyroscope.Z;
            }

        }
        #endregion Gyro

        private double period = 0;
        private double sec = 0;
        private void TmrDraw_Tick(object sender, EventArgs e)
        {

            float fMulti = 0.5f;
            float[] afAngle = new float[3];
           

            #region Change ACC Value -> Angle
            float fTmp;
            fTmp = m_afAcc[1] * m_afAcc[1] + m_afAcc[2] * m_afAcc[2];

            if (fTmp == 0.0f)
            {
                fTmp = (float)Ojw.CMath.Zero();
            }
            afAngle[0] = (float)Ojw.CMath.R2D((float)Math.Atan(m_afAcc[0] / (float)Math.Sqrt(fTmp)));

            fTmp = m_afAcc[2] * m_afAcc[2] + m_afAcc[0] * m_afAcc[0];

            if (fTmp == 0.0f)
            {
                fTmp = (float)Ojw.CMath.Zero();
            }
            afAngle[1] = (float)Ojw.CMath.R2D((float)Math.Atan(m_afAcc[1] / (float)Math.Sqrt(fTmp)));

            fTmp = m_afAcc[0] * m_afAcc[0] + m_afAcc[1] * m_afAcc[1];
            float fTmp2 = m_afAcc[2];
            if (fTmp2 == 0.0f)
            {
                fTmp2 = (float)Ojw.CMath.Zero();
            }
            afAngle[2] = (float)Ojw.CMath.R2D((float)Math.Atan((float)Math.Sqrt(fTmp) / fTmp2));
            #endregion Change ACC Value -> Angle

            #region Graph
            //push data

            //if (m_CTId_Graph.Get() >= 100)
            //{
            //    m_CTId_Graph.Set();
            m_CGrap2.Push(
           (int)Math.Round(afAngle[0] * fMulti), (int)Math.Round(afAngle[1] * fMulti), (int)Math.Round(afAngle[2] * fMulti),

           (int)Math.Round(m_afGyro[0] * fMulti), (int)Math.Round(m_afGyro[1] * fMulti), (int)Math.Round(m_afGyro[2] * fMulti)
           // (int)Math.Round(m_afAcc[0] * fMulti), (int)Math.Round(m_afAcc[1] * fMulti), (int)Math.Round(m_afAcc[2] * fMulti)
           );
            m_CGrap2.OjwDraw();  //plot
                                 //}
            #endregion Graph

            #region SensorText
            //Ojw.CMessage.Init(txtSensor);


            //if (m_CTId.Get() >= 1000)
            //{

            //    m_CTId.Set();

            // Angle
            int angle_x = (int)Math.Round(afAngle[0] * fMulti);
            int angle_y = (int)Math.Round(afAngle[1] * fMulti);
            int angle_z = (int)Math.Round(afAngle[2] * fMulti);

            // Gyro
            int gyro_x = (int)Math.Round(m_afGyro[0] * fMulti);
            int gyro_y = (int)Math.Round(m_afGyro[1] * fMulti);
            int gyro_z = (int)Math.Round(m_afGyro[2] * fMulti);

            // input timeStamp, Angle, Data.
            if (CollectionFlag)
            {
                period += m_CTId.Get();
                if(period >= 1000)
                {
                    sec += 1;
                }
                dm.getTimeStamp().Add(sec/10);
                dm.getAngle().AddAngle(angle_x, angle_y, angle_z);
                dm.getGyro().AddGyro(gyro_x, gyro_y, gyro_z);
            }
            else
            {
                period = 0;
                sec = 0;
            }
            

            Ojw.CMessage.Write(txtSensor, String.Format("Angle X: {0}, Y: {1}, Z: {2}, \n Gyro X: {3}, Y: {4}, Z: {5} ",

                angle_x,
                angle_y,
                angle_z,
                gyro_x,
                gyro_y,
                gyro_z
               //(int)Math.Round(m_afAcc[0] * fMulti),
               //(int)Math.Round(m_afAcc[1] * fMulti),
               //(int)Math.Round(m_afAcc[2] * fMulti)
               ));

            //}
            #endregion SensorText
        }


        //극 좌표계에서 복소수로 치환, int형 데이터는 theta가 0이 될 것( 회전값 X)
        public static Complex from_Polar(double r, double theta) //theta should be Radian member
        {
            Complex data = new Complex(r * Math.Cos(theta), r * Math.Sin(theta));
            return data;
        }

        //DFT (array of spectrum data)
        public static Complex[] DFT(Complex[] x)
        {
            int N = x.Length;
            Complex[] X = new Complex[N];

            for (int k = 0; k < N; k++)
            {
                X[k] = new Complex(0, 0);

                for (int n = 0; n < N; n++)
                {
                    Complex temp = from_Polar(1, -2 * Math.PI * n * k / N);
                    temp *= x[n];
                    X[k] += temp;
                }
            }
            return X;
        }
        
        public static Complex[] FFT(Complex[] x)
        {
            int N = x.Length;
            Complex[] X = new Complex[N];

            Complex[] d, D, e, E;

            if (N == 1)
            {
                X[0] = x[0];
                return X;
            }

            int k;

            e = new Complex[N / 2];
            d = new Complex[N / 2];

            for (k = 0; k < N / 2; k++)
            {
                e[k] = x[2 * k];
                d[k] = x[2 * k + 1];
            }

            //recursive 
            D = FFT(d);
            E = FFT(e);


            for (k = 0; k < N; k++)
            {
                Complex temp = from_Polar(1, -2 * Math.PI * k / N);
                D[k] *= temp;
            }

            for(k=0; k < N / 2; k++)
            {
                X[k] = E[k] + D[k];
                X[k + N / 2] = E[k] - D[k];
            }
            return X;
        }



        StreamWriter writer = null;

        DataManager dm = new DataManager();

        private void Btn_Start_Click(object sender, EventArgs e)
        {
            string title = DateTime.Now.ToString("MMdd") + "_" + DateTime.Now.ToString("HHmm");
            //string title = DateTime.Now.Month.ToString() + DateTime.Now.Day.ToString() +"_" + DateTime.Now.Hour.ToString() + DateTime.Now.Minute.ToString();
            writer = new StreamWriter("../../Data/Humble_" + title +".txt");
            CollectionFlag = true;
            Btn_Stop.Enabled = true;
            Btn_Start.Enabled = false;
        }

        private void Save_button(object sender, EventArgs e)
        {
            CollectionFlag = false;

            for (int i =0; i < dm.getSize(); i++)
            {
                writer.WriteLine(dm.ToString(i));
            }
            writer.Close();

            MessageBox.Show("Save !");
            Btn_Start.Enabled = true;
            Btn_Stop.Enabled = false;
        }

        


        //private void getPerformanceCounters()
        //{
        //    var cpuPerfCounter = new PerformanceCounter("Processor Information", "% Processor Time", "_Total");

        //    while (true)
        //    {
        //        cpuArray[cpuArray.Length - 1] = Math.Round(cpuPerfCounter.NextValue(), 0);

        //        Array.Copy(cpuArray, 1, cpuArray, 0, cpuArray.Length - 1);

        //        if (chtPSD.IsHandleCreated)
        //        {
        //            this.Invoke((MethodInvoker)delegate { UpdatechtPSD(); });
        //        }
        //        else
        //        {
        //            //.....
        //        }

        //        Thread.Sleep(1000);

        //    }

        //}

        //private void UpdatechtPSD()
        //{
        //    chtPSD.Series["Series1"].Points.Clear();

        //    for (int i = 0; i < cpuArray.Length - 1; ++i)
        //    {
        //        chtPSD.Series["Series1"].Points.AddY(cpuArray[i]);
        //    }
        //}

        //private void Button1_Click(object sender, EventArgs e)
        //{
        //    cpuThread = new Thread(new ThreadStart(this.getPerformanceCounters));
        //    cpuThread.IsBackground = true;
        //    cpuThread.Start();
        //}

        //public void PlotWaveform(int secondHarm, int thirdHarm, double secondPH, double thirdPH)
        //{
        //    Chart chart1 = new Chart();
        //    chart1.Series["Waveform"].Points.Clear();
        //    chart1.Series["Second Harmonic"].Points.Clear();
        //    chart1.Series["Third Harmonic"].Points.Clear();

        //    Complex32[] ir= { 3 };
        //    //Generate fundamental, 2nd & 3rd harmonic waveforms using MathNet libraries
        //    double[] fundamental = Generate.Sinusoidal(numsamples);
        //    Fourier.Forward(ir, FourierOptions.NoScaling);
        //}

    }
}
