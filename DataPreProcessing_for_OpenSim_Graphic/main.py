filepath = './Biceps_motion/'
filename = 'reverse_curl_basic.sto'

time = 0
SC_y = [-19.0, 0.0]
SC_z = [5.002, 0.0]
SC_x = [4.278, 0.0]
AC_y = [33.0, 0.0]
AC_z = [-6.769, 0.0]
AC_x = [-5.092, 0.0]
GH_y = [78.967, 0.0]
GH_z = [11.134, 0.0]
GH_yy = [-77.896, 0.0]
EL_x = [25.0, 0.0]
PS_y = [33, 0.0]

# 20ms 기준. 1초 => 50개
dataFrame_num = 80
EL_angle = 2.375
GH_yy_angle = 0.5
GH_z_angle = 0.5

with open(filepath+filename, 'w') as file:
    file.write("ReverseCurl_Basic_simulation\n")
    file.write("nRows = "+ str(dataFrame_num) +"\n")
    file.write("nColumns = 12\n")
    file.write("inDegrees=yes\n")
    file.write("endheader\n")
    file.write("\n")
    file.write("time"
               "\tSC_y"
               "\tSC_z"
               "\tSC_x"
               "\tAC_y"
               "\tAC_z"
               "\tAC_x"
               "\tGH_y"
               "\tGH_z"
               "\tGH_yy"
               "\tEL_x"
               "\tPS_y\n")

    # file.write("time\t/jointset/sc1/SC_y/value\t/jointset/sc1/SC_y/speed"
    #            "\t/jointset/sc2/SC_z/value\t/jointset/sc2/SC_z/speed"
    #            "\t/jointset/sc3/SC_x/value\t/jointset/sc3/SC_x/speed"
    #            "\t/jointset/ac1/AC_y/value\t/jointset/ac1/AC_y/speed"
    #            "\t/jointset/ac2/AC_z/value\t/jointset/ac2/AC_z/speed"
    #            "\t/jointset/ac3/AC_x/value\t/jointset/ac3/AC_x/speed"
    #            "\t/jointset/gh1/GH_y/value\t/jointset/gh1/GH_y/speed"
    #            "\t/jointset/gh2/GH_z/value\t/jointset/gh2/GH_z/speed"
    #            "\t/jointset/gh3/GH_yy/value\t/jointset/gh3/GH_yy/speed"
    #            "\t/jointset/hu/EL_x/value\t/jointset/hu/EL_x/speed"
    #            "\t/jointset/hu/PS_y/value\t/jointset/hu/PS_y/speed\n")
    for i in range(dataFrame_num):
        file.write(str('{0:.6f}'.format(time))
                   + "\t" + str('{0:.6f}'.format(SC_y[0]))
                   + "\t" + str('{0:.6f}'.format(SC_z[0]))
                   + "\t" + str('{0:.6f}'.format(SC_x[0]))
                   + "\t" + str('{0:.6f}'.format(AC_y[0]))
                   + "\t" + str('{0:.6f}'.format(AC_z[0]))
                   + "\t" + str('{0:.6f}'.format(AC_x[0]))
                   + "\t" + str('{0:.6f}'.format(GH_y[0]))
                   + "\t" + str('{0:.6f}'.format(GH_z[0]))
                   + "\t" + str('{0:.6f}'.format(GH_yy[0]))
                   + "\t" + str('{0:.6f}'.format(EL_x[0]))
                   + "\t" + str('{0:.6f}'.format(PS_y[0])) + "\n")
        # file.write(str(time)
        #            + "\t" + str(SC_y[0]) + "\t" + str(SC_y[1])
        #            + "\t" + str(SC_z[0]) + "\t" + str(SC_z[1])
        #            + "\t" + str(SC_x[0]) + "\t" + str(SC_x[1])
        #            + "\t" + str(AC_y[0]) + "\t" + str(AC_y[1])
        #            + "\t" + str(AC_z[0]) + "\t" + str(AC_z[1])
        #            + "\t" + str(AC_x[0]) + "\t" + str(AC_x[1])
        #            + "\t" + str(GH_y[0]) + "\t" + str(GH_y[1])
        #            + "\t" + str(GH_z[0]) + "\t" + str(GH_z[1])
        #            + "\t" + str(GH_yy[0]) + "\t" + str(GH_yy[1])
        #            + "\t" + str(EL_x[0]) + "\t" + str(EL_x[1])
        #            + "\t" + str(PS_y[0]) + "\t" + str(PS_y[1]) + "\n")
        time += 0.02
        if EL_x[0] < 25:
            EL_angle = 2.375
        elif EL_x[0] > 120:
            EL_angle = -2.375
        EL_x[0] += EL_angle

        ## Triceps + type == elbow
        # if AC_z[0] < -8:
        #     AC_z_angle = 0.5
        # elif AC_z[0] > 0:
        #     AC_z_angle = -0.5
        # AC_z[0] += AC_z_angle
        #
        # if GH_z[0] < -10:
        #     GH_z_angle = 0.5
        # elif GH_z[0] >0:
        #     GH_z_angle = -0.5
        # GH_z[0] += GH_z_angle

        ## if type == wrist,
        # if GH_yy[0] < -40:
        #     GH_yy_angle = 0.5
        # elif GH_yy[0] > -30:
        #     GH_yy_angle = -0.5
        # GH_yy[0] += GH_yy_angle
    file.close()
