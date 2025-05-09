#!/usr/bin/env python3
from env import Vsat, U_fwd
from argparse import ArgumentParser


def step_up_l_calculate(Freq: float, Vin: float, Vout: float, Iout: float):
    T = 1/Freq
    t_ratio = (Vout+U_fwd-Vin)/(Vin-Vsat)
    t_off = T/(t_ratio + 1)
    t_on = T-t_off
    C_t = 4*0.00001*t_on
    i_pk = 2*Iout*(t_ratio+1)
    L = ((Vin-Vsat)/i_pk)*t_on
    print(
        f"Freq = {Freq/1000:.2f} kHz  C = {C_t*1e12:.2f} pF  L >= {L*1000000:.2f} uH")


def step_down_l_calculate(Freq: float, Vin: float, Vout: float, Iout: float):
    T = 1/Freq
    t_ratio = (Vout+U_fwd)/(Vin-Vsat-Vout)
    t_off = T/(t_ratio + 1)
    t_on = T-t_off
    C_t = 4*0.00001*t_on
    i_pk = 2*Iout
    L = ((Vin-Vsat-Vout)/i_pk)*t_on
    print(
        f"Freq = {Freq/1000:.2f} kHz  C = {C_t*1e12:.2f} pF  L >= {L*1000000:.2f} uH")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Расчёт парметров DC-DC конветора на ИМС MC34063")
    parser.add_argument('v_in', type=float, help="входное напряжение, В")
    parser.add_argument('v_out', type=float, help="выходное напряжение, В")
    parser.add_argument('i_out', type=float, help="выходной ток, мА")
    parser.add_argument(
        'r1', type=float, help="сопротивление нижнего резистора, кОм")
    args = parser.parse_args()
    Vin = args.v_in
    Vout = args.v_out
    Iout = args.i_out/1000
    Idrv = (Iout/10)+0.007
    Rdrv = Vin/Idrv
    R1 = args.r1*1000
    R2 = ((Vout/1.25)-1)*R1
    print(f"Резистор нижний = {R1/1000} кОм\nРезистор верхний = {R2/1000} кОм\nРезистор драйвера (8 нога) <= {Rdrv} Ом")
    for fr in range(20, 51, 5):
        if (Vout >= Vin):
            step_up_l_calculate(Freq=fr*1000, Vin=Vin, Vout=Vout, Iout=Iout)
        else:
            step_down_l_calculate(Freq=fr*1000, Vin=Vin, Vout=Vout, Iout=Iout)
