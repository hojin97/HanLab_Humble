using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace TestEmg
{
    class Gyro
    {
        private ArrayList X = new ArrayList();                      // Gyro X
        private ArrayList Y = new ArrayList();                      // Gyro Y
        private ArrayList Z = new ArrayList();                      // Gyro Z

        public Gyro() { }
        public void AddGyro(int x, int y, int z)
        {
            this.X.Add(x);
            this.Y.Add(y);
            this.Z.Add(z);
        }

        public ArrayList getGyroX()
        {
            return X;
        }
        public ArrayList getGyroY()
        {
            return Y;
        }
        public ArrayList getGyroZ()
        {
            return Z;
        }
        public void ResetGyro()
        {
            X.Clear();
            Y.Clear();
            Z.Clear();
        }
    }
}
