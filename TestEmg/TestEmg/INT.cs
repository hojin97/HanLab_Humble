using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace TestEmg
{
    class INT
    {
        private ArrayList int_data = new ArrayList();

        public INT() { }
        public void AddINT(int int_data)
        {
            this.int_data.Add(int_data);
        }

        public ArrayList getINT()
        {
            return int_data;
        }

        public void ResetINT()
        {
            int_data.Clear();
        }
    }
}
