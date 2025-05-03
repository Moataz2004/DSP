from tkinter import *
from tkinter import filedialog, messagebox
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
home = Tk()
home.geometry("800x500")
home.title("Digital Signal Processing")
home.config(bg="lightblue")


def SignalSamplesAreEqual(file_name, samples):
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break

    if len(expected_samples) != len(samples):
        print(len(expected_samples))
        print(len(samples))
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one")
            return
    print("Test case passed successfully")



#====================================================TASK1=============================================================#
sg=[]
def genSignal():
    tl = Toplevel()
    tl.geometry("800x450")
    tl.title("Generating Signal")
    tl.config(bg="lightblue")
    ok = IntVar()
    rdbutton1 = Radiobutton(tl, text="Sin", value=1, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton2 = Radiobutton(tl, text="Cos", value=2, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton1.place(x=50, y=30)
    rdbutton2.place(x=175, y=30)
    A = IntVar()
    l1 = Label(tl, text="A (Amplitude):", font=("Helvetica", 25), background="lightblue")
    l1.place(x=50, y=100)
    et1 = Entry(tl, textvariable=A, font=("Helvetica", 16))
    et1.place(x=280, y=110)
    Theta = DoubleVar()
    l2 = Label(tl, text="Phase Shift Theta:", font=("Helvetica", 25), background="lightblue")
    l2.place(x=50, y=170)
    et2 = Entry(tl, textvariable=Theta, font=("Helvetica", 16))
    et2.place(x=330, y=180)
    F = IntVar()
    l3 = Label(tl, text="F (The Analog Frequency):", font=("Helvetica", 25), background="lightblue")
    l3.place(x=50, y=240)
    et3 = Entry(tl, textvariable=F, font=("Helvetica", 16))
    et3.place(x=450, y=250)
    Fs = IntVar()
    l4 = Label(tl, text="Fs (The Sampling Frequency):", font=("Helvetica", 25), background="lightblue")
    l4.place(x=50, y=310)
    et4 = Entry(tl, textvariable=Fs, font=("Helvetica", 16))
    et4.place(x=500, y=320)
    def generate():
        try:
            amp = float(A.get())
            theta = float(Theta.get())
            f = float(F.get())
            fs = float(Fs.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")
            return

        if fs < 2 * f:
            messagebox.showerror("Error", "Sampling frequency must satisfy the Nyquist criterion.")
            return

        t = np.linspace(0, 1, int(fs))  # Time domain: 1 second duration
        n = np.arange(int(fs))  # Discrete time points

        if ok.get() == 1:
            continuous_signal = amp * np.sin(2 * np.pi * f * t + theta)
            discrete_signal = amp * np.sin(2 * np.pi * (f / fs) * n + theta)
            title = "Sine"
        else:
            continuous_signal = amp * np.cos(2 * np.pi * f * t + theta)
            discrete_signal = amp * np.cos(2 * np.pi * (f / fs) * n + theta)
            title = "Cosine"

        sg = discrete_signal
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
        ax1.plot(t, continuous_signal)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Amplitude")
        ax1.set_title(f"{title} Continuous")
        ax2.scatter(n, discrete_signal)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Amplitude")
        ax2.set_title(f"{title} Discrete")
        plt.tight_layout()
        plt.show()
        print(len(sg))
    def Compare():
     SignalSamplesAreEqual(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), sg)


    btn1 = Button(tl, text="Generating", background="teal", foreground="white", width=15, height=3, command=generate, font=("Helvetica", 12))
    btn1.place(x=570, y=30)
    btn2 = Button(tl, text="Compare", background="teal", foreground="white", width=15, height=3, command=Compare,
                  font=("Helvetica", 12))
    btn2.place(x=570, y=100)


def RSignal():
    tl = Toplevel()
    tl.geometry("600x500")
    tl.title("Read a Signal")
    tl.config(bg="lightblue")

    def load_signal_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    signal_type = int(file.readline().strip())
                    is_periodic = int(file.readline().strip())
                    N1 = int(file.readline().strip())

                    if signal_type == 0:
                        time_samples = []
                        amplitudes = []

                        for _ in range(N1):
                            index, amp = map(float, file.readline().split())
                            time_samples.append(index)
                            amplitudes.append(amp)

                        continuous_time = np.linspace(min(time_samples), max(time_samples), N1)
                        continuous_signal = np.interp(continuous_time, time_samples, amplitudes)


                        plot_signals(continuous_time, continuous_signal, time_samples, amplitudes)

                    elif signal_type == 1:
                        freqs = []
                        amps = []
                        phases = []

                        for _ in range(N1):
                            freq, amp, phase = map(float, file.readline().split())
                            freqs.append(freq)
                            amps.append(amp)
                            phases.append(phase)

                        t = np.linspace(0, 1, N1)
                        signal = np.zeros_like(t)

                        for i in range(N1):
                            signal += amps[i] * np.cos(2 * np.pi * freqs[i] * t + phases[i])

                        discrete_time = np.linspace(0, 1, N1)
                        discrete_signal = np.interp(discrete_time, t, signal)


                        plot_signals(t, signal, discrete_time, discrete_signal)

                    else:
                        messagebox.showerror("Error", "Invalid signal type in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def plot_signals(continuous_time, continuous_signal, discrete_time, discrete_signal):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
        ax1.plot(continuous_time, continuous_signal)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Amplitude")
        ax1.set_title("Continuous Signal")
        ax2.scatter(discrete_time, discrete_signal)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Amplitude")
        ax2.set_title("Discrete Signal")
        plt.tight_layout()
        plt.show()

    btn_load = Button(tl, text="Load Signal", background="teal", foreground="white", width=15, height=3, command=load_signal_from_file, font=("Helvetica", 12))
    btn_load.place(x=200, y=200)


#====================================================TASK2=============================================================#
final = []
sg1 =[]
sg2 = []
def Arithmetic_Operations():
    tl = Toplevel()
    tl.geometry("600x500")
    tl.title("Arithmetic Operations")
    tl.config(bg="lightblue")

    ok = IntVar()
    rdbutton1 = Radiobutton(tl, text="Addition", value=1, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton2 = Radiobutton(tl, text="Subtraction", value=2, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton3 = Radiobutton(tl, text="Multiplication", value=3, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton4 = Radiobutton(tl, text="Squaring", value=4, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton5 = Radiobutton(tl, text="Normalization", value=5, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton6 = Radiobutton(tl, text="Accumulation", value=6, bg="lightblue", font=("Helvetica", 25), variable=ok)
    rdbutton1.place(x=50, y=30)
    rdbutton2.place(x=250, y=30)
    rdbutton3.place(x=50, y=100)
    rdbutton4.place(x=300, y=100)
    rdbutton5.place(x=50, y=170)
    rdbutton6.place(x=300, y=170)
    Mul = IntVar()
    l1 = Label(tl, text="Enetr A Number to Multiply:", font=("Helvetica", 18), background="lightblue")
    l1.place(x=25, y=235)
    et1 = Entry(tl, textvariable=Mul, font=("Helvetica", 16))
    et1.place(x=340, y=240)
    Nor = StringVar()
    l2 = Label(tl, text="Enetr A Rang to Normalize:", font=("Helvetica", 18), background="lightblue")
    l2.place(x=25, y=280)
    et2 = Entry(tl, textvariable=Nor, font=("Helvetica", 16))
    et2.place(x=340, y=285)

    def load_signal_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    signal_type = int(file.readline().strip())
                    is_periodic = int(file.readline().strip())
                    N1 = int(file.readline().strip())

                    if signal_type == 0:
                        time_samples = []
                        amplitudes = []

                        for _ in range(N1):
                            index, amp = map(int, file.readline().split())
                            time_samples.append(index)
                            amplitudes.append(amp)

                        continuous_time = np.linspace(min(time_samples), max(time_samples), N1)
                        continuous_signal = np.interp(continuous_time, time_samples, amplitudes)
                        return continuous_signal

                    elif signal_type == 1:
                        freqs = []
                        amps = []
                        phases = []

                        for _ in range(N1):
                            freq, amp, phase = map(int, file.readline().split())
                            freqs.append(freq)
                            amps.append(amp)
                            phases.append(phase)

                        t = np.linspace(0, 1, N1)
                        signal = np.zeros_like(t)

                        for i in range(N1):
                            signal += amps[i] * np.cos(2 * np.pi * freqs[i] * t + phases[i])

                        discrete_time = np.linspace(0, 1, N1)
                        discrete_signal = np.interp(discrete_time, t, signal)
                        return discrete_signal

                    else:
                        messagebox.showerror("Error", "Invalid signal type in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def load1() :
        global sg1
        sg1 = load_signal_from_file()
        sg1 = sg1.tolist()


    def load2() :
        global sg2
        sg2 = load_signal_from_file()
        sg2 = sg2.tolist()

    def Compare():
     SignalSamplesAreEqual(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), final)



    def Gen():
        global sg1 , sg2 , final

        if ok.get() == 1:
            for s1, s2 in zip(sg1, sg2):
                final.append(s1 + s2)
        elif ok.get() == 2:
            for s1, s2 in zip(sg1, sg2):
                final.append(abs(s1 - s2))
        elif ok.get() == 3:
            if Mul.get() == -1:
                for s in sg1:
                    final.append(-s)
            else:
                for s in sg1:
                    final.append(s * Mul.get())
        elif ok.get() == 4:
            final = [s ** 2 for s in sg1]
        elif ok.get() == 5:
            min_value = min(sg1)
            max_value = max(sg1)
            if Nor.get() == '-1 to 1':
                for i in sg1 :
                    x = (2 * (i - min_value) / (max_value - min_value)) - 1
                    final.append(x)

            elif Nor.get() == '0 to 1':
                for i in sg1:
                    x = (i - min_value) / (max_value - min_value)
                    final.append(x)

        else:
            list1= [0] * len(sg1)
            for i  in range(len(sg1)):
                if i == 0:
                    list1[0] = sg1[0]
                else:
                    list1[i] = sg1[i] + list1[i - 1]
            final.extend(list1)

        print(final)
        final.clear()

        t = np.linspace(0, 1, len(final))
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
        ax1.plot(t, final)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Amplitude")
        ax2.scatter(t, final)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Amplitude")
        plt.tight_layout()
        plt.show()




    btn_load1 = Button(tl, text="Load Signal 1", background="teal", foreground="white", width=15, height=3, command=load1, font=("Helvetica", 12))
    btn_load1.place(x=50, y=330)
    btn_load2 = Button(tl, text="Load Signal 2", background="teal", foreground="white", width=15, height=3,
                       command=load2, font=("Helvetica", 12))
    btn_load2.place(x=200, y=330)
    btn_gen = Button(tl, text="Generate Signal", background="teal", foreground="white", width=15, height=3,
                     command=Gen, font=("Helvetica", 12))
    btn_gen.place(x=350, y=330)
    btn2 = Button(tl, text="Compare", background="teal", foreground="white", width=15, height=3, command=Compare,
                  font=("Helvetica", 12))
    btn2.place(x=200, y=400)

#====================================================TASK3=============================================================#
Final = []
Sg = []
Encoded = []
Js = []
Errors = []
Levels = 0
def Quantization():
    tl = Toplevel()
    tl.geometry("600x500")
    tl.title("Quantization")
    tl.config(bg="lightblue")

    qt = IntVar()
    rdbutton1 = Radiobutton(tl, text="Levels", value=1, bg="lightblue", font=("Helvetica", 25), variable=qt)
    rdbutton2 = Radiobutton(tl, text="Bits", value=2, bg="lightblue", font=("Helvetica", 25), variable=qt)
    rdbutton1.place(x=50, y=50)
    rdbutton2.place(x=50, y=120)
    lb = IntVar()
    et1 = Entry(tl, textvariable=lb, font=("Helvetica", 20))
    et1.place(x=220, y=100)

    def load_signal_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    signal_type = int(file.readline().strip())
                    is_periodic = int(file.readline().strip())
                    N1 = int(file.readline().strip())

                    if signal_type == 0:
                        time_samples = []
                        amplitudes = []

                        for _ in range(N1):
                            index, amp = map(float, file.readline().split())
                            time_samples.append(index)
                            amplitudes.append(amp)
                        return amplitudes

                    else:
                        messagebox.showerror("Error", "Invalid signal type in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def load() :
        global Sg
        Sg = load_signal_from_file()
        print(Sg)

    def QuantizationTest1(file_name, Your_EncodedValues, Your_QuantizedValues):
        expectedEncodedValues = []
        expectedQuantizedValues = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                # process line
                L = line.strip()
                if len(L.split(' ')) == 2:
                    L = line.split(' ')
                    V2 = str(L[0])
                    V3 = float(L[1])
                    expectedEncodedValues.append(V2)
                    expectedQuantizedValues.append(V3)
                    line = f.readline()
                else:
                    break
        if ((len(Your_EncodedValues) != len(expectedEncodedValues)) or (
                len(Your_QuantizedValues) != len(expectedQuantizedValues))):
            print(len(Your_EncodedValues))
            print(len(expectedEncodedValues))
            print(len(Your_QuantizedValues))
            print(len(expectedQuantizedValues))
            print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_EncodedValues)):
            if (Your_EncodedValues[i] != expectedEncodedValues[i]):
                print(
                    "QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one")
                return
        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                print(
                    "QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one")
                return
        print("QuantizationTest1 Test case passed successfully")

    def QuantizationTest2(file_name, Your_IntervalIndices, Your_EncodedValues, Your_QuantizedValues, Your_SampledError):
        expectedIntervalIndices = []
        expectedEncodedValues = []
        expectedQuantizedValues = []
        expectedSampledError = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                # process line
                L = line.strip()
                if len(L.split(' ')) == 4:
                    L = line.split(' ')
                    V1 = int(L[0])
                    V2 = str(L[1])
                    V3 = float(L[2])
                    V4 = float(L[3])
                    expectedIntervalIndices.append(V1)
                    expectedEncodedValues.append(V2)
                    expectedQuantizedValues.append(V3)
                    expectedSampledError.append(V4)
                    line = f.readline()
                else:
                    break
        if (len(Your_IntervalIndices) != len(expectedIntervalIndices)
                or len(Your_EncodedValues) != len(expectedEncodedValues)
                or len(Your_QuantizedValues) != len(expectedQuantizedValues)
                or len(Your_SampledError) != len(expectedSampledError)):
            print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_IntervalIndices)):
            if (Your_IntervalIndices[i] != expectedIntervalIndices[i]):
                print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one")
                return
        for i in range(len(Your_EncodedValues)):
            if (Your_EncodedValues[i] != expectedEncodedValues[i]):
                print(
                    "QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one")
                return

        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                print(
                    "QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one")
                return
        for i in range(len(expectedSampledError)):
            if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
                continue
            else:
                print(
                    "QuantizationTest2 Test case failed, your SampledError have different values from the expected one")
                return
        print("QuantizationTest2 Test case passed successfully")

    def Compare():
        if qt.get() == 1:
            QuantizationTest2(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), Js, Encoded, Final,
                              Errors)
        else:
            QuantizationTest1(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), Encoded, Final)

    def decimal_to_binary(decimal_number, num_digits):
        if decimal_number == 0:
            return "0".zfill(num_digits)
        binary_number = ""
        while decimal_number > 0:
            remainder = decimal_number % 2
            binary_number = str(remainder) + binary_number
            decimal_number = decimal_number // 2
        if len(binary_number) < num_digits:
            binary_number = binary_number.zfill(num_digits)
        return binary_number

    def Gen():
        global Sg
        if qt.get() == 1:
            Levels = int(lb.get())
            Bits = int(np.log(Levels) / np.log(2))
        else:
            Bits = int(lb.get())
            Levels = pow(2, Bits)
        sg_Max = max(Sg)
        sg_Min = min(Sg)
        Delta = (sg_Max - sg_Min) / Levels


        Intervals = []
        while(Levels) :
            mid = (sg_Min + (Delta +sg_Min )) / 2
            mid = round(mid, 3)
            interval = [round(sg_Min, 3) , mid , round((Delta +sg_Min ), 3) ]
            Intervals.append(interval)
            sg_Min = (Delta + sg_Min)
            Levels = Levels - 1

        i = 0
        while i < len(Sg):
            j = 0
            while j < len(Intervals):
                if Sg[i] >= Intervals[j][0] and Sg[i] <= Intervals[j][2]:
                    x = decimal_to_binary(j, Bits)
                    e = Intervals[j][1] - Sg[i]
                    Final.append(Intervals[j][1])
                    Encoded.append(x)
                    Js.append(j + 1)
                    Errors.append(round(e, 3))
                    break
                j += 1
            i += 1

        print(Js)
        print(Encoded)
        print(Intervals)
        print(Final)
        Sg.clear()

    btn_load1 = Button(tl, text="Load Signal", background="teal", foreground="white", width=15, height=3,
                       command=load, font=("Helvetica", 12))
    btn_load1.place(x=70, y=300)
    btn_gen = Button(tl, text="Generate", background="teal", foreground="white", width=15, height=3,
                     command=Gen, font=("Helvetica", 12))
    btn_gen.place(x=230, y=300)
    btn2 = Button(tl, text="Compare", background="teal", foreground="white", width=15, height=3, command=Compare,
                  font=("Helvetica", 12))
    btn2.place(x=390, y=300)
#====================================================TASK4=============================================================#
Fur = []
Fl = []
Fin = []
A = []
ph = []
x_ax = []
DC = []
DCF = []
def Frequency_Domain():
    tl = Toplevel()
    tl.geometry("600x500")
    tl.title("Frequency Domain")
    tl.config(bg="lightblue")

    Fr = IntVar()
    rdbutton1 = Radiobutton(tl, text="DFT", value=1, bg="lightblue", font=("Helvetica", 25), variable=Fr)
    rdbutton2 = Radiobutton(tl, text="IDFT", value=2, bg="lightblue", font=("Helvetica", 25), variable=Fr)
    rdbutton3 = Radiobutton(tl, text="DCT", value=3, bg="lightblue", font=("Helvetica", 25), variable=Fr)
    rdbutton1.place(x=50, y=50)
    rdbutton2.place(x=50, y=120)
    rdbutton3.place(x=50, y=190)
    l1 = Label(tl, text="Fs :", font=("Helvetica", 20),
               background="lightblue")
    l1.place(x=200, y=60)
    nan = DoubleVar()
    et1 = Entry(tl, textvariable=nan, font=("Helvetica", 24))
    et1.place(x=200, y=100)
    l2 = Label(tl, text="Number of Elements to save :", font=("Helvetica", 20),
               background="lightblue")
    l2.place(x=200, y=150)
    M = IntVar()
    et1 = Entry(tl, textvariable=M, font=("Helvetica", 24))
    et1.place(x=200, y=190)

    def SignalComapreAmplitude(SignalInput=[], SignalOutput=[]):
        if len(SignalInput) != len(SignalOutput):
            print("Signal Comapre Amplitude Test case failed,your signal have different length from the expected one")
        else:
            for i in range(len(SignalInput)):
                if abs(SignalInput[i] - SignalOutput[i]) > 0.001:
                    print(SignalInput[i])
                    print(SignalOutput[i])
                    print("Signal Comapre Amplitude Test case failed, your Signal Values have different values from the expected one")
                    return False
            print("Signal Comapre Amplitude Test case passed successfully")

    def SignalComaprePhaseShift(SignalInput=[], SignalOutput=[]):
        if len(SignalInput) != len(SignalInput):
            print("Signal Comapre Phase Shift Test case failed,your signal have different length from the expected one")

        else:
            for i in range(len(SignalInput)):
                A = round(SignalInput[i])
                B = round(SignalOutput[i])
                if abs(A - B) > 0.0001:
                    print("Signal Comapre  Phase Shift Test case failed, your Signal Values have different values from the expected one")
                    return False
                elif A != B:
                    print("Signal Comapre Phase Shift Test case failed")
                    return False
            print("Phase Shift Test case passed successfully")


    def load_signal_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    signal_type = int(file.readline().strip())
                    is_periodic = int(file.readline().strip())
                    N1 = int(file.readline().strip())

                    if signal_type == 0:
                        time_samples = []
                        amplitudes = []

                        for _ in range(N1):
                            index, amp = map(float, file.readline().split())
                            time_samples.append(index)
                            amplitudes.append(amp)
                        return time_samples,amplitudes

                    else:
                        messagebox.showerror("Error", "Invalid signal type in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def load() :
        global Fur
        global Fl
        Fl , Fur = load_signal_from_file()

    def Compare():
        x, y = load_signal_from_file()
        if Fr.get() == 1:
            SignalComapreAmplitude(x, A)
            SignalComaprePhaseShift(y,ph)
        elif Fr.get() == 2:
            SignalComapreAmplitude(y, Fin)
        else:
            SignalSamplesAreEqual(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), Fin)
    def Gen():
        global Fur
        global Fin
        global A
        global ph
        global x_ax
        global DC
        global DCF

        if Fr.get() == 1 :
            N = len(Fur)
            for k in range(N):
                real = 0
                img = 0
                for n in range(N):
                    angle = -2 * np.pi * k * n / N
                    real += Fur[n] * np.cos(angle)
                    img += Fur[n] * np.sin(angle)
                Fin.append([real , img])
            i = 0
            while i < len(Fin):
                x = pow(Fin[i][0] , 2)
                y = pow(Fin[i][1], 2)
                A.append(np.sqrt(x + y))
                ph.append(np.atan2(Fin[i][1], Fin[i][0]))
                i += 1
            omega = (2.0 * 3.14 )/(N *(1/nan.get()))
            j = 1
            while j <= len(Fin):
                x_ax.append(omega * j)
                j += 1
            print(x_ax)
            print(A)
            print(ph)
            g = 0
            while g < len(Fin):
                if g ==0 :
                    DC.append([0,0])
                else :
                    DC.append([Fin[g][0],Fin[g][1]])
                g += 1
            i = 0
            real = []
            img = []
            while i < len(DC):
                real.append(Fl[i] * np.cos(DC[i]))
                img.append(Fl[i] * np.sin(DC[i]))
                i += 1
            N = len(real)
            signal_reconstructed = np.zeros(N)
            for n in range(N):
                for k in range(N):
                    angle = 2 * np.pi * k * n / N
                    signal_reconstructed[n] += real[k] * np.cos(angle) - img[k] * np.sin(angle)
                signal_reconstructed[n] /= N
                DCF.append(signal_reconstructed[n])
            print(DCF)
            plt.figure()
            plt.subplot(2, 1, 1)
            plt.stem(x_ax, A)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')
            plt.title('Frequency vs Amplitude')
            plt.grid(True)
            plt.subplot(2, 1, 2)
            plt.stem(x_ax, ph)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Phase (radians)')
            plt.title('Frequency vs Phase')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        elif Fr.get() == 2  :
            i = 0
            real = []
            img = []
            while i < len(Fur):
                real.append(Fl[i] * np.cos(Fur[i]))
                img.append(Fl[i] * np.sin(Fur[i]))
                i += 1
            N = len(real)
            signal_reconstructed = np.zeros(N)
            for n in range(N):
                for k in range(N):
                    angle = 2 * np.pi * k * n / N
                    signal_reconstructed[n] += real[k] * np.cos(angle) - img[k] * np.sin(angle)
                signal_reconstructed[n] /= N
                Fin.append(signal_reconstructed[n])
        else:
            print(Fur)
            N = len(Fur)
            for k in range(N):
                sq = np.sqrt(2 / N)
                s = 0
                for n in range(N):
                    s += Fur[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))
                s *= sq
                Fin.append(s)


        print(Fin)

    def save_coefficients(coefficients, m, filename):
        with open(filename, 'w') as f:
            for i in range(m):
                f.write(f"{coefficients[i]}\n")

    def save() :
        save_coefficients(Fin,M.get(),filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]))




    btn_load1 = Button(tl, text="Load Signal", background="teal", foreground="white", width=15, height=3,
                       command=load, font=("Helvetica", 12))
    btn_load1.place(x=70, y=300)

    btn2 = Button(tl, text="Compare", background="teal", foreground="white", width=15, height=3, command=Compare,
                  font=("Helvetica", 12))
    btn2.place(x=390, y=300)

    btn_gen = Button(tl, text="Generate", background="teal", foreground="white", width=15, height=3,
                     command=Gen, font=("Helvetica", 12))
    btn_gen.place(x=230, y=300)
    btn3 = Button(tl, text="Save", background="teal", foreground="white", width=15, height=3, command=save,
                  font=("Helvetica", 12))
    btn3.place(x=230, y=370)
