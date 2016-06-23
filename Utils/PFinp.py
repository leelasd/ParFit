#!/usr/bin/env python
#
# This a ParFit input file generating program.
#
#  To Do:
#  1. Error out if dihedral is given incorrectly (such as two numbers are the
#     same or not all numbers are given)
#  2. For values that are not known, the program will leave a place holder that a
#     user can then change using a text editor.
#  3. Add option to change two or three parameters per line.
#  4. Add new parameter fitting options, bond length, bond angle.
#

####################################################################################
# --- Functions ---
def PES_coordinate():
    print("The following prompts define the variables used to generate" +
          "the QM PESs.")
    atom_indices = raw_input("Enter atom indices separated by a space.\n")
    i_coord = raw_input("Enter the initial length or angle.\n")
    f_coord = raw_input("Enter the final length or angle.\n")
    coord_s = raw_input("Enter the lenght or angle step size.\n")
    return "{0}, {1} {2} {3}".format(atom_indices, i_coord, f_coord, coord_s)

def quantumdata(qmdatachoice) :
    if (qmdatachoice == "a" or qmdatachoice == "") :
        qmdata = 'comp'
        print "Selected compact file; one file contains the QM data."
        filenameroot = raw_input("Enter the root filename. ")
    elif (qmdatachoice == "b") :
        qmdata = 'full'
        print "Selected full; a series of files contain QM data."
        filenameroot = raw_input("Enter the root filename. ")
    return qmdata, filenameroot

def qmdata_prompt():
    print("<< QM data file format >>\n" +
          "(a) Compact: QM data is contained in one file that includes fixed\n" +
          "    bond lengths, bond angles, or torsion angle geometries.\n" +
          "(b) Series: GAMESS log files, one for each fixed bond length,\n" +
          "    bond angle, or torsion angle geometry.\n" +
          "Enter: a or b. [a]")

def parameter_lines(PEStype, no_PESs):
    if PEStype == "diha" :
        no_of_parameter_lines = no_PESs
        p_list_len = no_of_parameter_lines*4
        list_params = [None] * p_list_len
        for m in range(0, p_list_len, 4) :
            list_params[m]= raw_input("Enter parameter line number for the dihedral to be fit. ")
            for i in range(1, 4) :
                c_or_p = raw_input("Enter 'p' if Line " + list_params[m] + " V" +
                        str(i) + " should be varied during ParFit run. ")
                if c_or_p == "p" :
                    c_or_p = "p"
                else :
                    c_or_p = "c"
                list_params[m + i] = c_or_p
        i = raw_input("How many pairs of parameters are coupled? [0] ")
        if i == "" :
            i = 0
        else :
            i = int(i)
            print("Please identify the coupled parameters by giving the line numbers \n" +
                  "and parameter (1, 2 or 3 for V1, V2 and V3) " +
                  "in the following format: \n" +
                  "\t[line number] [line number] [parameter number] ")
        for n in range(i) :
            q, r, s = str.split(raw_input("Enter the line and parameter numbers. "))
            q_index = int(list_params.index(q))
            r_index = int(list_params.index(r))
            s = int(s)
            list_params[q_index + s] = list_params[r_index + s] = "p" + str(n + 1)
    else :
        m = raw_input("Enter parameter line number of the parameters to be fit. ")
        list_params = m + " p p"
#        print list_params  #print for debugging
    return list_params
###################################################################################
###################################################################################

# --- Determine ParFit input file name ---
print("Enter the name of ParFit input file to create, if blank, the file " +
      "name will be PFinput.\n")
pyout = raw_input()
if (pyout == "") :
    pyout = "PFinput"
    print "[PFinp]: Input filename:", pyout, "\n"
else :
    pyout == pyout
    print "[PFinp]: Input filename:", pyout, "\n"

# --- Open the file for writing ---
f = open(pyout,'w')

# --- Select the parameter type, bond length, bond angle, torsion. ---
property_type = raw_input('''Choose from the properties below:
(a) bond length
(b) bond angle
(c) torsion (default)
    \n
Enter: a, b, or c.\n''')

if (property_type == "a") :
    property_type = 'bond'
    parameterize = "bond length"
elif (property_type == "b") :
    property_type = 'angl'
    parameterize = "bond angle"
elif (property_type == "c") :
    property_type = 'diha'
    parameterize = "torsion angle"
else :
    print "The default, torsion angle, was chosen."
    property_type = 'diha'
    parameterize = "torsion angle"

# --- Multiple dihedral angle file fitting. ---
if (property_type == "bond" or property_type == "angl") :
    qmdata_prompt()
    qm_file_properties = quantumdata(qmdatachoice = raw_input())
    no_PESs = 1
#elif (property_type == "angl"):
#    qmdata_prompt()
#    qm_file_properties = quantumdata(qmdatachoice = raw_input())
#    no_PESs = 1
elif (property_type == "diha") :
    no_PESs = int(raw_input("Enter the number of PESs to be fit.\n"))
    print >> f, "mult, ", no_PESs
    for n in range(0, no_PESs) :
        qmdata_prompt()
        qm_f_properties =  quantumdata(qmdatachoice = raw_input())
        print qm_f_properties
        if (qm_f_properties[0] != "comp") :
            PES_properties = PES_coordinate()

# if not running a bond length/angle run, use this path.
else :
    print "[PFinp] Error: You have not properly chosen a property to parameterize."

# --- Determine which parameters will be changed by ParFit ---
list_params = parameter_lines(property_type, no_PESs)

# --- Get engine path ---
engine_path = raw_input("\nWhat is the full engine.exe path?\n")

# --- Determine the type of MM file that is to be modified ---
mmtypchoice = raw_input("\nChoose the MM type (mm3 or mmff94) parameters to be fit\n(a) MM3 - default\n(b) MMFF94\nChoose a or b.\n")
if (mmtypchoice == 'a' or mmtypchoice == "") :
    carbontyp = 50
    mmtyp = 'mm3'
elif (mmtypchoice == 'b') :
    carbontyp = 37
    mmtyp = 'mmff94'
else :
    mmtyp = 'mm3'
    print("Warning: Check the MM type you entered, the only options are a and b.\n" +
          "Default will be chosen.")

# --- Choose the algorithm used to fit parameters. ---
print("<< Fitting alorithms >>\n" +
      "(a) genetic algorithm\n" +
      "(b) Nedler-Mead algorithm\n" +
      "(c) hybrid: genetic followed by Nedler-Mead algorithm\n")
alg = raw_input("Select a, b, or c. [c] ")
if (alg == 'a') :
    alg = 'ga'
elif (alg == 'b') :
    alg = 'fmin'
elif (alg == 'c') :
    alg = 'hybr'
else :
   alg = 'hybr'
   print "Default was chosen."

# --- Printing csv file option ---
printcsv = raw_input("\nEnter \"n\" if you do NOT want ParFit to print a csv format file\ncontaining the angles, QM energy, and the optmized MM energies.\n")
if (printcsv == 'n') :
    csv = "csv_off"
else :
    csv = "csv_on"

print >> f, engine_path
print >> f, mmtyp
print >> f, alg
if property_type == "diha" :
    for i in range(0, no_PESs, 4):
        parameters = str(list_params[i]) + " " + list_params[i + 1] + " " + list_params[i + 2]
        print >> f, parameters
#else :                 #print for debugging
#    print list_params  #print for debugging
print >> f, csv

print "\nYour ParFit input file name {0} has been generated.\n".format(pyout)

exit()
