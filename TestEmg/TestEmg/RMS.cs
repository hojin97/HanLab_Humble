using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace TestEmg
{
    class RMS
    {
        private ArrayList rms = new ArrayList();

        public RMS() { }
        public void AddRMS(int rms)
        {
            this.rms.Add(rms);
        }

        public ArrayList getRMS()
        {
            return rms;
        }
     
        public void ResetRMS()
        {
            rms.Clear();
        }
    }
}