#====================================================TASK5=============================================================#
TD = []
TDI = []
TDD1 = []
TDD2 = []
TDF = []
TDFI = []
Tdd_x = []
Tdd_y = []
def Time_Domain():
    tl = Toplevel()
    tl.geometry("600x500")
    tl.title("Time Domain")
    tl.config(bg="lightblue")

    Td = IntVar()
    rdbutton1 = Radiobutton(tl, text="Sharpening", value=1, bg="lightblue", font=("Helvetica", 25), variable=Td)
    rdbutton2 = Radiobutton(tl, text="Delaying ", value=2, bg="lightblue", font=("Helvetica", 25), variable=Td)
    rdbutton3 = Radiobutton(tl, text="Advancing ", value=3, bg="lightblue", font=("Helvetica", 25), variable=Td)
    rdbutton4 = Radiobutton(tl, text="Folding ", value=4, bg="lightblue", font=("Helvetica", 25), variable=Td)
    rdbutton5 = Radiobutton(tl, text="Delaying a Folding", value=5, bg="lightblue", font=("Helvetica", 25), variable=Td)
    rdbutton6 = Radiobutton(tl, text="Advancing a Folding", value=6, bg="lightblue", font=("Helvetica", 25), variable=Td)
    rdbutton7 = Radiobutton(tl, text="Remove the DC component", value=7, bg="lightblue", font=("Helvetica", 25),variable=Td)
    rdbutton1.place(x=50, y=50)
    rdbutton2.place(x=50, y=120)
    rdbutton3.place(x=50, y=190)
    rdbutton4.place(x=250, y=50)
    rdbutton5.place(x=250, y=120)
    rdbutton6.place(x=250, y=190)
    rdbutton7.place(x=50, y=260)
    K = IntVar()
    et1 = Entry(tl, textvariable=K, font=("Helvetica", 24))
    et1.place(x=120, y=320)

    def load_signal_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    signal_type = int(file.readline().strip())
                    is_periodic = int(file.readline().strip())
                    N1 = int(file.readline().strip())

                    if signal_type == 0:
                        time_samples = []
                        amplitudes = []

                        for _ in range(N1):
                            index, amp = map(float, file.readline().split())
                            time_samples.append(index)
                            amplitudes.append(amp)
                        return time_samples, amplitudes

                    else:
                        messagebox.showerror("Error", "Invalid signal type in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")


    def Shift_Fold_Signal_Compare(file_name, Your_indices, Your_samples):
        expected_indices = []
        expected_samples = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                # process line
                L = line.strip()
                if len(L.split(' ')) == 2:
                    L = line.split(' ')
                    V1 = int(L[0])
                    V2 = float(L[1])
                    expected_indices.append(V1)
                    expected_samples.append(V2)
                    line = f.readline()
                else:
                    break
        print("Current Output Test file is: ")
        print(file_name)
        print("\n")
        if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
            print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_indices)):
            if (Your_indices[i] != expected_indices[i]):
                print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one")
                return
        for i in range(len(expected_samples)):
            if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                print("Shift_Fold_Signal Test case failed, your signal have different values from the expected one")
                return
        print("Shift_Fold_Signal Test case passed successfully")
    def load() :
        global TD
        global TDI
        TDI , TD = load_signal_from_file()

    def Compare():
        if Td.get() == 2 or Td.get() == 3 :
            Shift_Fold_Signal_Compare(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), TDFI, TD)
        elif Td.get() == 4:
            Shift_Fold_Signal_Compare(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), TDI, TDF)
        elif Td.get() == 5 or Td.get() == 6 :
            Shift_Fold_Signal_Compare(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), TDFI, TDF)
        else :
            SignalSamplesAreEqual(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), TDF)
    def Ploting(x1 , y1 , x2 , y2) :
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.stem(x1, y1)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.title('Original')
        plt.grid(True)
        plt.subplot(2, 1, 2)
        plt.stem(x2, y2)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.title('Modified')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def Gen():
        global TD
        global TDI
        global TDD1
        global TDD2
        global TDF
        global TDFI
        global Tdd_x
        global Tdd_y

        if Td.get() == 1 :
            i = 0
            j = 0
            while i < len(TD):
                if i != 0:
                    x = TD[i] - TD[i - 1]
                    TDD1.append(x)
                    Tdd_x.append(TDI[i])
                i += 1
            print(TDI)

            while j < len(TD):
                if j != 0 and j != len(TD) - 1:
                    x = TD[j + 1] - 2 * TD[j] + TD[j - 1]
                    TDD2.append(x)
                    Tdd_y.append(TDI[j])
                j += 1
            print(len(TDD1))
            print(TDD1)
            print(len(TDD2))
            print(TDD2)
        elif Td.get() == 2 :
            j = 0
            while j < len(TD)  :
                TDFI.append(TDI[j] + K.get())
                j += 1
            print(TD)
            print(TDFI)
        elif Td.get() == 3 :
            m = 0
            while m < len(TD) :
                TDFI.append(TDI[m] - K.get())
                m += 1
            print(TD)
            print(TDFI)
        elif Td.get() == 4 :
            f = len(TD) - 1
            while f >= 0 :
                TDF.append(TD[f])
                f -= 1
            print(TDF)
        elif Td.get() == 5 :
            f = len(TD) - 1
            while f >= 0:
                TDF.append(TD[f])
                f -= 1
            j = 0
            while j < len(TD):
                TDFI.append(TDI[j] + K.get())
                j += 1
            print(TDF)
            print(TDFI)
        elif Td.get() == 6 :
            f = len(TD) - 1
            while f >= 0:
                TDF.append(TD[f])
                f -= 1
            m = 0
            while m < len(TD):
                TDFI.append(TDI[m] - K.get())
                m += 1
            print(TDF)
            print(TDFI)
        else :
            mean = np.sum(TD) / len(TD)
            l = [x - mean for x in TD]
            [TDF.append(v) for v in l]
            print(TDF)

        if Td.get() == 1 :
            Ploting(Tdd_x, TDD1, Tdd_y, TDD2)
        elif Td.get() == 2 or Td.get() == 3:
            Ploting(TDI,TD,TDFI,TD)
        elif Td.get() == 4 :
            Ploting(TDI, TD, TDI, TDF)
        elif Td.get() == 5 or Td.get() == 6 :
            Ploting(TDI, TD, TDFI, TDF)







    btn_load1 = Button(tl, text="Load Signal", background="teal", foreground="white", width=15, height=3,
                       command=load, font=("Helvetica", 12))
    btn_load1.place(x=70, y=370)

    btn2 = Button(tl, text="Compare", background="teal", foreground="white", width=15, height=3, command=Compare,
                  font=("Helvetica", 12))
    btn2.place(x=390, y=370)

    btn_gen = Button(tl, text="Generate", background="teal", foreground="white", width=15, height=3,
                     command=Gen, font=("Helvetica", 12))
    btn_gen.place(x=230, y=370)
