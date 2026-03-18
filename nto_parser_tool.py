import re

def extract_nto_data(filename, states='all', threshold=0):

    # global constants   
    state_string_start = 'TD-DFT/TDA EXCITED STATES'   
    state_string_end = 'TD-DFT/TDA-EXCITATION SPECTRA'  
    nto_string_start ='NATURAL TRANSITION ORBITALS'  
    found_nto = False                                                                      

    #global lists
    statelist = list()            #mode
    energylist = list()           #energy cm-1
    intenslist = list()           #fosc
    nmlist = list()               #wavelength 
    orblist = list()              #list of orbital -> orbital transition
    md_table = list()             #table for the markdown output
    statedict = dict()            #dictionary of states with all transitions
    selected_statedict = dict()   #dictionary of selected states with all transitions and or with those above the threshold
 
    #for NTO
    nto_orblist=list()            #list of orbital -> orbital transition for NTOs
    nto_statedict=dict()          #dictionary of states with all transitions for NTOs


    with open(filename, "r") as input_file:
        for line in input_file:

            if state_string_start in line:
                for line in input_file:
                    #build the state - with several transitions dict: dict[state]=list(orb1 -> orb2, xx%), list(orb3 -> orb4, xx%)
                    #first the state
                    if re.search(r"STATE\s{1,}(\d{1,}):",line):
                        match_state=re.search(r"STATE\s{1,}(\d{1,}):",line)
                    #transitions here in orblist
                    elif re.search(r"\d{1,}[a,b]\s{1,}->\s{1,}\d{1,}[a,b]",line):
                        match_orbs=re.search(r"(\d{1,}[a,b]\s{1,}->\s{1,}\d{1,}[a,b])\s{1,}:\s{1,}(\d{1,}.\d{1,})",line)
                        orblist.append((match_orbs.group(1).replace("  "," "),match_orbs.group(2)))
                    #add orblist to statedict and clear orblist for next state
                    elif re.search(r"^\s*$",line):
                        if orblist:
                            statedict[match_state.group(1)] = orblist
                            orblist=[] 
                                                        
                    #exit here
                    elif nto_string_start in line:
                        break
                    elif state_string_end in line:
                        break
            

            #same for NTOs
            if re.search(r"FOR STATE\s{1,}(\d{1,})",line):
                #found NTO in orca.out
                found_nto = True
                match_state_nto=re.search(r"FOR STATE\s{1,}(\d{1,})",line)
            elif re.search(r"\d{1,}[a,b]\s{1,}->\s{1,}\d{1,}[a,b]",line):
                match_orbs_nto=re.search(r"(\d{1,}[a,b]\s{1,}->\s{1,}\d{1,}[a,b])\s{1,}: n=\s{1,}(\d{1,}.\d{1,})",line)
                nto_orblist.append((match_orbs_nto.group(1).replace(" ","").replace("a","").split("->"),match_orbs_nto.group(2)))
                
            #add orblist to statedict and clear orblist for next state
            elif re.search(r"^\s*$",line):
                if nto_orblist:
                    nto_statedict[match_state_nto.group(1)] = nto_orblist
                    nto_orblist=[] 

    #build selected_statedict from statedict with selected states
    if states == 'all':
        selected_statedict = nto_statedict

    else:
        for elements in states:
                selected_statedict[elements]=nto_statedict[elements]

                
    #remove transitions below threshold from selected_statedict
    for elements in selected_statedict:
        transition_list=[]
        for v in selected_statedict[elements]:
            if float(v[1])*100 >= threshold:
                transition_list.append(v)
        selected_statedict[elements]=transition_list    

    return selected_statedict

print(extract_nto_data(filename='water.out', threshold=0.1))