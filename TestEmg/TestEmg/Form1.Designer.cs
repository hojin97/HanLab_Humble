namespace TestEmg
{
    partial class frmMain
    {
        /// <summary>
        /// 필수 디자이너 변수입니다.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 사용 중인 모든 리소스를 정리합니다.
        /// </summary>
        /// <param name="disposing">관리되는 리소스를 삭제해야 하면 true이고, 그렇지 않으면 false입니다.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 디자이너에서 생성한 코드

        /// <summary>
        /// 디자이너 지원에 필요한 메서드입니다.
        /// 이 메서드의 내용을 코드 편집기로 수정하지 마십시오.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.txtMessage = new System.Windows.Forms.TextBox();
            this.lbGraph = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.lbDisp = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.lbStatus = new System.Windows.Forms.Label();
            this.tmrDraw = new System.Windows.Forms.Timer(this.components);
            this.txtSensor = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.lbINTG = new System.Windows.Forms.Label();
            this.Btn_Stop = new System.Windows.Forms.Button();
            this.Btn_Start = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // txtMessage
            // 
            this.txtMessage.Location = new System.Drawing.Point(12, 12);
            this.txtMessage.Multiline = true;
            this.txtMessage.Name = "txtMessage";
            this.txtMessage.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.txtMessage.Size = new System.Drawing.Size(488, 134);
            this.txtMessage.TabIndex = 0;
            // 
            // lbGraph
            // 
            this.lbGraph.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lbGraph.Location = new System.Drawing.Point(12, 153);
            this.lbGraph.Name = "lbGraph";
            this.lbGraph.Size = new System.Drawing.Size(488, 321);
            this.lbGraph.TabIndex = 24;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(408, 476);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(92, 12);
            this.label1.TabIndex = 25;
            this.label1.Text = "RMS (Strength)";
            // 
            // lbDisp
            // 
            this.lbDisp.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lbDisp.Location = new System.Drawing.Point(506, 154);
            this.lbDisp.Name = "lbDisp";
            this.lbDisp.Size = new System.Drawing.Size(501, 659);
            this.lbDisp.TabIndex = 26;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(863, 818);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(144, 12);
            this.label2.TabIndex = 27;
            this.label2.Text = "Angle Value & Gyro Value";
            // 
            // lbStatus
            // 
            this.lbStatus.AutoSize = true;
            this.lbStatus.Location = new System.Drawing.Point(926, 28);
            this.lbStatus.Name = "lbStatus";
            this.lbStatus.Size = new System.Drawing.Size(40, 12);
            this.lbStatus.TabIndex = 28;
            this.lbStatus.Text = "Status";
            // 
            // tmrDraw
            // 
            this.tmrDraw.Tick += new System.EventHandler(this.TmrDraw_Tick);
            // 
            // txtSensor
            // 
            this.txtSensor.Location = new System.Drawing.Point(506, 12);
            this.txtSensor.Multiline = true;
            this.txtSensor.Name = "txtSensor";
            this.txtSensor.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.txtSensor.Size = new System.Drawing.Size(371, 134);
            this.txtSensor.TabIndex = 29;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(474, 818);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(25, 12);
            this.label3.TabIndex = 31;
            this.label3.Text = "INT";
            // 
            // lbINTG
            // 
            this.lbINTG.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lbINTG.Location = new System.Drawing.Point(11, 496);
            this.lbINTG.Name = "lbINTG";
            this.lbINTG.Size = new System.Drawing.Size(488, 317);
            this.lbINTG.TabIndex = 32;
            // 
            // Btn_Stop
            // 
            this.Btn_Stop.Enabled = false;
            this.Btn_Stop.Location = new System.Drawing.Point(910, 103);
            this.Btn_Stop.Name = "Btn_Stop";
            this.Btn_Stop.Size = new System.Drawing.Size(75, 23);
            this.Btn_Stop.TabIndex = 33;
            this.Btn_Stop.Text = "Stop";
            this.Btn_Stop.UseVisualStyleBackColor = true;
            this.Btn_Stop.Click += new System.EventHandler(this.Save_button);
            // 
            // Btn_Start
            // 
            this.Btn_Start.Location = new System.Drawing.Point(910, 59);
            this.Btn_Start.Name = "Btn_Start";
            this.Btn_Start.Size = new System.Drawing.Size(75, 23);
            this.Btn_Start.TabIndex = 34;
            this.Btn_Start.Text = "Start";
            this.Btn_Start.UseVisualStyleBackColor = true;
            this.Btn_Start.Click += new System.EventHandler(this.Btn_Start_Click);
            // 
            // frmMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1019, 839);
            this.Controls.Add(this.Btn_Start);
            this.Controls.Add(this.Btn_Stop);
            this.Controls.Add(this.lbINTG);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.txtSensor);
            this.Controls.Add(this.lbStatus);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.lbDisp);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.txtMessage);
            this.Controls.Add(this.lbGraph);
            this.Name = "frmMain";
            this.Text = "Myo Emg";
            this.Load += new System.EventHandler(this.frmMain_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox txtMessage;
        private System.Windows.Forms.Label lbGraph;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lbDisp;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label lbStatus;
        private System.Windows.Forms.Timer tmrDraw;
        private System.Windows.Forms.TextBox txtSensor;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label lbINTG;
        private System.Windows.Forms.Button Btn_Stop;
        public System.Windows.Forms.Button Btn_Start;
    }
}

