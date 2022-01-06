using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace TestEmg
{
    class DataManager
    {
        INT int_data = null;
        RMS rms_data = null;
        Gyro gyro_data = null;
        Angle angle_data = null;
        ArrayList timeStamp = null;

        public DataManager()
        {
            int_data = new INT();
            rms_data = new RMS();
            gyro_data = new Gyro();
            angle_data = new Angle();
            timeStamp = new ArrayList();
        }

        public INT getINT()
        {
            return int_data;
        }

        public RMS getRMS()
        {
            return rms_data;
        }

        public Gyro getGyro()
        {
            return gyro_data;
        }
        public Angle getAngle()
        {
            return angle_data;
        }
        public ArrayList getTimeStamp()
        {
            return timeStamp;
        }

        public string ToString(int i)
        {
            string result = "";
            try
            {
                result = timeStamp[i]+ "\t" + angle_data.getAngleX()[i] + "\t" + angle_data.getAngleY()[i] + "\t" + angle_data.getAngleZ()[i] + "\t" +
                    gyro_data.getGyroX()[i] + "\t" + gyro_data.getGyroY()[i] + "\t" + gyro_data.getGyroZ()[i] + "\t" +
                    rms_data.getRMS()[i] + "\t" + int_data.getINT()[i];
            }catch (ArgumentOutOfRangeException e)
            {
                ;
            }
            return result;
        }

        public void ResetData()
        {
            angle_data.ResetAngle();
            gyro_data.ResetGyro();
            rms_data.ResetRMS();
            int_data.ResetINT();
            timeStamp.Clear();
        }

        public int getSize()
        {
            return angle_data.getAngleX().Count;
        }
    }
}
