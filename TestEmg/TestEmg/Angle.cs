using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace TestEmg
{
    class Angle
    {
        private ArrayList X = new ArrayList();                      // Angle X
        private ArrayList Y = new ArrayList();                      // Angle Y
        private ArrayList Z = new ArrayList();                      // Angle Z

        public Angle() { }

        public void AddAngle(int x, int y, int z)
        {
            this.X.Add(x);
            this.Y.Add(y);
            this.Z.Add(z);
        }

        public ArrayList getAngleX()
        {
            return X;
        }
        public ArrayList getAngleY()
        {
            return Y;
        }
        public ArrayList getAngleZ()
        {
            return Z;
        }

        public void ResetAngle()
        {
            X.Clear();
            Y.Clear();
            Z.Clear();
        }
    }
}

