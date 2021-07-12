using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CALCULADORA_V0._2.Clases
{
    class Porciento
    {
        public double Porcentaje(double valor1, double valor2)
        {
            double porci;
            porci = (valor1 * valor2)/100;
            return porci;
        }
    }
}