# ====================================================TASK6=============================================================#
SCC1 = []
SCCI1 = []
SCC2 = []
SCCI2 = []
SccFin = []
def S_C_C():
    tl = Toplevel()
    tl.geometry("600x500")
    tl.title("Convolution and Correlation")
    tl.config(bg="lightblue")

    Scc = IntVar()
    rdbutton1 = Radiobutton(tl, text="Smoothing", value=1, bg="lightblue", font=("Helvetica", 25), variable=Scc)
    rdbutton2 = Radiobutton(tl, text="Convolution", value=2, bg="lightblue", font=("Helvetica", 25), variable=Scc)
    rdbutton3 = Radiobutton(tl, text="Correlation", value=3, bg="lightblue", font=("Helvetica", 25), variable=Scc)
    rdbutton1.place(x=50, y=50)
    rdbutton2.place(x=50, y=120)
    rdbutton3.place(x=50, y=190)
    window_size = IntVar()
    et1 = Entry(tl, textvariable=window_size, font=("Helvetica", 24))
    et1.place(x=120, y=240)

    def load_signal_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    signal_type = int(file.readline().strip())
                    is_periodic = int(file.readline().strip())
                    N1 = int(file.readline().strip())

                    if signal_type == 0:
                        time_samples = []
                        amplitudes = []

                        for _ in range(N1):
                            index, amp = map(float, file.readline().split())
                            time_samples.append(index)
                            amplitudes.append(amp)
                        return time_samples, amplitudes

                    else:
                        messagebox.showerror("Error", "Invalid signal type in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def ConvTest(Your_indices, Your_samples):
        """
        Test inputs
        InputIndicesSignal1 =[-2, -1, 0, 1]
        InputSamplesSignal1 = [1, 2, 1, 1 ]

        InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
        InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
        """

        expected_indices = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
        expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1]

        if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
            print("Conv Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_indices)):
            if (Your_indices[i] != expected_indices[i]):
                print("Conv Test case failed, your signal have different indicies from the expected one")
                return
        for i in range(len(expected_samples)):
            if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                print("Conv Test case failed, your signal have different values from the expected one")
                return
        print("Conv Test case passed successfully")

    def Compare_Signals(file_name, Your_indices, Your_samples):
        expected_indices = []
        expected_samples = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                # process line
                L = line.strip()
                if len(L.split(' ')) == 2:
                    L = line.split(' ')
                    V1 = int(L[0])
                    V2 = float(L[1])
                    expected_indices.append(V1)
                    expected_samples.append(V2)
                    line = f.readline()
                else:
                    break
        print("Current Output Test file is: ")
        print(file_name)
        print("\n")
        if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
            print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_indices)):
            if (Your_indices[i] != expected_indices[i]):
                print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one")
                return
        for i in range(len(expected_samples)):
            if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                print("Correlation Test case failed, your signal have different values from the expected one")
                return
        print("Correlation Test case passed successfully")

    def load1() :
        global SCC1
        SCCI1 , SCC1 = load_signal_from_file()

    def load2() :
        global SCC2
        SCCI2 , SCC2 = load_signal_from_file()

    def Compare():
        if Scc.get() == 1:
            SignalSamplesAreEqual(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), SccFin)
        elif Scc.get() == 2:
            ConvTest(SCCI1 , SccFin)
        elif Scc.get() == 3:
            Compare_Signals(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), SCCI1 , SccFin)

    def rotate_signal(signal):
        rotated_signal = [0] * len(signal)
        for i in range(len(signal)):
            new_index = (i - 1) % len(signal)
            rotated_signal[new_index] = signal[i]
        return rotated_signal

    def normalized_cross_correlation(y1_, y2_):
        new_y = y2_
        N = len(y1_)
        rs = []
        f = 0
        s = 0
        nc = []
        for n in range(N):
            r = 0
            for k in range(N):
                r += ((y1_[k]) * (new_y[k]))
            new_y = rotate_signal(new_y)
            rs.append(r / N)
            f += pow(y1_[n], 2)
            s += pow(y2_[n], 2)
        for i in range(N):
            nc.append(round(5 * rs[i] / np.sqrt(f * s), 5))
        return rs, nc

    def Gen() :
        global SCC1
        global SCC2
        global SCCI1
        global SCCI2
        global SccFin
        if Scc.get() == 1 :
            for i in range(len(SCC1) - window_size.get() + 1):
                window = SCC1[i:i + window_size.get()]
                window_average = np.sum(window) / window_size.get()
                SccFin.append(window_average)
            print(SccFin)
        elif Scc.get() == 2 :
            len_signal1 = len(SCC1)
            len_signal2 = len(SCC2)
            len_output = len_signal1 + len_signal2 - 1
            output = [0] * len_output
            for i in range(len_signal1):
                for j in range(len_signal2):
                    output[i + j] += SCC1[i] * SCC2[j]
            for k in output :
                SccFin.append(k)
            print(SccFin)
        else :
            output, SccFin =normalized_cross_correlation(SCC1,SCC2)
            print(SccFin)


            print(output)
            print(SccFin)


    btn_load1 = Button(tl, text="Load Signal 1", background="teal", foreground="white", width=15, height=3,
                       command=load1, font=("Helvetica", 12))
    btn_load1.place(x=130, y=300)

    btn_load2 = Button(tl, text="Load Signal 2", background="teal", foreground="white", width=15, height=3,
                       command=load2, font=("Helvetica", 12))
    btn_load2.place(x=330, y=300)

    btn2 = Button(tl, text="Compare", background="teal", foreground="white", width=15, height=3, command=Compare,
                  font=("Helvetica", 12))
    btn2.place(x=330, y=400)

    btn_gen = Button(tl, text="Generate", background="teal", foreground="white", width=15, height=3,
                     command=Gen, font=("Helvetica", 12))
    btn_gen.place(x=130, y=400)
