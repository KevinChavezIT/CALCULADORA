using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CALCULADORA_V0._2
{
    public partial class Form1 : Form
    {     
        double Num1 = 0;
        double Num2 = 0;
        double respuesta;
        string operacion;

        public Form1()
        {
            InitializeComponent();
        }

        Clases.Suma GetSuma = new Clases.Suma();
        Clases.Resta GetResta = new Clases.Resta();
        Clases.Multiplicacion GetMultiplicacion = new Clases.Multiplicacion();
        Clases.Division GetDivision = new Clases.Division();
        Clases.Porciento GetPorciento = new Clases.Porciento();

        private void aggnum(string numero)
        {
            if (txtpantalla.Text == "0")
            {
                txtpantalla.Text = numero;
            }
            else
                txtpantalla.Text += numero;
        }

        private void btncero_Click(object sender, EventArgs e)
        {
           
            if (txtpantalla.Text == "0")
            {
                return;
            }
            else
                txtpantalla.Text = txtpantalla.Text + "0";
        }

        private void btnone_Click(object sender, EventArgs e)
        {
            aggnum("1");
        }
        private void btndos_Click(object sender, EventArgs e)
        {
            aggnum("2");
        }
        private void btntres_Click(object sender, EventArgs e)
        {
            aggnum("3");
        }
        private void btncuatro_Click(object sender, EventArgs e)
        {
            aggnum("4");
        }
        private void btncinco_Click(object sender, EventArgs e)
        {
            aggnum("5");
        }
        private void btnseis_Click(object sender, EventArgs e)
        {
            aggnum("6");
        }
        private void btnsiete_Click(object sender, EventArgs e)
        {
            aggnum("7");
        }
        private void btnocho_Click(object sender, EventArgs e)
        {
            aggnum("8");
        }
        private void btnnueve_Click(object sender, EventArgs e)
        {
            aggnum("9");
        }
        private void btnsigno_Click(object sender, EventArgs e)
        {
           
            Num1 = Convert.ToDouble(txtpantalla.Text);
            lbhistorial.Text = txtpantalla.Text + operacion;
            Num1 *= -1;
            txtpantalla.Text = Num1.ToString();
        }
    
        private void btnpunto_Click(object sender, EventArgs e)
        {         
            if (txtpantalla.Text.Contains(","))
            {

            }
            else           
                txtpantalla.Text =txtpantalla.Text + ",";           
        }

    private void btnmas_Click(object sender, EventArgs e)
        {          
            lbhistorial.Text = "";
            operacion = "+";

            
            Num1 = double.Parse(txtpantalla.Text);
            lbhistorial.Text = lbhistorial.Text + txtpantalla.Text + "+";
            txtpantalla.Text = "0";
            btnmas.Enabled = false;
        }

        private void btnmenos_Click(object sender, EventArgs e)
        {
            lbhistorial.Text = "";
            operacion = "-";

            Num1 = double.Parse(txtpantalla.Text);
            lbhistorial.Text = lbhistorial.Text + txtpantalla.Text + "-";
            txtpantalla.Text = "0";
            btnmenos.Enabled = false;
        }

        private void btnpor_Click(object sender, EventArgs e)
        {
            lbhistorial.Text = "";            
            operacion = "*";

            Num1 = double.Parse(txtpantalla.Text);
            lbhistorial.Text = lbhistorial.Text + txtpantalla.Text + "*";
            txtpantalla.Text="0";
            btnpor.Enabled = false;           
        }

        private void btndivision_Click(object sender, EventArgs e)
        {
            lbhistorial.Text = "";
            operacion = "/";

            Num1 = double.Parse(txtpantalla.Text);          
            lbhistorial.Text = lbhistorial.Text + txtpantalla.Text + "÷";
            txtpantalla.Text = "0";
            btndivision.Enabled = false;
        }

        private void btnporciento_Click(object sender, EventArgs e)
        {
            lbhistorial.Text = "";
            operacion = "%";

            Num2 = double.Parse(txtpantalla.Text);          

            txtpantalla.Text = Convert.ToString((Num1 )* Num2/100);           
            lbhistorial.Text = lbhistorial.Text + txtpantalla.Text;         
            btnporciento.Enabled = true;
            btnpor.Enabled = true;
        }

        private void btnigual_Click(object sender, EventArgs e)
        {           
            Num2 = double.Parse(txtpantalla.Text);

            btnmas.Enabled = true;
            btnmenos.Enabled = true;
            btndivision.Enabled = true;
            btnpor.Enabled = true;
            btnporciento.Enabled = true;

            double su;
            double re;
            double mu;
            double di;
            double porci;

            switch (operacion)
            {
             
                case "+":                 
                    su = GetSuma.Sumar((Num1), (Num2));
                    lbhistorial.Text = lbhistorial.Text + txtpantalla.Text ;
                    txtpantalla.Text = su.ToString();
                    break;

                case "-":
                    re = GetResta.Restar((Num1), (Num2));
                    lbhistorial.Text = lbhistorial.Text + txtpantalla.Text;
                    txtpantalla.Text = re.ToString();
                    break;

                case "*":
                    mu = GetMultiplicacion.Multiplicar((Num1), (Num2));
                    lbhistorial.Text = lbhistorial.Text + txtpantalla.Text;
                    txtpantalla.Text = mu.ToString();
                    break;
                case "/":
                    if (Num2 == 0)
                    {
                        lbhistorial.Text = "No se puede dividir entre 0!";
                    }
                    else
                    {
                        di = GetDivision.Dividir((Num1), (Num2));
                        lbhistorial.Text = lbhistorial.Text + txtpantalla.Text;
                        txtpantalla.Text = di.ToString();
                    }                   
                    break;
                case "%":
                    porci = GetPorciento.Porcentaje((Num1), (Num2)/100);
                    
                    break;                 
            }
        }
        private void btnborrar_Click(object sender, EventArgs e)
        {
            txtpantalla.Text="0" ;
        }

        private void btnborarrtodo_Click(object sender, EventArgs e)
        {
            txtpantalla.Clear();
            lbhistorial.Text = "";
            btnmas.Enabled = true;
            btnmenos.Enabled = true;
            btndivision.Enabled = true;
            btnpor.Enabled = true;
            btnporciento.Enabled = true;
        }

        private void btneliminar_Click(object sender, EventArgs e)
        {
            if (txtpantalla.Text.Length == 1)
            {
                txtpantalla.Text = "0";
            }             
            else
                txtpantalla.Text = txtpantalla.Text.Substring(0, txtpantalla.Text.Length - 1);
        }

        private void btncuadrado_Click(object sender, EventArgs e)
        {
            lbhistorial.Text = "";

            Num1 = double.Parse(txtpantalla.Text);
            respuesta = Num1;
            lbhistorial.Text = lbhistorial.Text + txtpantalla.Text + "²";
            txtpantalla.Text = Math.Pow(Num1, 2).ToString();
        }

        private void btnraiz_Click(object sender, EventArgs e)
        {           
            lbhistorial.Text = "";

            Num1 = double.Parse(txtpantalla.Text);
            respuesta = Num1;
            lbhistorial.Text = "√" + lbhistorial.Text + txtpantalla.Text;
            txtpantalla.Text = Math.Sqrt(Num1).ToString();
        }     
    }
}
