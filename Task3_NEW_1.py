
# coding: utf-8

# In[21]:

import os
import argparse
def main(args=None):
    #if (os.path.exists(".\exam_ddc.ini")) == True:
    #    os.remove(".\exam_ddc.ini")
    parser = argparse.ArgumentParser()   
    parser.add_argument("workmode", type=int, help="WorkMode [0, 1]")
    parser.add_argument("-fn", "--filename", type=str, help="Output filename for workmode 1")
    parser.add_argument("-c", "--channels", type=int, help="Number of channels [1,2,3,4]")
    parser.add_argument("-f", "--frequencies", type=str, help="Frequencies in kHz for channels (delimeter - ',')")
    parser.add_argument("-s", "--sampling_rate", type=str, help="Sampling rate in kHz [12.5, 125, 250, 375, 500, 600, 750, 1000, 1250]")
    args = parser.parse_args()
    w = args.workmode
    fn =args.filename
    c = args.channels
    f = args.frequencies
    s = args.sampling_rate
    
    if w==1 and fn is None:
        raise NameError('When Work_mode=1 filename arg must be set')
    a = {}
    
    if w==0 and fn is not None:
        print('filename argument will be ignored in work_mode=0')
    
    if w==1 and os.path.exists(fn):
        print('WARNING!!! File ' + fn + ' exist already!')      
        fn=fn.split('.')[-2]+'_1.'+fn.split('.')[-1]
        print('Will use ' + fn + ' instead')
    
    # default values
    if c is None:
        c=3
        
    if f is None:
        f="4996,9996,14996"
        
    if s is None:
        s="125"
    
    if c>4 or c<1:
        raise ValueError('Number of channels must be in range [1,4]')
    
    if c==1:
        c_str='0x1'
    if c==2:
        c_str='0x3'
    if c==3:
        c_str='0x7'
    if c==4:
        c_str='0xF'
    
    
    if (',' in f) == False and len(f.split(','))!=1:
        raise ValueError("Error while parsing list of frequencies")
    f_parse=f.split(',')
    
    f_list=[]
    f_str_list=[]
    for f_str in f_parse:
        #print(f_str)
        f_list.append(int(float(f_str)*1000))
        if f_list[-1]<2000 or f_list[-1]>90000000:
            raise ValueError("Frequency is out of range [2,90000] kHz")
        f_str_list.append(str(f_list[-1])+".0")
        
    if s not in ['12.5','125','250','375','500','600','750','1000','1250']:
        raise ValueError("Sampling rate can be one of the this list [12.5,125,250,375,500,600,750,1000,1250] kHz")
    
    if s=='12.5':
        sr_string='f10k-60Md1200n.prg';
    if s=='125':
        sr_string='f104k-60Md120n.prg';
    if s=='250':
        sr_string='f212k-60Md60n.prg';
    if s=='375':
        sr_string='f320k-60Md40n.prg';
    if s=='500':
        sr_string='f396k-60Md30n.prg';
    if s=='600':
        sr_string='f510k-60Md25n.prg';
    if s=='750':
        sr_string='f636k-60Md20n.prg';
    if s=='1000':
        sr_string='f850k-60Md15n.prg';
    if s=='1200':
        sr_string='f1000k-60Md12n.prg';
    
    if len(f_parse)!=c:
        raise ValueError('Length of list of frequencies must be equal to number of channels')
        
    print(w)
    print(fn)
    print(c)
    print(f_str_list)
    print(sr_string)
    
    if len(f_str_list)==1:
        f_str_list.append(f_str_list[-1])
        f_str_list.append(f_str_list[-1])
        f_str_list.append(f_str_list[-1])
    if len(f_str_list)==2:
        f_str_list.append(f_str_list[-1])
        f_str_list.append(f_str_list[-1])
    if len(f_str_list)==3:
        f_str_list.append(f_str_list[-1])

        
    print(f_str_list)
    
    a[0] = "// Файл параметров инициализации для субмодуля ADMDDC4x16, установленного на базовые модули AMBPCX/AMBPCD/AMBPEX2/AMBPEX8\n"
    a[1] = "\n"
    a[2] = "[Option]\n"
    a[3] = "\n"
    a[4] = ";PldFileName=ambpcd_v10_admddc4x16_v30_s.mcs        ;файл прошивки ПЛИС для БМ AMBPCD\n"
    a[5] = ";PldFileName=ambpcd_v10_admddc4x16_v30_s_v11.mcs    ;файл прошивки ПЛИС для БМ AMBPCD\n"
    a[6] = "PldFileName=ambpcx_v10_admddc4x16_v30.mcs       ;файл прошивки ПЛИС для БМ AMBPCX\n"
    a[7] = ";PldFileName=ambpex2_v10_admddc4x16_lx30.mcs        ;файл прошивки ПЛИС для БМ AMBPEX2\n"
    a[8] = ";PldFileName=ambpex2_v10_admddc4x16_lx30_v12.mcs        ;файл прошивки ПЛИС для БМ AMBPEX2\n"
    a[9] = "\n"
    a[10] = "IsPldLoadAlways= 0      ;0-загружать прошивкy, только если она не загружена\n"
    a[11] = "                        ;1-загружать прошивку всегда при запуске программы\n"
    a[12] = "IsSystemMemory= 0       ;0-пользовательская память(скорость до ~90 Мбайт/сек)\n"
    a[13] = "                        ;1-системная память(размер до ~128 Мбайт)\n"
    a[14] = "SamplesPerChannel= 16384       ;число собираемых отсчётов на канал при работе с ISVI\n"
    a[15] = "EnableDDC= 1       ;0-отсчёты с АЦП (DDC выключено), 1-отсчёты с DDC,\n"
    a[16] = "           ;2 - отсчёты с АЦП в SRDRAM / 1-отсчёты с DDC в FIFO\n"
    a[17] = "WorkMode= "+str(w)+"\n"
    a[18] = "                        ;0-сбор данных с последующей записью в файл data.bin (для ISVI), 1-сбор с непосредственной записью данных в файл с заданным именем (не прерывая сбора)\n"
    a[19] = "\n"
    a[20] = "DirFileName= "+fn+"\n"
    a[21] = "DirFileBufSize= 3072       ;размер буфера (Кбайт)при прямой записи в файл\n"
    a[22] = "DirNumBufWrite= 100000     ;число буферов записываемх в файл\n"
    a[23] = "                           ;размер файла равен DirFileBufSize*DirNumBufWrite (Кбайт)\n"
    a[24] = "DirTimeoutSec=50   ;тайм-аут ожидания сбора каждого буфера при прямой записи в файл\n"
    a[25] = "\n"
    a[26] = "DaqIntoMemory=0            ;0-сбор данных в FIFO, 1-сбор данных в SDRAM\n"
    a[27] = "MemSamplesPerChan=131072   ;число собираемых в SDRAM отсчётов на канал\n"
    a[28] = "\n"
    a[29] = "DMA=1              ; всегда использовать 1 (0 только для отладки)\n"
    a[30] = "Cycle=1                ; 0 - однократный сбор, 1- многократный (для прерывания нажмите ESC)\n"
    a[31] = "\n"
    a[32] = "TimeoutSec=5       ;тайм-аут ожидания сбора буфера\n"
    a[33] = "\n"
    a[34] = "DrqFlag=2      ;флаг формирования запроса ПДП для тетрады АЦП или DDC (0 - PAE=1, 1 - RDY=1, 2 - HF=0)\n"
    a[35] = "\n"
    a[36] = "[device0_ddc4x160]\n"
    a[37] = "ClockSource= 0     ;генератор: 0-внутренний, 1-внешний\n"
    a[38] = "InternalClockValue= 60000000   ;значение частоты внутреннего генератора(Гц)\n"
    a[39] = "ExternalClockValue= 60000000.0 ;значение частоты внешнего генератора(Гц)\n"
    a[40] = "AdcBits=1      ; разрядность АЦП для DDC: 0 - 14bit, 1 - 16bit\n"
    a[41] = "AdcGainMask= 0x0       ; маска усилений для АЦП 0x0-0xF (1 в каком-либо разряде - усиление в 1.5 раза соответствующего АЦП)\n"
    a[42] = "Dither= 0      ; 0 -выключен, 1 - включен\n"
    a[43] = "\n"
    a[44] = "ChannelMask= 0x1       ;маска включённых каналов АЦП: 0..0xf(режим EnableDDC=0)\n"
    a[45] = ";ChannelMask=0x2               ; Mask of channels (2 channels)\n"
    a[46] = ";ChannelMask=0x3               ; Mask of channels (3 channels)\n"
    a[47] = "\n"
    a[48] = "DDCChannelMask= "+c_str+"\n"
    a[49] = "\n"
    a[50] = ";DDCChannelMask=0x1        ; DDC Mask of 2 channels\n"
    a[51] = ";DDCChannelMask=0x3        ; DDC Mask of 4 channels\n"
    a[52] = ";DDCChannelMask=0x7        ; DDC Mask of 6 channels\n"
    a[53] = ";DDCChannelMask=0xF        ; DDC Mask of 8 channels\n"
    a[54] = "\n"
    a[55] = "DataFormat= 0      ;формат данных DDC: 0-16 бит, 4-24 бита; АЦП: 0-16 бит, 1-8 бит\n"
    a[56] = "\n"
    a[57] = "\n"
    a[58] = "FrequencyNCO0= "+ f_str_list[0] + "\n"
    a[59] = "FrequencyNCO1= "+ f_str_list[1] + "\n"
    a[60] = "FrequencyNCO2= "+ f_str_list[2] + "\n"
    a[61] = "FrequencyNCO3= "+ f_str_list[3] + "\n"
    a[62] = "FrequencyNCO4= 10700000.0  ;частота NCO DDC канала 4\n"
    a[63] = "FrequencyNCO5= 10700000.0  ;частота NCO DDC канала 5\n"
    a[64] = "FrequencyNCO6= 10700000.0  ;частота NCO DDC канала 6\n"
    a[65] = "FrequencyNCO7= 10700000.0  ;частота NCO DDC канала 7\n"
    a[66] = "FrequencyNCO8= 10700000.0  ;частота NCO DDC канала 8\n"
    a[67] = "FrequencyNCO9= 10700000.0  ;частота NCO DDC канала 9\n"
    a[68] = "FrequencyNCO10= 10700000.0 ;частота NCO DDC канала 10\n"
    a[69] = "FrequencyNCO11= 10700000.0 ;частота NCO DDC канала 11\n"
    a[70] = "FrequencyNCO12= 10700000.0 ;частота NCO DDC канала 12\n"
    a[71] = "FrequencyNCO13= 10700000.0 ;частота NCO DDC канала 13\n"
    a[72] = "FrequencyNCO14= 10700000.0 ;частота NCO DDC канала 14\n"
    a[73] = "FrequencyNCO15= 10700000.0 ;частота NCO DDC канала 15\n"
    a[74] = "\n"
    a[75] = "InputSource=0      ; номер АЦП подключённного ко всем каналам DDC\n"
    a[76] = "InputSource0= 0        ; номер АЦП подключённного к каналу 0 DDC\n"
    a[77] = "InputSource1= 0        ; номер АЦП подключённного к каналу 1 DDC\n"
    a[78] = "InputSource2= 0        ; номер АЦП подключённного к каналу 2 DDC\n"
    a[79] = "InputSource3= 0        ; номер АЦП подключённного к каналу 3 DDC\n"
    a[80] = "InputSource4= 0        ; номер АЦП подключённного к каналу 4 DDC\n"
    a[81] = "InputSource5= 0        ; номер АЦП подключённного к каналу 5 DDC\n"
    a[82] = "InputSource6= 0        ; номер АЦП подключённного к каналу 6 DDC\n"
    a[83] = "InputSource7= 0        ; номер АЦП подключённного к каналу 7 DDC\n"
    a[84] = "InputSource8= 0        ; номер АЦП подключённного к каналу 8 DDC\n"
    a[85] = "InputSource9= 0        ; номер АЦП подключённного к каналу 9 DDC\n"
    a[86] = "InputSource10= 0       ; номер АЦП подключённного к каналу 10 DDC\n"
    a[87] = "InputSource11= 0       ; номер АЦП подключённного к каналу 11 DDC\n"
    a[88] = "InputSource12= 0       ; номер АЦП подключённного к каналу 12 DDC\n"
    a[89] = "InputSource13= 0       ; номер АЦП подключённного к каналу 13 DDC\n"
    a[90] = "InputSource14= 0       ; номер АЦП подключённного к каналу 14 DDC\n"
    a[91] = "InputSource15= 0       ; номер АЦП подключённного к каналу 15 DDC\n"
    a[92] = "\n"
    a[93] = "DDCProgramFile= "+sr_string+"\n"
    a[94] = ";DDCProgramFile= PRGFILES\IsGSM.prg    ; файл конфигурации микросхемы DDC\n"
    a[95] = ";DDCProgramFile=f10k-60Md1200n.prg ; файл конфигурации микросхемы DDC\n"    
    a[96] = ";DDCProgramFile=f212k-60Md60n.prg\n"
    a[97] = ";DDCProgramFile=f320k-60Md40n.prg\n"
    a[98] = ";DDCProgramFile=f396k-60Md30n.prg\n"
    a[99] = ";DDCProgramFile=f510k-60Md25n.prg\n"
    a[100] = ";DDCProgramFile=f636k-60Md20n.prg\n"
    a[101] = ";DDCProgramFile=f850k-60Md15n.prg\n"
    a[102] = ";DDCProgramFile=f1000k-60Md12n.prg\n"
    a[103] = "\n"
    a[104] = "DDCSyncMode= 2        ; режим синхронизации DDC:  1-по старту ввода, 2-программный\n"
    a[105] = "\n"
    a[106] = "\n"
    a[107] = "StartSource= 0        ; источник старта для DDC: 0-программный, 1-ExtSt(компаратор 0), 2-SDX(компаратор 1), 4-SYNX\n"
    a[108] = "StartBaseSource= 0    ; источник старта для ADC: 0-программный, 1-ExtSt(компаратор 0), 2-SDX(компаратор 1), 4-SYNX\n"
    a[109] = "ComparatorThresholdSDX= 0.00  ; порог компаратора для старта от SDX (от -2.5 Вольт до + 2.5 Вольт)\n"
    a[110] = "ComparatorThresholdExtSt= 0.00    ; порог компаратора для старта от ExtSt\n"
    a[111] = "StartInverting=0  ; инверсия сигнала старта: 0-нет, 1-есть\n"
    a[112] = "StartMode=1       ; режим старта: 0-потенциальный, 1-триггерный\n"
    a[113] = "StopSource=0      ; источник останова при триггерном старте\n"
    a[114] = "StopInverting=0       ; инверсия сигнала останов: 0-нет, 1-есть\n"
    a[115] = "\n"
    a[116] = "ReStart=0         ; 1 - use with AcquiredSampleEnable=1 & AcquiredSampleCounter = block size\n"
    a[117] = "AcquiredSampleEnable=0        ; 1 - use with ReStart=1\n"
    a[118] = "AcquiredSampleCounter=2048    ; block size\n"
    a[119] = "\n"
    a[120] = "TitleEnable=0\n"
    a[121] = "TitleSize=10\n"
    a[122] = "DataAlign=0           ; 24bit mode: 0 - align to high-order bit, 1 - align to low-order bit\n"
    a[123] = "\n"
    a[124] = "MasterMode= 1     ; 0 - SLAVE, 1 - SINGLE, 2 - MASTER\n"
    a[125] = "\n"
    i = 0
    cfg = open (".\exam_ddc.ini", "w")
    for i in range(125):
        cfg.writelines(a[i])
if __name__=="__main__":
    main()