# ====================================================TASK7=============================================================#
FIR_Signal = []
FIR_SignalI = []
FIR = []
FIRI = []
Conv =[]
ConvI = []
upsampled_signal = []
downsampled_signal = []
fil = []
filI = []
convol = []
convolI = []
REI =[]


def FIR():
    tl = Toplevel()
    tl.geometry("600x700")
    tl.title("FIR Filter")
    tl.config(bg="lightblue")

    FirCheck = IntVar()
    rdbutton1 = Radiobutton(tl, text="Low Pass", value=1, bg="lightblue", font=("Helvetica", 25), variable=FirCheck)
    rdbutton2 = Radiobutton(tl, text="High Pass", value=2, bg="lightblue", font=("Helvetica", 25), variable=FirCheck)
    rdbutton3 = Radiobutton(tl, text="Band Pass", value=3, bg="lightblue", font=("Helvetica", 25), variable=FirCheck)
    rdbutton4 = Radiobutton(tl, text="Band Stop", value=4, bg="lightblue", font=("Helvetica", 25), variable=FirCheck)
    rdbutton1.place(x=30, y=10)
    rdbutton2.place(x=30, y=70)
    rdbutton3.place(x=250, y=10)
    rdbutton4.place(x=250, y=70)
    FS_FIR = IntVar()
    FC1_FIR = IntVar()
    FC2_FIR = IntVar()
    STOP_FIR = IntVar()
    TRANSITION_FIR = IntVar()
    M_IN = IntVar()
    L_IN = IntVar()
    et1 = Entry(tl, textvariable=FS_FIR, font=("Helvetica", 18))
    et2 = Entry(tl, textvariable=FC1_FIR, font=("Helvetica", 18))
    et3 = Entry(tl, textvariable=FC2_FIR, font=("Helvetica", 18))
    et4 = Entry(tl, textvariable=STOP_FIR, font=("Helvetica", 18))
    et5 = Entry(tl, textvariable=TRANSITION_FIR, font=("Helvetica", 18))
    et6 = Entry(tl, textvariable=M_IN, font=("Helvetica", 18))
    et7 = Entry(tl, textvariable=L_IN, font=("Helvetica", 18))
    et1.place(x=90, y=125)
    et2.place(x=100, y=165)
    et3.place(x=100, y=215)
    et4.place(x=290, y=255)
    et5.place(x=250, y=295)
    et6.place(x=90, y=335)
    et7.place(x=90, y=375)
    l1 = Label(tl, text="Fs :", font=("Helvetica", 20),background="lightblue")
    l2 = Label(tl, text="Fc1 :", font=("Helvetica", 20), background="lightblue")
    l3 = Label(tl, text="Fc2 :", font=("Helvetica", 20), background="lightblue")
    l4 = Label(tl, text="Stop Attenuation δs :", font=("Helvetica", 20), background="lightblue")
    l5 = Label(tl, text="Transition Band :", font=("Helvetica", 20), background="lightblue")
    l6 = Label(tl, text="M :", font=("Helvetica", 20), background="lightblue")
    l7 = Label(tl, text="L :", font=("Helvetica", 20), background="lightblue")
    l1.place(x=30, y=120)
    l2.place(x=30, y=160)
    l3.place(x=30, y=210)
    l4.place(x=30, y=250)
    l5.place(x=30, y=290)
    l6.place(x=30, y=330)
    l7.place(x=30, y=370)

    def load_signal_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    signal_type = int(file.readline().strip())
                    is_periodic = int(file.readline().strip())
                    N1 = int(file.readline().strip())

                    if signal_type == 0:
                        time_samples = []
                        amplitudes = []

                        for _ in range(N1):
                            index, amp = map(float, file.readline().split())
                            time_samples.append(index)
                            amplitudes.append(amp)
                        return time_samples, amplitudes

                    else:
                        messagebox.showerror("Error", "Invalid signal type in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def load() :
        global FIR
        global FIRI
        FIRI , FIR = load_signal_from_file()

    def Compare_Signals(file_name, Your_indices, Your_samples):
        expected_indices = []
        expected_samples = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                # process line
                L = line.strip()
                if len(L.split(' ')) == 2:
                    L = line.split(' ')
                    V1 = int(L[0])
                    V2 = float(L[1])
                    expected_indices.append(V1)
                    expected_samples.append(V2)
                    line = f.readline()
                else:
                    break
        print("Current Output Test file is: ")
        print(file_name)
        print("\n")
        if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
            print("Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_indices)):
            if (Your_indices[i] != expected_indices[i]):
                print("Test case failed, your signal have different indicies from the expected one")
                return
        for i in range(len(expected_samples)):
            if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                print("Test case failed, your signal have different values from the expected one")
                return
        print("Test case passed successfully")

    def Compare():
            Compare_Signals(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), FIR_SignalI,FIR_Signal)
    def Compare_Conv():
            Compare_Signals(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), ConvI, Conv)
    def Compare_re():
        if M_IN.get() == 0 and L_IN.get() != 0:
            Compare_Signals(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), convolI, convol)
        elif M_IN.get() != 0 and L_IN.get() == 0:
            Compare_Signals(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), REI, downsampled_signal)
        elif M_IN.get() != 0 and L_IN.get() != 0:
            Compare_Signals(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]), REI, downsampled_signal)

    def FIR_FILTER(fs , fc1 , fc2  , stop , transaction , filter):
        out = 0.0
        fin =[]
        window = []
        win = 0
        TransitionBand = transaction / fs
        N = -1
        window_arr = []
        if stop <= 21:
            N = 0.9 / TransitionBand
            N = math.ceil(N)
            if N % 2 == 0:
                N += 1
            for i in range(int((N - 1) / 2) + 1):
                window_arr.append(1)
        elif stop <= 44:
            N = 3.1 / TransitionBand
            N = math.ceil(N)
            if N % 2 == 0:
                N += 1
            for i in range(int((N - 1) / 2) + 1):
                window_arr.append(0.5 + (0.5 * math.cos((2 * np.pi * i) / N)))
        elif stop <= 53:

            N = 3.3 / TransitionBand
            N = math.ceil(N)
            if N % 2 == 0:
                N += 1

            for i in range(int((N - 1) / 2) + 1):
                window_arr.append(0.54 + (0.46 * math.cos((2 * np.pi * i) / N)))

        else:
            N = 5.5 / TransitionBand
            N = math.ceil(N)
            if N % 2 == 0:
                N += 1

            for i in range(int((N - 1) / 2) + 1):
                window_arr.append(
                    0.42 + (0.5 * math.cos((2 * np.pi * i) / (N - 1))) + (0.08 * math.cos((4 * np.pi * i) / (N - 1))))

        half = ((N + 1) / 2) - 1
        result = [0 for i in range(N)]
        if filter == 1 :
            fc1 = fc1 + ((TransitionBand * fs) / 2)
            fc1 /= fs
            omega = (2 * np.pi * fc1)
            result[int(half)] = 2 * fc1
            for i in range(int(half) + 1, N):
                j = i - half
                result[i] = 2 * fc1 * math.sin(j * omega) / (omega * j)
                result[int(half - j)] = result[i]

        elif filter == 2 :
            fc1 = fc1 - ((TransitionBand * fs) / 2)
            fc1 /= fs
            omega = (2 * np.pi * fc1)
            result[int(half)] = 1 - (2 * fc1)
            for i in range(int(half) + 1, N):
                j = i - half
                result[i] = -1 * (2 * fc1 * math.sin(j * omega) / (omega * j))
                result[int(half - j)] = result[i]

        elif filter == 3 :
            fc1 = fc1 - ((TransitionBand * fs) / 2)
            fc1 /= fs
            fc2 = fc2 + ((TransitionBand * fs) / 2)
            fc2 /= fs
            omega = (2 * np.pi * fc1)
            omega2 = (2 * np.pi * fc2)
            result[int(half)] = 2 * (fc2 - fc1)
            for i in range(int(half) + 1, N):
                j = i - half
                result[i] = (2 * fc2 * math.sin(j * omega2) / (omega2 * j)) - (
                            2 * fc1 * math.sin(j * omega) / (omega * j))
                result[int(half - j)] = result[i]

        elif filter == 4 :
            fc1 = fc1 + ((TransitionBand * fs) / 2)
            fc1 /= fs
            fc2 = fc2 - ((TransitionBand * fs) / 2)
            fc2 /= fs
            omega = (2 * np.pi * fc1)
            omega2 = (2 * np.pi * fc2)
            result[int(half)] = 1 - (2 * (fc2 - fc1))
            for i in range(int(half) + 1, N):
                j = i - half
                result[i] = (2 * fc1 * math.sin(j * omega) / (omega * j)) - (
                            2 * fc2 * math.sin(j * omega2) / (omega2 * j))
                result[int(half - j)] = result[i]


        j = int(-(((N + 1) / 2) - 1))
        final = []
        for i in range(N):
            final.append(result[i] * window_arr[abs(j)])
            j += 1
        index_arr = [i for i in range(int(-(((N + 1) / 2) - 1)), int(((N + 1) / 2)))]
        return index_arr, final

    def conv(signal1,signal2,n):
        global Conv
        global ConvI
        len_signal1 = len(signal1)
        len_signal2 = len(signal2)
        N = len(n)
        len_output = len_signal1 + len_signal2 - 1
        output = [0] * len_output
        index_conv = []
        half = ((N + 1) / 2) - 1
        k = -half
        for i in range(len_output):
            ConvI.append(k)
            k += 1
        for i in range(len_signal1):
            for j in range(len_signal2):
                output[i + j] += signal1[i] * signal2[j]
        for i in output:
            Conv.append(i)
        print(ConvI)
        print(Conv)
        return ConvI,Conv

    def Resampling(input_signal, M, L):
        global upsampled_signal
        global downsampled_signal
        global fil
        global filI
        global convol
        global convolI
        global REI
        if M == 0 and L != 0:
            for i in range(len(input_signal)):
                upsampled_signal.extend([input_signal[i]] + [0] * (L - 1))
            for i in range(L - 1):
                upsampled_signal.pop()
            filI , fil = FIR_FILTER(FS_FIR.get(),FC1_FIR.get(),FC2_FIR.get(),STOP_FIR.get(),TRANSITION_FIR.get(),FirCheck.get())
            convolI,convol = conv(upsampled_signal,fil,filI)
            print(convolI)
            print(convol)

        elif M != 0 and L == 0:
            filI, fil = FIR_FILTER(FS_FIR.get(), FC1_FIR.get(), FC2_FIR.get(), STOP_FIR.get(), TRANSITION_FIR.get(),
                                   FirCheck.get())
            convolI,convol = conv(input_signal, fil, filI)
            for j in convol[::M]:
                downsampled_signal.append(j)
            k = -((len(filI) + 1) / 2) + 1
            for i in range(len(downsampled_signal)):
                REI.append(k)
                k += 1
            print(REI)
            print(downsampled_signal)

        elif M != 0 and L != 0:
            for i in range(len(input_signal)):
                upsampled_signal.extend([input_signal[i]] + [0] * (L - 1))
            for i in range(L - 1):
                upsampled_signal.pop()
            filI, fil = FIR_FILTER(FS_FIR.get(), FC1_FIR.get(), FC2_FIR.get(), STOP_FIR.get(), TRANSITION_FIR.get(),
                                   FirCheck.get())
            convolI, convol = conv(upsampled_signal, fil, filI)
            for j in convol[::M]:
                downsampled_signal.append(j)
            k = -((len(filI) + 1) / 2) + 1
            for i in range(len(downsampled_signal)):
                REI.append(k)
                k += 1
            print(REI)
            print(downsampled_signal)


    def con():
        global FIR
        ci ,c =conv(FIR , FIR_Signal , FIR_SignalI)

    def re():
        global FIR
        Resampling(FIR, M_IN.get(), L_IN.get())

    def Gen():
        global FIR_Signal
        global FIR_SignalI
        FIR_SignalI, FIR_Signal = FIR_FILTER(FS_FIR.get(),FC1_FIR.get(),FC2_FIR.get(),STOP_FIR.get(),TRANSITION_FIR.get(),FirCheck.get())
        print(FIR_SignalI)
        print(FIR_Signal)





    btn_load = Button(tl, text="Load Signal", background="teal", foreground="white", width=15, height=3,
                       command=load, font=("Helvetica", 12))
    btn_load.place(x=50, y=450)
    btn1 = Button(tl, text="Compare", background="teal", foreground="white", width=15, height=3, command=Compare,
                  font=("Helvetica", 12))
    btn1.place(x=350, y=450)
    btn2 = Button(tl, text="Compare Convolution", background="teal", foreground="white", width=20, height=3, command=Compare_Conv,
                  font=("Helvetica", 12))
    btn2.place(x=250, y=520)
    btn_gen = Button(tl, text="Generate", background="teal", foreground="white", width=15, height=3,
                     command=Gen, font=("Helvetica", 12))
    btn_gen.place(x=200, y=450)
    btn_con = Button(tl, text="Convolution", background="teal", foreground="white", width=15, height=3,
                     command=con, font=("Helvetica", 12))
    btn_con.place(x=100, y=520)
    btn_re = Button(tl, text="Resampling", background="teal", foreground="white", width=15, height=3,
                     command=re, font=("Helvetica", 12))
    btn_re.place(x=100, y=590)
    btn3 = Button(tl, text="Compare Resampling", background="teal", foreground="white", width=20, height=3,
                  command=Compare_re,
                  font=("Helvetica", 12))
    btn3.place(x=250, y=590)
#====================================================END===============================================================#
l1 = Label(home, text="Welcome To Our Digital Signal Processing App", font=("Helvetica", 20), background="lightblue")
l1.place(x=140, y=20)

btn1 = Button(home, text="Generating Signal", background="teal", foreground="white", width=15, height=3, command=genSignal, font=("Helvetica", 14))
btn1.place(x=100, y=120)

btn2 = Button(home, text="Read Signal", background="teal", foreground="white", width=15, height=3, command=RSignal, font=("Helvetica", 14))
btn2.place(x=300, y=120)

btn3 = Button(home, text="Arithmetic Operations", background="teal", foreground="white", width=18, height=3, command=Arithmetic_Operations, font=("Helvetica", 14))
btn3.place(x=500, y=120)

btn4 = Button(home, text="Quantize Signal", background="teal", foreground="white", width=15, height=3, command=Quantization, font=("Helvetica", 14))
btn4.place(x=100, y=220)

btn5 = Button(home, text="Frequency Domain", background="teal", foreground="white", width=15, height=3, command=Frequency_Domain, font=("Helvetica", 14))
btn5.place(x=300, y=220)

btn6 = Button(home, text="Time Domain", background="teal", foreground="white", width=18, height=3, command=Time_Domain, font=("Helvetica", 14))
btn6.place(x=500, y=220)

btn7 = Button(home, text="Convolution and Correlation", background="teal", foreground="white", width=26, height=3, command=S_C_C, font=("Helvetica", 14))
btn7.place(x=100, y=320)

btn8 = Button(home, text="FIR Filter", background="teal", foreground="white", width=27, height=3, command=FIR, font=("Helvetica", 14))
btn8.place(x=401, y=320)

home.mainloop()